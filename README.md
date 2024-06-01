# Weather App CircleCI CI/CD Pipeline 

## Introduction
**This project demonstrates a CI/CD pipeline using CircleCI to build, test, and deploy a Dockerized Weather App to an EKS cluster. The pipeline includes Terraform for infrastructure management, Terratest for infrastructure testing, and Checkov for security compliance checks. The application is deployed to the EKS cluster using ArgoCD.**

## Prerequisites

Before you begin, ensure you have the following:

1. **AWS Account**: An AWS account with necessary IAM permissions.
2. **AWS CLI**: Installed and configured with access key and secret key.
3. **Terraform**: Installed on your local machine.
4. **CircleCI Account**: A CircleCI account connected to your GitHub repository.
5. **Bridgecrew Account**: To obtain an API key for Checkov.
6. **Go**: Installed for running Terratest.


## CircleCI Configuration
The CircleCI configuration is defined in `.circleci/config.yml`. It includes jobs for building Docker images, running tests, creating infrastructure with Terraform, validating infrastructure with Terratest and Checkov, and deploying the application using ArgoCD.

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/your-repo.git
cd your-repo

### 2. Configure AWS Credentials
Set up your AWS credentials in your environment:
export AWS_ACCESS_KEY_ID=your-access-key-id
export AWS_SECRET_ACCESS_KEY=your-secret-access-key

### 3. Configure CircleCI Environment Variables
Add the following environment variables in your CircleCI project settings:

**AWS_ACCESS_KEY_ID: Your AWS access key ID.
**AWS_SECRET_ACCESS_KEY: Your AWS secret access key.
**BC_API_KEY: Your Bridgecrew API key.
**DISCORD_WEBHOOK: Your Discord webhook URL for notifications.
**GITLAB_REGISTRY: Your GitLab registry URL.
**GITLAB_USER: Your GitLab username.
**GITLAB_TOKEN: Your GitLab token


### 4. Modify variables.tf
Ensure your variables.tf contains the necessary variables:
```sh
variable "region" {
  description = "The AWS region to create resources in."
  type        = string
  default     = "eu-north-1"  # Stockholm region
}

variable "cluster_name" {
  description = "The name of the EKS cluster."
  type        = string
  default     = "my-eks-cluster"
}

variable "node_instance_type" {
  description = "Instance type of the EKS worker nodes."
  type        = string
  default     = "t3.micro"  
}

variable "AWS_ACCESS_KEY_ID" {
  description = "The AWS access key ID."
  type        = string
}

variable "AWS_SECRET_ACCESS_KEY" {
  description = "The AWS secret access key."
  type        = string
}
```

### 5. Setup Terraform :
```sh
cd terraform
terraform init
terraform apply
```

### 6. Run Terratest Locally
```sh
cd test
go test -v 2>&1 | tee test.log
```

### 7. CircleCI Pipeline
The CircleCI pipeline is defined in .circleci/config.yml:

