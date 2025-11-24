import logging
import boto3
from botocore.exceptions import ClientError
import os

class S3Manager:
    def __init__(self, region_name='us-east-1'):
        """Initialize the S3 client."""
        self.s3_client = boto3.client('s3', region_name=region_name)
        self.region = region_name

    def create_bucket(self, bucket_name):
        """Create an S3 bucket in a specified region."""
        try:
            if self.region == 'us-east-1':
                self.s3_client.create_bucket(Bucket=bucket_name)
            else:
                location = {'LocationConstraint': self.region}
                self.s3_client.create_bucket(Bucket=bucket_name, CreateBucketConfiguration=location)
            
            print(f"✅ Bucket '{bucket_name}' created successfully.")
            return True
        except ClientError as e:
            logging.error(e)
            return False

    def upload_file(self, file_name, bucket, object_name=None):
        """
        Upload a file to an S3 bucket.
        :param file_name: File to upload (local path)
        :param bucket: Bucket to upload to
        :param object_name: S3 object name. If not specified then file_name is used
        """
        # If S3 object_name was not specified, use file_name
        if object_name is None:
            object_name = os.path.basename(file_name)

        try:
            self.s3_client.upload_file(file_name, bucket, object_name)
            print(f"✅ Uploaded '{file_name}' to '{bucket}/{object_name}'")
            return True
        except ClientError as e:
            logging.error(e)
            return False

    def download_file(self, bucket, object_name, file_name):
        """Download a file from S3 to local path."""
        try:
            self.s3_client.download_file(bucket, object_name, file_name)
            print(f"✅ Downloaded '{object_name}' from '{bucket}' to '{file_name}'")
            return True
        except ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("❌ The object does not exist.")
            else:
                logging.error(e)
            return False

    def list_files(self, bucket):
        """List all files (objects) in an S3 bucket."""
        try:
            response = self.s3_client.list_objects_v2(Bucket=bucket)
            
            print(f"\n📂 Files in bucket '{bucket}':")
            if 'Contents' in response:
                for obj in response['Contents']:
                    print(f" - {obj['Key']} (Size: {obj['Size']} bytes)")
            else:
                print(" - Bucket is empty.")
                
        except ClientError as e:
            logging.error(e)

# --- Usage Example ---
if __name__ == "__main__":
    # Configuration
    BUCKET_NAME = "my-unique-bucket-name-12345" # Must be globally unique
    FILE_TO_UPLOAD = "test.txt"
    
    # Create a dummy file for testing
    with open(FILE_TO_UPLOAD, "w") as f:
        f.write("Hello S3!")

    # Initialize Manager
    s3 = S3Manager(region_name='us-east-1')

    # 1. Create Bucket
    s3.create_bucket(BUCKET_NAME)

    # 2. Upload File
    s3.upload_file(FILE_TO_UPLOAD, BUCKET_NAME)

    # 3. List Files
    s3.list_files(BUCKET_NAME)

    # 4. Download File (as a new name)
    s3.download_file(BUCKET_NAME, "test.txt", "downloaded_test.txt")
    
    # Clean up local files
    # os.remove(FILE_TO_UPLOAD)
    # os.remove("downloaded_test.txt")