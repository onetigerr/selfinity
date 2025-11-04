variable "location" {
  description = "Azure region for all resources"
  type        = string
  default     = "northeurope"
}

variable "resource_group_name" {
  description = "Name of the Azure resource group"
  type        = string
  default     = "selfinity-rg"
}

variable "app_service_plan_name" {
  description = "Name of the Azure App Service Plan"
  type        = string
  default     = "selfinity-plan"
}

variable "web_app_name" {
  description = "Name of the Azure Web App"
  type        = string
  default     = "selfinity-app"
}

variable "docker_image" {
  description = "Full Docker image reference (e.g., \"<mydockerhub>/selfinity:latest\")"
  type        = string
}

variable "pg_admin_username" {
  description = "PostgreSQL Flexible Server administrator username"
  type        = string
}

variable "pg_admin_password" {
  description = "PostgreSQL Flexible Server administrator password"
  type        = string
  sensitive   = true
}

variable "secret_key" {
  description = "Application secret key for the web app"
  type        = string
  sensitive   = true
}

variable "storage_account_name" {
  description = "Name of the Azure Storage Account"
  type        = string
  default     = "selfinitystorage"
}

variable "key_vault_name" {
  description = "Name of the Azure Key Vault"
  type        = string
  default     = "selfinity-kv"
}

variable "pg_server_name" {
  description = "Name of the PostgreSQL Flexible Server"
  type        = string
  default     = "selfinity-pg"
}

variable "pg_database_name" {
  description = "Name of the PostgreSQL database"
  type        = string
  default     = "selfinitydb"
}
