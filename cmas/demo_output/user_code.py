# [WARNING] Untranslated AWS SDK references detected. Please check mappings.
import boto3
import json

# --- CONFIGURATION ---
REGION = 'YOUR_REGION'  # e.g., 'us-east-1'
ACCOUNT_ID = 'YOUR_ACCOUNT_ID' # e.g., '123456789012'
BUCKET_NAME = 'YOUR_BUCKET_NAME' # Must be globally unique
TOPIC_NAME = 'S3ObjectCreationTopic'
QUEUE_NAME = 'S3ProcessingQueue'

# --- BOTO3 CLIENTS ---
s3_client = boto3.client('s3', region_name=REGION)
sns_client = boto3.client('sns', region_name=REGION)
sqs_client = boto3.client('sqs', region_name=REGION)

# ARNs will be determined after creation
SQS_ARN = f'arn:aws:sqs:{REGION}:{ACCOUNT_ID}:{QUEUE_NAME}'
SNS_ARN = f'arn:aws:sns:{REGION}:{ACCOUNT_ID}:{TOPIC_NAME}'

print("Starting AWS Resource Setup...")

### 1. CREATE SQS QUEUE AND GET URL/ARN ###
# SQS Queue is created first
try:
    sqs_response = sqs_client.create_subscription(name=sqs_client.subscription_path("your-project-id", QUEUE_NAME), topic="projects/your-project-id/topics/my-topic")
    QUEUE_URL = sqs_response['QueueUrl']
    print(f"1. SQS Queue created: {QUEUE_URL}")
except Exception as e:
    print(f"1. SQS Queue creation failed: {e}")

### 2. CREATE SNS TOPIC ###
try:
    sns_response = sns_client.create_topic(request={"name": sns_client.topic_path("my-gcp-project", TOPIC_NAME)})
    TOPIC_ARN = sns_response['TopicArn']
    print(f"2. SNS Topic created: {TOPIC_ARN}")
except Exception as e:
    print(f"2. SNS Topic creation failed: {e}")
    TOPIC_ARN = SNS_ARN # Use placeholder ARN if creation failed

### 3. SET SQS QUEUE POLICY (Allow SNS to publish to SQS) ###
sqs_policy = {
    "Version": "2012-10-17",
    "Id": f"{SQS_ARN}/SQSDefaultPolicy",
    "Statement": [
        {
            "Sid": "AllowSNSPublish",
            "Effect": "Allow",
            "Principal": {"Service": "sns.amazonaws.com"},
            "Action": "sqs:SendMessage",
            "Resource": SQS_ARN,
            "Condition": {"ArnEquals": {"aws:SourceArn": TOPIC_ARN}}
        }
    ]
}

try:
    sqs_client.set_queue_attributes(
        QueueUrl=QUEUE_URL,
        Attributes={'Policy': json.dumps(sqs_policy)}
    )
    print("3. SQS Policy set: Allowed SNS to publish messages.")
except Exception as e:
    print(f"3. Failed to set SQS Policy: {e}")


### 4. SUBSCRIBE SQS QUEUE TO SNS TOPIC ###
try:
    sns_client.subscribe(
        TopicArn=TOPIC_ARN,
        Protocol='sqs',
        Endpoint=SQS_ARN
    )
    print("4. SQS subscribed to SNS Topic.")
except Exception as e:
    print(f"4. Failed to subscribe SQS to SNS: {e}")

### 5. SET SNS TOPIC POLICY (Allow S3 to publish to SNS) ###
sns_policy = {
    "Version": "2012-10-17",
    "Id": "__default_policy_ID",
    "Statement": [
        {
            "Sid": "AllowS3Publish",
            "Effect": "Allow",
            "Principal": {"Service": "s3.amazonaws.com"},
            "Action": "SNS:Publish",
            "Resource": TOPIC_ARN,
            "Condition": {"ArnLike": {"aws:SourceArn": f"arn:aws:s3:::{BUCKET_NAME}"}}
        }
    ]
}

try:
    sns_client.set_topic_attributes(
        TopicArn=TOPIC_ARN,
        AttributeName='Policy',
        AttributeValue=json.dumps(sns_policy)
    )
    print("5. SNS Policy set: Allowed S3 to publish events.")
except Exception as e:
    print(f"5. Failed to set SNS Topic Policy: {e}")

### 6. CONFIGURE S3 EVENT NOTIFICATION ###
# This step links S3 events to the SNS topic
notification_config = {
    'TopicConfigurations': [
        {
            'Id': 'S3ObjectCreatedNotification',
            'TopicArn': TOPIC_ARN,
            'Events': ['s3:ObjectCreated:*'] # Trigger on any object creation
        }
    ]
}

try:
    # Ensure the bucket exists first (uncomment the line below if you need to create it)
    # s3_client.create_bucket(Bucket=BUCKET_NAME, CreateBucketConfiguration={'LocationConstraint': REGION})
    
    s3_client.put_bucket_notification_configuration(
        Bucket=BUCKET_NAME,
        NotificationConfiguration=notification_config
    )
    print("6. S3 Event Notification configured successfully!")
except Exception as e:
    print(f"6. S3 Notification configuration failed. Ensure bucket exists and IAM permissions are correct: {e}")

print("\nSetup complete. You can now upload a file to the S3 bucket to test the flow.")