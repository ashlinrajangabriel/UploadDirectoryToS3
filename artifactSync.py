import os
import json
import boto3
from pathlib import Path
import hashlib
from datetime import datetime

class S3Sync:
    def __init__(self, bucket, key_prefix, log_file_key, username):
        self.s3 = boto3.client('s3')
        self.bucket = bucket
        self.key_prefix = key_prefix
        self.log_file_key = log_file_key
        self.username = username
        self.excluded_extensions = {'.csv', '.xlsx', '.xls', '.parquet'}

    def upload_directory(self, local_directory):
        log_entries = []
        for root, dirs, files in os.walk(local_directory):
            for filename in files:
                if not self._should_exclude_file(filename):
                    local_path = os.path.join(root, filename)
                    relative_path = os.path.relpath(local_path, local_directory)
                    s3_path = os.path.join(self.key_prefix, relative_path)
                    file_hash = self._calculate_file_md5(local_path)

                    print(f"Uploading {s3_path} to {self.bucket}")
                    self.s3.upload_file(local_path, self.bucket, s3_path)

                    log_entry = f"{datetime.now()}, {self.username}, {filename}, {local_path}, {file_hash}\n"
                    log_entries.append(log_entry)
        self._write_log_to_s3(log_entries)


    def _calculate_file_md5(self, filename):
        hash_md5 = hashlib.md5()
        with open(filename, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()

    def _write_log_to_s3(self, log_entries):
        if log_entries:
            log_content = ''.join(log_entries)
            self.s3.put_object(Body=log_content, Bucket=self.bucket, Key=self.log_file_key)


    def download_directory(self, bucket, key, local_directory):
        paginator = self.s3.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket, Prefix=key):
            for obj in page.get('Contents', []):
                target = os.path.join(local_directory, os.path.relpath(obj['Key'], key))
                self._make_dirs_for_file(target)
                self.s3.download_file(bucket, obj['Key'], target)

    def _should_exclude_file(self, filename):
        extension = Path(filename).suffix
        return extension in self.excluded_extensions

    @staticmethod
    def _make_dirs_for_file(path):
        if not os.path.exists(os.path.dirname(path)):
            os.makedirs(os.path.dirname(path))

def clear_notebook_outputs(notebook_path):
    with open(notebook_path, 'r', encoding='utf-8') as file:
        notebook = json.load(file)

    if 'cells' in notebook:
        for cell in notebook['cells']:
            if cell['cell_type'] == 'code':
                cell['outputs'] = []
                cell['execution_count'] = None

    with open(notebook_path, 'w', encoding='utf-8') as file:
        json.dump(notebook, file, ensure_ascii=False, indent=2)

def clear_outputs_in_directory(directory):
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.ipynb'):
                notebook_path = os.path.join(root, file)
                print(f"Clearing outputs from: {notebook_path}")
                clear_notebook_outputs(notebook_path)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 6:
        print("Usage: python script.py <action> <username> <local_directory> <s3_bucket> <s3_key>")
        sys.exit(1)

    action, username, local_directory, bucket, key = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
    log_file_key = 'upload_log.txt'

    sync = S3Sync(bucket, key, log_file_key, username)

    if action == 'upload':
        clear_outputs_in_directory(local_directory)
        sync.upload_directory(local_directory)
    elif action == 'download':
        sync.download_directory(bucket, key, local_directory)
    else:
        print("Invalid action. Use 'upload' or 'download'.")
