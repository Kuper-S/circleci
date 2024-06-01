#variable.tf

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
