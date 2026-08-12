output "vpc_id" {
  description = "Taskly VPC ID"
  value       = aws_vpc.taskly.id
}

output "eks_cluster_name" {
  description = "Taskly EKS cluster name"
  value       = aws_eks_cluster.taskly.name
}

output "eks_cluster_endpoint" {
  description = "Taskly EKS API endpoint"
  value       = aws_eks_cluster.taskly.endpoint
}

output "ecr_repository_url" {
  description = "Taskly ECR repository URL"
  value       = aws_ecr_repository.taskly.repository_url
}

output "rds_endpoint" {
  description = "Taskly PostgreSQL endpoint"
  value       = aws_db_instance.taskly.address
}

output "redis_endpoint" {
  description = "Taskly Redis endpoint"
  value       = aws_elasticache_replication_group.taskly.primary_endpoint_address
}