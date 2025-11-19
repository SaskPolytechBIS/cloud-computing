import json
import boto3
from PIL import Image
import io

def lambda_handler(event, context):
    """
    Lambda function that receives:
        event = {
            "bucket": "-original-image-buckets1",
            "key": "Untitled.jpg"
        }
    Resizes the image to 128x128 and saves it to original-image-buckets1.
    Returns {'status': 'success'} or {'status': 'failed'}.
    """
    try:
        # ---- 1. Get input from Step Functions (or API Gateway) ----
        original_bucket = event['bucket']      # e.g. "-original-image-buckets2"
        key = event['key']                    # e.g. "Untitled.jpg"

        s3 = boto3.client('s3')

        # ---- 2. Download the original image ----
        response = s3.get_object(Bucket=original_bucket, Key=key)
        image_data = response['Body'].read()

        # ---- 3. Resize the image (128x128 thumbnail) ----
        image = Image.open(io.BytesIO(image_data))
        resized_image = image.resize((128, 128))

        # Preserve original format, else fallback to JPEG
        img_format = image.format if image.format else 'JPEG'

        # Creates an in-memory file to save the resized image
        buffer = io.BytesIO()
        # Saves the resized image to the buffer using the original format
        resized_image.save(buffer, format=img_format)
        # Resets the pointer to the start of the buffer so S3 can read
        buffer.seek(0)

        # ---- 4. Upload resized image to the destination bucket ----
        resized_bucket = '-resized-image-buckets2'   # <My bucket
        s3.put_object(
            Bucket=resized_bucket,
            Key=key,                     # same filename 
            Body=buffer,
            ContentType=response['ContentType']  # keep original MIME type
        )

        # ---- 5. Return success for Step Functions Choice state ----
        return {'status': 'success'}

    except Exception as e:
        # Log the full error to CloudWatch 
        print(f"Image resize failed: {str(e)}")
        return {'status': 'failed'}
