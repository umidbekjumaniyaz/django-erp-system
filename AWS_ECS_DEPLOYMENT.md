# AWS ECS/Fargate Deployment Guide

## Prerequisites

1. AWS Account with appropriate permissions
2. Docker installed locally
3. AWS CLI installed and configured
4. AWS ECR repository for your Docker images

## Step-by-Step Deployment

### 1. Create ECR Repository

```bash
# Create ECR repository
aws ecr create-repository --repository-name django-erp-system --region us-east-1

# Get login token and login to ECR
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com
```

### 2. Build and Push Docker Image

```bash
# Build Docker image
docker build -t django-erp-system .

# Tag image for ECR
docker tag django-erp-system:latest YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/django-erp-system:latest

# Push to ECR
docker push YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/django-erp-system:latest
```

### 3. Create ECS Cluster

```bash
# Create ECS cluster
aws ecs create-cluster --cluster-name django-erp-cluster --capacity-providers FARGATE --default-capacity-provider-strategy capacityProvider=FARGATE,weight=1
```

### 4. Create IAM Roles

#### ECS Task Execution Role
```bash
# Create trust policy
cat > ecs-task-execution-trust-policy.json << EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ecs-tasks.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create role
aws iam create-role --role-name ecsTaskExecutionRole --assume-role-policy-document file://ecs-task-execution-trust-policy.json

# Attach policy
aws iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy
```

### 5. Store Secrets in AWS Secrets Manager

```bash
# Store Django secret key
aws secretsmanager create-secret --name "django-erp/SECRET_KEY" --secret-string "your-very-secret-key-here"

# Store database URL
aws secretsmanager create-secret --name "django-erp/DATABASE_URL" --secret-string "your-database-url-here"
```

### 6. Create RDS Database (Optional)

```bash
# Create DB subnet group
aws rds create-db-subnet-group --db-subnet-group-name django-erp-db-subnet --db-subnet-group-description "Subnet group for Django ERP" --subnet-ids subnet-12345678 subnet-87654321

# Create PostgreSQL database
aws rds create-db-instance \
  --db-instance-identifier django-erp-db \
  --db-instance-class db.t3.micro \
  --engine postgres \
  --master-username admin \
  --master-user-password your-secure-password \
  --allocated-storage 20 \
  --db-subnet-group-name django-erp-db-subnet \
  --vpc-security-group-ids sg-12345678
```

### 7. Update Task Definition

Edit `aws-task-definition.json` and replace:
- `YOUR_ACCOUNT_ID` with your AWS account ID
- `YOUR_REGION` with your AWS region
- Update the image URI
- Update ARN values

### 8. Register Task Definition

```bash
aws ecs register-task-definition --cli-input-json file://aws-task-definition.json
```

### 9. Create ECS Service

```bash
# Create service
aws ecs create-service \
  --cluster django-erp-cluster \
  --service-name django-erp-service \
  --task-definition django-erp-system:1 \
  --desired-count 1 \
  --launch-type FARGATE \
  --network-configuration "awsvpcConfiguration={subnets=[subnet-12345678,subnet-87654321],securityGroups=[sg-12345678],assignPublicIp=ENABLED}"
```

### 10. Create Application Load Balancer

```bash
# Create ALB
aws elbv2 create-load-balancer \
  --name django-erp-alb \
  --subnets subnet-12345678 subnet-87654321 \
  --security-groups sg-12345678

# Create target group
aws elbv2 create-target-group \
  --name django-erp-targets \
  --protocol HTTP \
  --port 8000 \
  --vpc-id vpc-12345678 \
  --target-type ip \
  --health-check-path /

# Create listener
aws elbv2 create-listener \
  --load-balancer-arn arn:aws:elasticloadbalancing:us-east-1:123456789012:loadbalancer/app/django-erp-alb/50dc6c495c0c9188 \
  --protocol HTTP \
  --port 80 \
  --default-actions Type=forward,TargetGroupArn=arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/django-erp-targets/73e2d6bc24d8a067
```

### 11. Update ECS Service with Load Balancer

```bash
aws ecs update-service \
  --cluster django-erp-cluster \
  --service django-erp-service \
  --load-balancers targetGroupArn=arn:aws:elasticloadbalancing:us-east-1:123456789012:targetgroup/django-erp-targets/73e2d6bc24d8a067,containerName=django-erp-container,containerPort=8000
```

## Monitoring and Logging

### CloudWatch Logs
```bash
# Create log group
aws logs create-log-group --log-group-name /ecs/django-erp-system
```

### CloudWatch Metrics
- CPU utilization
- Memory utilization
- Request count
- Response time

## Auto Scaling

```bash
# Create auto scaling target
aws application-autoscaling register-scalable-target \
  --service-namespace ecs \
  --resource-id service/django-erp-cluster/django-erp-service \
  --scalable-dimension ecs:service:DesiredCount \
  --min-capacity 1 \
  --max-capacity 10

# Create scaling policy
aws application-autoscaling put-scaling-policy \
  --policy-name django-erp-scaling-policy \
  --service-namespace ecs \
  --resource-id service/django-erp-cluster/django-erp-service \
  --scalable-dimension ecs:service:DesiredCount \
  --policy-type TargetTrackingScaling \
  --target-tracking-scaling-policy-configuration '{"TargetValue":70,"PredefinedMetricSpecification":{"PredefinedMetricType":"ECSServiceAverageCPUUtilization"}}'
```

## Security Best Practices

1. **VPC**: Deploy in private subnets with NAT Gateway
2. **Security Groups**: Restrict access to necessary ports only
3. **IAM**: Use least privilege principle
4. **Secrets**: Use AWS Secrets Manager or Parameter Store
5. **SSL**: Use ACM for SSL certificates

## Cost Optimization

1. **Right-sizing**: Choose appropriate CPU/memory allocation
2. **Auto Scaling**: Scale based on demand
3. **Spot Instances**: Consider Fargate Spot for cost savings
4. **Reserved Capacity**: For predictable workloads

## Useful Commands

```bash
# View service status
aws ecs describe-services --cluster django-erp-cluster --services django-erp-service

# View task logs
aws logs tail /ecs/django-erp-system --follow

# Update service
aws ecs update-service --cluster django-erp-cluster --service django-erp-service --force-new-deployment

# Scale service
aws ecs update-service --cluster django-erp-cluster --service django-erp-service --desired-count 3
```
