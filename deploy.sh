#!/bin/bash

set -e

echo "🚀 Deploying User Registration App..."

# Deploy infrastructure
echo "📦 Deploying infrastructure with Terraform..."
cd terraform
terraform init
terraform plan
terraform apply -auto-approve

# Get API Gateway URL
API_URL=$(terraform output -raw api_gateway_url)
S3_BUCKET=$(terraform output -raw s3_bucket_name)

echo "✅ Infrastructure deployed!"
echo "API Gateway URL: $API_URL"
echo "S3 Bucket: $S3_BUCKET"

cd ..

# Build and deploy frontend
echo "🔨 Building React frontend..."
cd frontend

# Create .env file with API URL
echo "REACT_APP_API_URL=$API_URL" > .env

# Install dependencies and build
npm install
npm run build

echo "📤 Uploading frontend to S3..."
aws s3 sync build/ s3://$S3_BUCKET --delete

cd ..

echo "🎉 Deployment complete!"
echo "Frontend URL: http://$(cd terraform && terraform output -raw s3_website_url)"
echo "API URL: $API_URL"