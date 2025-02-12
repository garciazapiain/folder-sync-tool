# Folder Synchronization Tool

## Description

This Python script synchronizes a replica folder with a source folder, ensuring that the replica always mirrors the source. It performs the following actions:

    - Copies new or modified files from the source to the replica

    - Deletes files in the replica that are no longer present in the source

    - Allows continuous synchronization at a user-defined time interval (seconds)

    - Logs all synchronization activities in console output and in log file

    - User provides file paths for source, replica and log file

    - Ensures the source folder exists before proceeding
         - if it doesn't, it prompts user to create it with yes/no option
         - In case user says no, script stops automatically

    - Creates replica folder automatically when non-existant initially or deleted


## Requirements:

Make sure you have Python 3 installed.

## Installation:

Clone the repository or download the script:

```bash 
git clone https://github.com/garciazapiain/folder-sync-tool.git
```
```bash
cd <repository-folder>
```

## Usage:

Run the script using the following command:

```bash
python3 sync.py <source_folder> <replica_folder> <sync_interval_seconds> <log_file>
```

## Explanation of parameters:

- **`<source_folder>`**: The **absolute or relative path** to the folder that contains the original files.  
  - Example: `~/Desktop/source-folder` or `/home/user/source-folder`

- **`<replica_folder>`**: The **absolute or relative path** to the folder where the synchronization will replicate files from the source.  
  - Example: `~/Desktop/replica-folder` or `/home/user/replica-folder`

- **`<sync_interval_seconds>`**: The **time interval (in seconds)** at which the synchronization process repeats.  
  - Example: `10` (syncs every 10 seconds)

- **`<log_file>`**: The **file path** where logs will be stored, detailing synchronization activities.  
  - Example: `sync_log.txt` (stores logs in the current directory)

## To stop script:

    - Press Ctrl + C