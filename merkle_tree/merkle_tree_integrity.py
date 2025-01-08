import json
import os
from .merkle_tree_generation import MerkleTree

def verify_merkle_tree_integrity(original_json_path: str, directory_path: str) -> bool:
    """
    Verify the integrity of a Merkle tree by comparing against a saved JSON file
    
    Args:
        original_json_path (str): Path to the original merkle_tree.json
        directory_path (str): Path to the directory to verify
        
    Returns:
        bool: True if integrity is maintained, False if changes detected
    """
    # Load the original merkle tree data
    with open(original_json_path, 'r') as f:
        original_tree_data = json.load(f)
    
    # Generate new merkle tree
    current_tree = MerkleTree(directory_path)
    current_tree.build_tree()
    
    # Save current tree to temporary file
    current_tree.save_tree("current_merkle_tree.json")
    
    # Load current tree data
    with open("current_merkle_tree.json", 'r') as f:
        current_tree_data = json.load(f)
    
    # Clean up temporary file
    os.remove("current_merkle_tree.json")
    
    # Compare root hashes
    if original_tree_data["root_hash"] != current_tree_data["root_hash"]:
        print("Root hash mismatch - directory structure or file contents have changed")
        return False
        
    # Compare nodes
    if original_tree_data["nodes"] != current_tree_data["nodes"]:
        print("Node hashes mismatch - file contents or structure have changed")
        return False
        
    # Compare leaves
    if set(original_tree_data["leaves"]) != set(current_tree_data["leaves"]):
        print("Leaf nodes mismatch - files have been added, removed or modified")
        return False
        
    # Compare hierarchy
    if original_tree_data["hierarchy"] != current_tree_data["hierarchy"]:
        print("Hierarchy mismatch - directory structure has changed")
        return False
    
    print("Merkle tree integrity verified - no changes detected")
    return True

def verification(merkle_tree_json_path: str, directory_path: str) -> bool:
    # Verify the merkle tree integrity
    original_json = merkle_tree_json_path
    directory = directory_path
    
    if not os.path.exists(original_json):
        print(f"Error: {original_json} not found")
        return False
        
    if not os.path.exists(directory):
        print(f"Error: Directory {directory} not found")
        return False
        
    is_valid = verify_merkle_tree_integrity(original_json, directory)
    if not is_valid:
        return False
    else:
        return True
