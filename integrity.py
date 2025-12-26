import hashlib
import os

HASH_FILE = "hash_store.txt"

def calculate_hash(file_path):
    """Calculate SHA256 hash of a file"""
    sha256 = hashlib.sha256()
    with open(file_path, "rb") as f:
        while chunk := f.read(4096):
            sha256.update(chunk)
    return sha256.hexdigest()


def load_previous_hashes():
    """Load stored hashes from file"""
    hashes = {}
    if os.path.exists(HASH_FILE):
        with open(HASH_FILE, "r") as f:
            for line in f:
                file, hash_value = line.strip().split("||")
                hashes[file] = hash_value
    return hashes


def save_hashes(hashes):
    """Save hashes to file"""
    with open(HASH_FILE, "w") as f:
        for file, hash_value in hashes.items():
            f.write(f"{file}||{hash_value}\n")


def check_file_integrity(directory):
    old_hashes = load_previous_hashes()
    new_hashes = {}

    print("\n🔍 Checking File Integrity...\n")

    for filename in os.listdir(directory):
        if filename == HASH_FILE:
            continue

        file_path = os.path.join(directory, filename)

        if os.path.isfile(file_path):
            current_hash = calculate_hash(file_path)
            new_hashes[filename] = current_hash

            if filename in old_hashes:
                if old_hashes[filename] == current_hash:
                    print(f"✅ {filename} - Unchanged")
                else:
                    print(f"⚠️ {filename} - Modified")
            else:
                print(f"🆕 {filename} - New File")

    save_hashes(new_hashes)
    print("\n✔ Integrity check completed.\n")


if __name__ == "__main__":
    folder_path = input("Enter folder path to monitor (or press Enter for current folder): ")

    if folder_path == "":
        folder_path = os.getcwd()

    check_file_integrity(folder_path)
