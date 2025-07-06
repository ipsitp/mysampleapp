# User Registration App

A serverless application for user registration with React frontend, Lambda backend, and DynamoDB storage.

## Architecture

- **Frontend**: React app hosted on S3 with static website hosting
- **API**: HTTP API Gateway with CORS enabled
- **Backend**: Python Lambda function for processing
- **Database**: DynamoDB for user data storage
- **Infrastructure**: Terraform for AWS resource provisioning

## Tech Stack

- **Infrastructure**: Terraform
- **Backend**: Python 3.9 (AWS Lambda)
- **Frontend**: React 18
- **Database**: DynamoDB
- **Hosting**: S3 Static Website + API Gateway

## Database Schema

```json
{
  "Customer_Id": "7-digit number (auto-generated)",
  "First_Name": "String (max 25 chars)",
  "Last_Name": "String (max 25 chars)",
  "Email": "String (max 50 chars)",
  "Phone_Number": "String (max 15 chars)",
  "Address_Ln_1": "String (max 100 chars)",
  "City": "String (max 20 chars)",
  "State": "String (max 15 chars)",
  "Country": "String (max 15 chars)",
  "Start_Date": "ISO Date (auto-generated)"
}
```

## API Endpoints

- `POST /register` - Register a new user
- `GET /users` - Retrieve all registered users

## Prerequisites

- AWS CLI configured with appropriate permissions
- Terraform installed
- Node.js and npm installed

## Deployment

### Quick Deploy

```bash
./deploy.sh
```

### Manual Deploy

1. **Deploy Infrastructure**:
   ```bash
   cd terraform
   terraform init
   terraform apply
   ```

2. **Build and Deploy Frontend**:
   ```bash
   cd frontend
   
   # Get API URL from Terraform output
   API_URL=$(cd ../terraform && terraform output -raw api_gateway_url)
   echo "REACT_APP_API_URL=$API_URL" > .env
   
   # Build and deploy
   npm install
   npm run build
   
   # Upload to S3
   S3_BUCKET=$(cd ../terraform && terraform output -raw s3_bucket_name)
   aws s3 sync build/ s3://$S3_BUCKET --delete
   ```

3. **Get URLs**:
   ```bash
   cd terraform
   echo "Frontend: http://$(terraform output -raw s3_website_url)"
   echo "API: $(terraform output -raw api_gateway_url)"
   ```

## Project Structure

```
mysampleapp/
├── terraform/          # Infrastructure as Code
│   └── main.tf
├── lambda/             # Backend Lambda function
│   └── lambda_function.py
├── frontend/           # React frontend
│   ├── public/
│   ├── src/
│   └── package.json
├── deploy.sh          # Automated deployment script
└── README.md
```

## Features

- Form validation (client and server-side)
- Responsive design
- Error handling
- CORS enabled for cross-origin requests
- Auto-generated customer IDs
- Real-time form feedback

## Cleanup

To destroy all resources:

```bash
cd terraform
terraform destroy
```



