import os
import boto3
import logging
import uuid
from botocore.exceptions import ClientError

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class S3Service:
    def __init__(self):
        """Initialize S3 client using environment variables"""
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.bucket_name = os.getenv('S3_BUCKET_NAME')
        
    def upload_file(self, file_data, original_filename, user_id):
        """
        Upload a file to S3 bucket
        
        Args:
            file_data: File-like object
            original_filename: Original filename
            user_id: User ID for organizing files
            
        Returns:
            s3_key: The S3 key where the file was uploaded
        """
        try:
            # Generate unique key
            extension = original_filename.split('.')[-1].lower()
            s3_key = f"uploads/{user_id}/{uuid.uuid4()}.{extension}"
            
            # Upload file
            self.s3_client.upload_fileobj(
                file_data,
                self.bucket_name,
                s3_key
            )
            
            logger.info(f"Successfully uploaded file to {s3_key}")
            
            return s3_key
            
        except ClientError as e:
            logger.error(f"Error uploading file to S3: {str(e)}")
            raise
            
    def download_file(self, s3_key, local_path):
        """
        Download a file from S3 bucket
        
        Args:
            s3_key: S3 key to download
            local_path: Local path to save file
            
        Returns:
            local_path: Path where file was saved
        """
        try:
            self.s3_client.download_file(
                self.bucket_name,
                s3_key,
                local_path
            )
            
            logger.info(f"Successfully downloaded file from {s3_key} to {local_path}")
            
            return local_path
            
        except ClientError as e:
            logger.error(f"Error downloading file from S3: {str(e)}")
            raise
            
    def delete_file(self, s3_key):
        """
        Delete a file from S3 bucket
        
        Args:
            s3_key: S3 key to delete
        """
        try:
            self.s3_client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            
            logger.info(f"Successfully deleted file {s3_key}")
            
        except ClientError as e:
            logger.error(f"Error deleting file from S3: {str(e)}")
            raise 