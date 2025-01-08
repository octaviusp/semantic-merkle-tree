from merkle_tree.merkle_tree_integrity import verification
from merkle_tree.merkle_tree_generation import generate_tree

if __name__ == "__main__":
    # This line generate the merkle tree and save it to merkle_tree.json for the folder_1
    generate_tree("folder_1")
    # This line verify the merkle tree integrity for the folder_1 (Check that now there is no changes so this is false)
    verification("merkle_tree.json", "folder_1")

    # We gonna make a change in the folder_1/file_1.txt (the old content was "a", the new content is "cb" , so integrity is broken)
    with open("folder_1/file_1.txt", "w") as f:
        f.write("The human is walking in the park")

    # Now we gonna verify the merkle tree integrity for the folder_1 (Check that now there is a change so this is true)
    verification("merkle_tree.json", "folder_1")

