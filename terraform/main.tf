provider "aws" {
  region = "us-east-1"
}

resource "aws_s3_bucket" "data_bucket" {
  bucket = "your-data-bucket"
}

resource "aws_db_instance" "rds" {
  allocated_storage    = 10
  engine              = "postgres"
  instance_class      = "db.t3.micro"
  identifier          = "your-rds-instance"
  username           = "admin"
  password           = "yourpassword"
  skip_final_snapshot = true
}

resource "aws_ecr_repository" "repo" {
  name = "etl-docker-repo"
}

resource "aws_lambda_function" "etl_lambda" {
  function_name = "etl_lambda"
  image_uri     = "${aws_ecr_repository.repo.repository_url}:latest"
  package_type  = "Image"
  role          = aws_iam_role.lambda_role.arn
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda_execution_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
      Action = "sts:AssumeRole"
    }]
  })
}