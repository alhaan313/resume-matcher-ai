import boto3
import os
from decimal import Decimal  # Import Decimal for DynamoDB

# AWS Credentials & Config
AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = "us-east-1"
S3_BUCKET = "resume-parser-bucket-12345"  # Replace with your bucket name
DYNAMODB_TABLE = "ResumeMetadata"  # Replace with your table name

# Connect to AWS S3
s3 = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)

# Connect to DynamoDB
dynamodb = boto3.resource(
    "dynamodb",
    aws_access_key_id=AWS_ACCESS_KEY,
    aws_secret_access_key=AWS_SECRET_KEY,
    region_name=AWS_REGION
)
table = dynamodb.Table(DYNAMODB_TABLE)

def upload_to_s3(file, unique_filename):
    """Uploads a file to S3 and returns its URL."""
    file.seek(0)
    s3.upload_fileobj(
        file,
        S3_BUCKET,
        unique_filename,
        ExtraArgs={"ContentType": "application/pdf"}
    )
    return f"https://{S3_BUCKET}.s3.amazonaws.com/{unique_filename}"

def store_resume_metadata(resume_id, original_filename, file_url, ats_score):
    """Stores resume metadata in DynamoDB."""
    table.put_item(Item={
        "resume_id": resume_id,
        "original_filename": original_filename,
        "file_url": file_url,
        "ats_score": Decimal(str(ats_score))
    })

def get_resume_by_id(resume_id):
    """Fetches a resume's metadata from DynamoDB."""
    response = table.get_item(Key={"resume_id": resume_id})
    return response.get("Item")

def get_all_resumes():
    """Fetches all stored resume metadata from DynamoDB."""
    response = table.scan()
    return response.get("Items", [])
