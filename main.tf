terraform {
  required_providers{
    aws = {
      source  = "hashicorp/aws"
      version = "~> 3.0"
    }
  }
}

provider "aws" {
  region = "ap-southeast-2"
}

resource "aws_instance" "chatbot" {
  ami           = "ami-0310483fb2b488153" # Ubuntu 20.04 LTS // us-east-1
  instance_type = "t2.micro"
}

