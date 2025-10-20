terraform {
  required_version = ">= 1.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

# Intentional security issue: S3 bucket without encryption
resource "aws_s3_bucket" "app_bucket" {
  bucket = "my-app-bucket-${random_id.bucket_suffix.hex}"
  
  tags = {
    Name        = "App Bucket"
    Environment = "Dev"
  }
}

# Intentional security issue: Public S3 bucket
resource "aws_s3_bucket_public_access_block" "app_bucket" {
  bucket = aws_s3_bucket.app_bucket.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "random_id" "bucket_suffix" {
  byte_length = 8
}

# Intentional security issue: Security group with open ingress
resource "aws_security_group" "app_sg" {
  name        = "app-security-group"
  description = "Security group for application"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # Open to world - security issue!
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}  