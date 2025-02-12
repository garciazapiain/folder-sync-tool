import os
import shutil
import hashlib
import time
import argparse
from datetime import datetime

def ensure_source_folder_exists(source):
    """Check if the source folder exists; if not, prompt the user to create it."""
    while not os.path.exists(source):
        print(f"Error: Source folder '{source}' does not exist.")
        user_input = input("Would you like to create it? (y/n): ").strip().lower()

        if user_input == 'y':
            os.makedirs(source)
            print(f"Source folder '{source}' has been created. Starting synchronization...")
        else:
            print("Exiting. Please create the source folder and run the script again.")
            exit(1)  # Exit with an error code

def get_file_checksum(file_path):
    """Calculate the MD5 checksum of a file."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        while chunk := f.read(4096):
            hasher.update(chunk)
    return hasher.hexdigest()

def sync_folders(source, replica, log_file):
    """Synchronize the replica folder to match the source folder exactly."""

    with open(log_file, 'a') as log:
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log.write(f"\n[{timestamp}] Starting synchronization...\n")
        print(f"\n[{timestamp}] Starting synchronization...")
        
        # Ensure the replica directory exists
        if not os.path.exists(replica):
            os.makedirs(replica)
            log.write(f"Created directory: {replica}\n")
            print(f"Created directory: {replica}")
        
        # Synchronize files and directories
        for root, dirs, files in os.walk(source):
            relative_path = os.path.relpath(root, source)
            replica_root = os.path.join(replica, relative_path)
            
            if not os.path.exists(replica_root):
                os.makedirs(replica_root)
                log.write(f"Created directory: {replica_root}\n")
                print(f"Created directory: {replica_root}")
            
            for file in files:
                source_file = os.path.join(root, file)
                replica_file = os.path.join(replica_root, file)
                
                if not os.path.exists(replica_file) or get_file_checksum(source_file) != get_file_checksum(replica_file):
                    shutil.copy2(source_file, replica_file)
                    log.write(f"Copied file: {source_file} -> {replica_file}\n")
                    print(f"Copied file: {source_file} -> {replica_file}")
        
        # Remove extra files in replica folder
        for root, dirs, files in os.walk(replica, topdown=False):
            relative_path = os.path.relpath(root, replica)
            source_root = os.path.join(source, relative_path)
            
            for file in files:
                replica_file = os.path.join(root, file)
                source_file = os.path.join(source_root, file)
                
                if not os.path.exists(source_file):
                    os.remove(replica_file)
                    log.write(f"Deleted file: {replica_file}\n")
                    print(f"Deleted file: {replica_file}")
            
            if not os.path.exists(source_root):
                shutil.rmtree(root)
                log.write(f"Deleted directory: {root}\n")
                print(f"Deleted directory: {root}")
        
        log.write(f"[{timestamp}] Synchronization completed.\n")
        print(f"[{timestamp}] Synchronization completed.")

        # Ensure the source folder exists before proceeding
        ensure_source_folder_exists(source)

def main():
    parser = argparse.ArgumentParser(description="Folder Synchronization Tool")
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")
    
    args = parser.parse_args()

    # Ensure the source folder exists before proceeding
    ensure_source_folder_exists(args.source)

    try:
        while True:
            sync_folders(args.source, args.replica, args.log_file)
            time.sleep(args.interval)
    except KeyboardInterrupt:
        print("\nSynchronization stopped by user.")

if __name__ == "__main__":
    main()
