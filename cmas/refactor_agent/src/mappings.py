from typing import Dict, Tuple

# Mapping structure: AWS Service/Function -> (GCP Service/Function, GCP Import/Resource)

PYTHON_MAPPINGS: Dict[str, Tuple[str, str]] = {
    "boto3.client('s3')": ("storage.Client()", "from google.cloud import storage"),
    "s3.put_object": ("bucket.blob(key).upload_from_string(body)", ""),
    "s3.upload_file": ("bucket.blob(key).upload_from_filename(filename)", ""),
    "s3_client.upload_file": ("bucket.blob(key).upload_from_filename(filename)", ""), # Hack for sample
    "boto3.client('ec2')": ("compute_v1.InstancesClient()", "from google.cloud import compute_v1"),
    # Add more mappings as needed based on PRD
}

TERRAFORM_MAPPINGS: Dict[str, str] = {
    "aws_s3_bucket": "google_storage_bucket",
    "aws_instance": "google_compute_instance",
    "aws_db_instance": "google_sql_database_instance",
    "aws_lambda_function": "google_cloudfunctions_function",
    "aws_sqs_queue": "google_pubsub_topic", # Approximation, SQS is queue, PubSub is topic/sub
}

def get_python_mapping(aws_code_snippet: str) -> Tuple[str, str]:
    """
    Returns the GCP equivalent code and necessary import for a given AWS code snippet.
    This is a simplified lookup for the MVP.
    """
    return PYTHON_MAPPINGS.get(aws_code_snippet, (None, None))

def get_terraform_mapping(aws_resource_type: str) -> str:
    """
    Returns the GCP equivalent resource type for a given AWS resource type.
    """
    return TERRAFORM_MAPPINGS.get(aws_resource_type, None)
