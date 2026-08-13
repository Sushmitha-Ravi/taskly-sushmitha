variable "aws_region" {
  description = "AWS region for Taskly infrastructure"
  type        = string
  default     = "us-east-1"
}
variable "project_name" {
  description = "Unique project name used for AWS resource naming"
  type        = string
  default     = "taskly-sushmitha"
}
