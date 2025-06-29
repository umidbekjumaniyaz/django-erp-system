#!/bin/bash

# AWS Django ERP Deployment Script
# This script helps deploy the Django ERP system to AWS

set -e

echo "🚀 Django ERP System AWS Deployment Script"
echo "=========================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_NAME="django-erp-system"
AWS_REGION="us-east-1"
EB_ENVIRONMENT="django-erp-prod"

# Functions
print_status() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

check_requirements() {
    echo "Checking requirements..."
    
    # Check if AWS CLI is installed
    if ! command -v aws &> /dev/null; then
        print_error "AWS CLI is not installed. Please install it first:"
        echo "  brew install awscli"
        exit 1
    fi
    print_status "AWS CLI is installed"
    
    # Check if EB CLI is installed
    if ! command -v eb &> /dev/null; then
        print_error "EB CLI is not installed. Please install it first:"
        echo "  brew install aws-elasticbeanstalk"
        exit 1
    fi
    print_status "EB CLI is installed"
    
    # Check AWS credentials
    if ! aws sts get-caller-identity &> /dev/null; then
        print_error "AWS credentials not configured. Please run:"
        echo "  aws configure"
        exit 1
    fi
    print_status "AWS credentials are configured"
}

deploy_elastic_beanstalk() {
    echo ""
    echo "🌱 Deploying to AWS Elastic Beanstalk..."
    
    # Check if EB is already initialized
    if [ ! -d ".elasticbeanstalk" ]; then
        print_warning "Initializing Elastic Beanstalk..."
        eb init $PROJECT_NAME --region $AWS_REGION --platform python-3.11
    else
        print_status "Elastic Beanstalk already initialized"
    fi
    
    # Check if environment exists
    if ! eb list | grep -q $EB_ENVIRONMENT; then
        print_warning "Creating new environment: $EB_ENVIRONMENT"
        eb create $EB_ENVIRONMENT --cname ${PROJECT_NAME}-prod
    else
        print_status "Environment $EB_ENVIRONMENT already exists"
    fi
    
    # Set environment variables
    print_status "Setting environment variables..."
    eb setenv DEBUG=False
    eb setenv DJANGO_ALLOWED_HOSTS="*.elasticbeanstalk.com"
    eb setenv SECRET_KEY="$(python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())')"
    
    # Deploy
    print_status "Deploying application..."
    eb deploy $EB_ENVIRONMENT
    
    # Open in browser
    print_status "Opening application in browser..."
    eb open $EB_ENVIRONMENT
    
    print_status "Deployment completed!"
    echo "Your application is now running on AWS Elastic Beanstalk"
}

deploy_docker() {
    echo ""
    echo "🐳 Preparing Docker deployment..."
    
    # Check if Docker is installed
    if ! command -v docker &> /dev/null; then
        print_error "Docker is not installed. Please install Docker first."
        exit 1
    fi
    
    print_status "Building Docker image..."
    docker build -t $PROJECT_NAME .
    
    print_status "Docker image built successfully!"
    echo "To deploy to AWS ECS, follow the guide in AWS_ECS_DEPLOYMENT.md"
}

show_menu() {
    echo ""
    echo "Choose deployment method:"
    echo "1) AWS Elastic Beanstalk (Recommended for beginners)"
    echo "2) Docker preparation (for ECS/Fargate)"
    echo "3) Show deployment guides"
    echo "4) Exit"
    echo ""
    read -p "Enter your choice (1-4): " choice
    
    case $choice in
        1)
            deploy_elastic_beanstalk
            ;;
        2)
            deploy_docker
            ;;
        3)
            echo ""
            echo "📚 Available deployment guides:"
            echo "- AWS_DEPLOYMENT.md - Elastic Beanstalk deployment"
            echo "- AWS_ECS_DEPLOYMENT.md - ECS/Fargate deployment"
            echo ""
            ;;
        4)
            echo "Goodbye!"
            exit 0
            ;;
        *)
            print_error "Invalid choice. Please try again."
            show_menu
            ;;
    esac
}

# Main execution
main() {
    check_requirements
    show_menu
}

# Run main function
main
