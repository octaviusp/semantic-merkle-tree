#!/usr/bin/env python3
"""
Semantic Merkle Tree (all-in-one) – embeddings + SHA-256
Example Usage:
  python3 main.py build  <input_folder>
  python3 main.py verify <input_folder>
It will save/read its state in index.json next to the script.
"""

from __future__ import annotations
import argparse, json, hashlib, sys, time
from pathlib import Path
from typing import Dict, List, Tuple
import numpy as np
from tqdm import tqdm

# ── embeddings ─────────────────────────────────────────────────────────────
try:
    from sentence_transformers import SentenceTransformer
except ImportError:
    sys.exit("Install sentence-transformers:  pip install sentence-transformers")

MODEL = SentenceTransformer("all-MiniLM-L6-v2")
THETA = 0.70                    # minimum similarity for semantic equivalence
INDEX_FILE = Path("index.json")   # persists leaves + root

# ── small utilities ────────────────────────────────────────────────────────
def sha256(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def cosine(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

def embed(text: str) -> np.ndarray:
    return MODEL.encode(text, convert_to_numpy=True, normalize_embeddings=True)

def load_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(encoding="latin1", errors="replace")

# ── Merkle helpers ─────────────────────────────────────────────────────────
def build_merkle_hashes(leaf_hashes: List[str]) -> str:
    lvl = leaf_hashes[:]
    if not lvl:
        return ""
    while len(lvl) > 1:
        nxt = []
        it = iter(lvl)
        for left in it:
            right = next(it, left)          # duplicate if odd
            nxt.append(sha256((left+right).encode()))
        lvl = nxt
    return lvl[0]

# ── persistent state ───────────────────────────────────────────────────────
def load_index() -> Dict:
    if INDEX_FILE.exists():
        return json.loads(INDEX_FILE.read_text())
    return {"leaves": {}, "root_hash": ""}

def save_index(idx: Dict):
    INDEX_FILE.write_text(json.dumps(idx, indent=2))

# ── build ──────────────────────────────────────────────────────────────────
def cmd_build(folder: Path):
    idx = {"leaves": {}, "root_hash": ""}
    leaves_order: List[Tuple[str, str]] = []   # (path, sha)
    for fp in tqdm(sorted(folder.rglob("*")), desc="building"):
        if fp.is_file():
            raw = fp.read_bytes()
            text = load_text(fp)
            emb = embed(text).tolist()
            sha = sha256(raw)
            idx["leaves"][str(fp)] = {"sha": sha, "emb": emb, "ts": time.time()}
            leaves_order.append((str(fp), sha))
    root = build_merkle_hashes([sha for _, sha in leaves_order])
    idx["root_hash"] = root
    save_index(idx)
    print(f"Build complete. root_hash = {root}")

# ── verify ────────────────────────────────────────────────────────────────
def cmd_verify(folder: Path):
    idx = load_index()
    if not idx["leaves"]:
        sys.exit("index.json is empty – run build first.")
    changed: List[str] = []
    # update/create leaves
    for fp in tqdm(sorted(folder.rglob("*")), desc="verifying"):
        if not fp.is_file():
            continue
        raw = fp.read_bytes()
        text = load_text(fp)
        sha = sha256(raw)
        new_emb = embed(text)
        leaf = idx["leaves"].get(str(fp))
        if leaf is None:
            # new file
            idx["leaves"][str(fp)] = {"sha": sha, "emb": new_emb.tolist(), "ts": time.time()}
            changed.append(str(fp))
            continue
        # compare latent meaning
        old_emb = np.array(leaf["emb"])
        sim = cosine(old_emb, new_emb)
        print(f"Cosine similarity for '{fp}': {sim:.6f}")
        if sim < THETA:             # relevant change
            idx["leaves"][str(fp)] = {"sha": sha, "emb": new_emb.tolist(), "ts": time.time()}
            changed.append(str(fp))
    # recalculate root
    leaf_hashes = [d["sha"] for _, d in sorted(idx["leaves"].items())]
    new_root = build_merkle_hashes(leaf_hashes)
    idx["root_hash"] = new_root
    save_index(idx)
    # output
    if changed:
        print("Files with *latent meaning* change:")
        for p in changed:
            print("  •", p)
    else:
        print("No semantic changes.")
    print("root_hash =", new_root)

# ── CLI ────────────────────────────────────────────────────────────────────
def main():
    ap = argparse.ArgumentParser(description="Semantic Merkle Tree – simple all-in-one", usage="""
  poetry run python3 main.py build  ./example_folder -> Build the first Merkle tree
  # Do a change in the example_folder then run:
  poetry run python3 main.py verify ./example_folder -> Verify the changes""")
    ap.add_argument("command", choices=["build", "verify"])
    ap.add_argument("folder", help="Input folder path")
    
    args = ap.parse_args()

    folder = Path(args.folder).expanduser().resolve()
    if not folder.exists():
        sys.exit("Folder does not exist.")

    if args.command == "build":
        cmd_build(folder)
    elif args.command == "verify":
        cmd_verify(folder)

if __name__ == "__main__":
    main()