*****************************************
```yaml
version: 2.1

orbs:
  discord: antonioned/discord@0.1.0
  bridgecrew: bridgecrew/bridgecrew@1.0.5
  aws-eks: circleci/aws-eks@1.0.0
  kubernetes: circleci/kubernetes@0.11.1

jobs:
  build_and_test:
    docker:
      - image: cimg/base:2023.03
    steps:
      - checkout
      - setup_remote_docker
      - run: 
          name: Create .env
          command: echo "API_KEY=$API_KEY" > .env
      - run:
          name: "Docker Compose (build & run)"
          command: |
            cd weather-app
            docker-compose up -d
      - run:
          name: Test
          command: docker exec weather-app-app-1 python3 tests/reachability_test.py
      - run:
          name: Gitlab login and push
          command: |
            echo "$GITLAB_TOKEN" | docker login registry.gitlab.com -u $GITLAB_USER --password-stdin
            docker tag weather-app-app registry.gitlab.com/barminz1209/circleci-weather:$(git rev-parse --short HEAD)
            docker push registry.gitlab.com/barminz1209/circleci-weather:$(git rev-parse --short HEAD)
            docker tag weather-app-app registry.gitlab.com/barminz1209/circleci-weather:latest
            docker push registry.gitlab.com/barminz1209/circleci-weather:latest
      - discord/status:
          fail_only: false
          failure_message: "**${CIRCLE_JOB}** failed. - **${CIRCLE_USERNAME}**."
          success_message: "**${CIRCLE_JOB}** Success - **${CIRCLE_USERNAME}**."
          webhook: "$DISCORD_WEBHOOK"
 
  checkov_tests:
    executor: bridgecrew/default
    steps:
      - checkout
      - bridgecrew/scan:
          api-key-variable: BC_API_KEY
          directory: ./terraform
          output: json
          soft-fail: true
      - discord/status:
          fail_only: false
          failure_message: "**${CIRCLE_JOB}** failed. - **${CIRCLE_USERNAME}**."
          success_message: "**${CIRCLE_JOB}** Success - **${CIRCLE_USERNAME}**."
          webhook: "$DISCORD_WEBHOOK"
        
  terratest:
    docker:
      - image: cimg/base:2023.03
    steps:
      - checkout
      - run:
          name: Install Terraform
          command: |
            sudo apt-get update && sudo apt-get install -y gnupg software-properties-common
            wget -O- https://apt.releases.hashicorp.com/gpg | gpg --dearmor | sudo tee /usr/share/keyrings/hashicorp-archive-keyring.gpg > /dev/null
            gpg --no-default-keyring --keyring /usr/share/keyrings/hashicorp-archive-keyring.gpg --fingerprint
            echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] https://apt.releases.hashicorp.com $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/hashicorp.list
            sudo apt update && sudo apt-get install terraform
      - run:
          name: Install Go
          command: sudo apt update && sudo apt install golang-go
      - run:
          name: Install Terratest
          command: |
            cd terraform
            go mod init terratest
            go mod tidy
      - run:
          name: Replace profile with credentials
          command: |
            awk -v "aws_access_key_id=$AWS_ACCESS_KEY_ID" -v "aws_secret_access_key=$AWS_SECRET_ACCESS_KEY" ' \
            BEGIN { FS = OFS = "=" } \
            $1 == "access_key" { $2 = aws_access_key_id } \
            $1 == "secret_key" { $2 = aws_secret_access_key } \
            ' terraform/providers.tf
      - run:
          name: Run Terratest tests
          command: |
            cd terraform/test
            go test -v -timeout 30m
      - discord/status:
          fail_only: false
          failure_message: "**${CIRCLE_JOB}** failed. - **${CIRCLE_USERNAME}**."
          success_message: "**${CIRCLE_JOB}** Success - **${CIRCLE_USERNAME}**."
          webhook: "$DISCORD_WEBHOOK"

workflows:
  build_and_test:
    jobs:
      - build_and_test
      - checkov_tests:
          requires:
            - build_and_test
      - terratest:
          requires:
            - checkov_tests
```
*****************************************

### Usage:
**Running the Pipeline**
**Push your changes to the GitHub repository.**
**The CircleCI pipeline will trigger automatically.**
**Monitor the build process on CircleCI.**
**Successful builds will deploy the application to the EKS cluster.**

### Manual Testing
To manually test the infrastructure:
```sh
cd terraform
terraform apply
cd ../test
go test -v
```

### Cleaning Up
To clean up the resources:
```sh
cd terraform
terraform destroy
```

### Contributing
Feel free to contribute to this project by creating pull requests, submitting issues, or suggesting features.

### License
This project is licensed under the MIT License.

**This `README.md` file provides comprehensive instructions for setting up, using, and maintaining the Terraform configurations and CircleCI pipeline. Adjust the placeholder values and paths as necessary for your specific project setup.**







