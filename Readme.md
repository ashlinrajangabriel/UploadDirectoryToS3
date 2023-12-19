# AWS S3 Sync Tool

## Overview
The AWS S3 Sync Tool is a Python-based utility designed to facilitate the synchronization of files between a local file system and an AWS S3 bucket. This tool is particularly useful for automating the process of uploading and downloading files to and from S3, making it an essential asset for data management and backup strategies. Key features include:

- **Uploading to S3**: Uploads files from a specified local directory to an S3 bucket, while excluding certain file types like CSV, XLSX, XLS, and Parquet.
- **Clearing Jupyter Notebook Outputs**: Before uploading, the tool clears outputs from Jupyter notebooks to ensure clean version control.
- **Downloading from S3**: Downloads files from an S3 bucket to a local directory, replicating the S3 file structure locally.
- **Logging**: Generates logs for each upload operation, including details such as username, file name, local path, and MD5 hash, and stores them in an S3 log file.

## Requirements
- Python 3.x
- `boto3` library
- AWS credentials configured (either via AWS CLI or environment variables)

## Installation
1. Ensure you have Python and `boto3` installed. If not, `boto3` can be installed using pip:
   ```bash
   pip install boto3

# Usage

## Uploading Files to S3
To upload files from a local directory to an AWS S3 bucket:

```bash
python artifactSync.py upload <username> <local_directory> <s3_bucket> <s3_key_prefix>
```
<username>: Your username, used for logging purposes.
<local_directory>: The path to the local directory containing the files to upload.
<s3_bucket>: The name of the S3 bucket to which files will be uploaded.
<s3_key_prefix>: The S3 key prefix under which files will be stored.

Example:


```bash
python artifactSync.py upload ashlin Experiments/TestDanger sagemaker-eu-west-1-xxxxxx ashlin/code_artifact
```
Downloading Files from S3
To download files from an AWS S3 bucket to a local directory:

```bash

python artifactSync.py download <username> <local_directory> <s3_bucket> <s3_key_prefix>
```
Example:

```bash
python artifactSync.py download ashlin Experiments/TestDanger sagemaker-eu-west-1-xxxxxx ashlin/code_artifact
```
# Logging
The tool logs each upload operation, capturing the username, date and time, file name, local path, and file hash. The log is stored as upload_log.txt in the specified S3 bucket.

# Security and Permissions
Ensure that the AWS credentials used have the necessary permissions for the required S3 actions. It's recommended to test the tool in a controlled environment before using it in production settings.

Note
Always backup important data before performing upload or download operations, as the tool will overwrite existing files in the destination directory.
