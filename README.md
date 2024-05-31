# Weather App CircleCI CI/CD Pipeline 

## Introduction
This project demonstrates a CI/CD pipeline using CircleCI to build, test, and deploy a Dockerized Weather App to an EKS cluster. The pipeline includes Terraform for infrastructure management, Terratest for infrastructure testing, and Checkov for security compliance checks. The application is deployed to the EKS cluster using ArgoCD.

## Prerequisites
- Docker
- GitLab account
- CircleCI account
- AWS account with IAM permissions to create EKS and related resources
- Familiar with Terraform 
- Familiar with ArgoCD 


## CircleCI Configuration
The CircleCI configuration is defined in `.circleci/config.yml`. It includes jobs for building Docker images, running tests, creating infrastructure with Terraform, validating infrastructure with Terratest and Checkov, and deploying the application using ArgoCD.
