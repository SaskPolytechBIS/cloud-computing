# Serverless Image Processing Pipeline

## 📌 Overview
This project implements a serverless image resizing pipeline using AWS services: S3, Lambda, Step Functions, and API Gateway.

## 🧱 Architecture
- **S3**: Stores original and resized images
- **Lambda**: Resizes images to thumbnails using Pillow
- **Step Functions**: Orchestrates the workflow
- **API Gateway**: Triggers the workflow via HTTP

## 🚀 Setup Instructions

### 1. Create S3 Buckets
- `original-images-bucket`
- `resized-images-bucket`

### 2. Deploy Lambda Function
- Runtime: Python 3.9+
- Set environment variable: `RESIZED_BUCKET = resized-images-bucket`
- Attach IAM role with S3 and CloudWatch permissions

### 3. Create Step Functions State Machine
- Use the provided `step_function.json`
- Replace `REGION`, `ACCOUNT_ID`, and Lambda ARN

### 4. Configure API Gateway
- Create a POST endpoint
- Integrate with Step Functions execution

## 🧪 Testing
1. Upload an image to `original-images-bucket`
2. Trigger the API Gateway endpoint
3. Check `resized-images-bucket` for the thumbnail
4. Monitor logs in CloudWatch


