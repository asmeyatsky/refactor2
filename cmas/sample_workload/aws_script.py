import boto3

def upload_to_s3(bucket_name, file_name, object_name=None):
    """Upload a file to an S3 bucket"""
    if object_name is None:
        object_name = file_name

    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket_name, object_name)
    except Exception as e:
        print(e)
        return False
    return True

if __name__ == "__main__":
    # This is just a sample, won't actually run without creds
    print("Starting S3 upload...")
    upload_to_s3("my-bucket", "test.txt")
    print("Upload complete.")
