import os
import hashlib
import json
from typing import List, Dict, Optional, Tuple

class MerkleTree:
    def __init__(self, path: str):
        self.path = path
        self.leaves = []
        self.nodes = {}
        self.hierarchy = {}
        
    def _get_file_hash(self, filepath: str) -> str:
        """Calculate SHA256 hash of a file"""
        sha256_hash = hashlib.sha256()
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def _get_dir_contents(self, dir_path: str) -> Tuple[List[str], List[str]]:
        """Get files and subdirectories in a directory"""
        files = []
        subdirs = []
        for item in os.listdir(dir_path):
            full_path = os.path.join(dir_path, item)
            if os.path.isfile(full_path):
                files.append(full_path)
            elif os.path.isdir(full_path):
                subdirs.append(full_path)
        return sorted(files), sorted(subdirs)

    def _hash_dir(self, dir_path: str) -> Optional[str]:
        """Calculate hash for a directory by combining its contents"""
        files, subdirs = self._get_dir_contents(dir_path)
        
        hashes = []
        dir_contents = {"files": {}, "subdirs": {}}
        
        # Get hashes of files
        for file_path in files:
            file_hash = self._get_file_hash(file_path)
            self.nodes[file_hash] = file_path
            hashes.append(file_hash)
            dir_contents["files"][os.path.basename(file_path)] = file_hash
            
        # Get hashes of subdirectories
        for subdir in subdirs:
            subdir_hash = self._hash_dir(subdir)
            if subdir_hash:
                hashes.append(subdir_hash)
                dir_contents["subdirs"][os.path.basename(subdir)] = subdir_hash

        if not hashes:
            return None

        # Combine all hashes
        combined = "".join(sorted(hashes))
        dir_hash = hashlib.sha256(combined.encode()).hexdigest()
        self.nodes[dir_hash] = dir_path
        self.hierarchy[dir_hash] = dir_contents
        return dir_hash

    def build_tree(self) -> Dict:
        """Build the Merkle tree from directory structure"""
        self.nodes = {}
        self.hierarchy = {}
        root_hash = self._hash_dir(self.path)
        if root_hash:
            self.leaves = [h for h, v in self.nodes.items() if os.path.isfile(v)]
        return self.nodes

    def get_root_hash(self) -> str:
        """Get the root hash of the Merkle tree"""
        if not self.nodes:
            return ""
        for hash_, path in self.nodes.items():
            if path == self.path:
                return hash_
        return ""

    def verify_file(self, filepath: str) -> bool:
        """Verify if a file's hash exists in the Merkle tree"""
        if not os.path.exists(filepath):
            return False
        file_hash = self._get_file_hash(filepath)
        return file_hash in self.nodes

    def save_tree(self, output_file: str = "merkle_tree.json"):
        """Save the Merkle tree structure to a JSON file"""
        tree_data = {
            "root_hash": self.get_root_hash(),
            "nodes": self.nodes,
            "leaves": self.leaves,
            "hierarchy": self.hierarchy
        }
        with open(output_file, "w") as f:
            json.dump(tree_data, f, indent=4)

def generate_tree(directory_path: str):
    tree = MerkleTree(directory_path)
    tree.build_tree()
    tree.save_tree()
