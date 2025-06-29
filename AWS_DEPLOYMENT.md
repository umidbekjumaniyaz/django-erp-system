# AWS Elastic Beanstalk Deployment Guide

## Prerequisites

1. **AWS Account**: Create an AWS account if you don't have one
2. **AWS CLI**: Install and configure AWS CLI
3. **EB CLI**: Install Elastic Beanstalk CLI

## Installation

### Install AWS CLI
```bash
# macOS
brew install awscli

# Or using pip
pip install awscli

# Configure AWS credentials
aws configure
```

### Install EB CLI
```bash
# macOS
brew install aws-elasticbeanstalk

# Or using pip
pip install awsebcli
```

## Deployment Steps

### 1. Initialize Elastic Beanstalk Application
```bash
# Navigate to your project directory
cd /Users/umidbek/Downloads/django-erp-system-main

# Initialize EB application
eb init

# Follow the prompts:
# - Select a default region (e.g., us-east-1)
# - Choose application name: django-erp-system
# - Choose platform: Python
# - Choose platform version: Python 3.11
# - Set up SSH: Yes (recommended)
```

### 2. Create Environment
```bash
# Create and deploy to a new environment
eb create django-erp-prod

# This will:
# - Create an environment named "django-erp-prod"
# - Deploy your application
# - Set up load balancer, auto-scaling, etc.
```

### 3. Set Environment Variables
```bash
# Set required environment variables
eb setenv SECRET_KEY="your-secret-key-here"
eb setenv DEBUG=False
eb setenv DJANGO_ALLOWED_HOSTS="*.elasticbeanstalk.com"
eb setenv DATABASE_URL="your-database-url-if-using-rds"
```

### 4. Deploy Updates
```bash
# Deploy changes
eb deploy

# Open your application in browser
eb open
```

## Environment Variables Setup

Set these environment variables in your EB environment:

```bash
eb setenv SECRET_KEY="your-very-secret-key-here"
eb setenv DEBUG=False
eb setenv DJANGO_ALLOWED_HOSTS="*.elasticbeanstalk.com,yourdomain.com"
eb setenv DATABASE_URL="postgres://user:password@host:port/database"
```

## Optional: RDS Database Setup

### 1. Create RDS PostgreSQL Database
```bash
# This will add a PostgreSQL database to your environment
eb create --database.engine postgres --database.username your_username
```

### 2. Or create RDS separately
- Go to AWS RDS Console
- Create PostgreSQL database
- Note the connection details
- Add DATABASE_URL environment variable

## SSL Certificate (Optional)

### 1. Request SSL Certificate
- Go to AWS Certificate Manager
- Request a certificate for your domain
- Verify domain ownership

### 2. Configure Load Balancer
- Go to EC2 Load Balancers
- Add HTTPS listener
- Select your SSL certificate

## Custom Domain (Optional)

1. **Route 53**: Set up your domain in Route 53
2. **CNAME Record**: Point your domain to EB environment URL
3. **Update ALLOWED_HOSTS**: Add your domain to Django settings

## Monitoring and Logs

```bash
# View logs
eb logs

# View application health
eb health

# SSH into instance
eb ssh
```

## Scaling

```bash
# Scale your application
eb scale 3  # Run 3 instances

# Or configure auto-scaling in EB console
```

## Useful Commands

```bash
# List environments
eb list

# Switch environment
eb use environment-name

# Terminate environment
eb terminate environment-name

# Show environment status
eb status
```

## Troubleshooting

### Common Issues:

1. **Static Files**: Ensure collectstatic runs successfully
2. **Database**: Check DATABASE_URL format
3. **Permissions**: Verify IAM roles and permissions
4. **Dependencies**: Check requirements.txt

### Debug Steps:
```bash
# Check logs
eb logs

# SSH and check manually
eb ssh
sudo tail -f /var/log/eb-docker/containers/eb-current-app/eb-*-stdouterr.log
```

## Cost Optimization

1. **Instance Type**: Use t3.micro for small applications
2. **Auto Scaling**: Set minimum instances to 1
3. **Reserved Instances**: For production workloads
4. **Monitoring**: Use CloudWatch to monitor costs

## Security Best Practices

1. **Environment Variables**: Never commit secrets to code
2. **IAM Roles**: Use least privilege principle
3. **Security Groups**: Restrict access to necessary ports
4. **SSL**: Always use HTTPS in production
5. **Database**: Use RDS with backup enabled

## Backup Strategy

1. **Database**: Enable automated backups in RDS
2. **Code**: Keep code in version control (Git)
3. **Static Files**: Consider S3 for static/media files
