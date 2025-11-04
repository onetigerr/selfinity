output "web_app_url" {
  description = "URL of the deployed web application"
  value       = "https://${azurerm_linux_web_app.selfinity_app.default_hostname}"
}

output "postgresql_endpoint" {
  description = "PostgreSQL Flexible Server endpoint (FQDN)"
  value       = azurerm_postgresql_flexible_server.selfinity_pg.fqdn
}

output "postgresql_connection_string" {
  description = "PostgreSQL connection string"
  value       = "postgresql://${azurerm_postgresql_flexible_server.selfinity_pg.administrator_login}:${azurerm_postgresql_flexible_server.selfinity_pg.administrator_password}@${azurerm_postgresql_flexible_server.selfinity_pg.fqdn}:5432/${azurerm_postgresql_flexible_server_database.selfinity_db.name}?sslmode=require"
  sensitive   = true
}

output "storage_account_blob_endpoint" {
  description = "Storage Account Blob Service endpoint"
  value       = azurerm_storage_account.selfinity_storage.primary_blob_endpoint
}

output "key_vault_uri" {
  description = "Key Vault URI"
  value       = azurerm_key_vault.selfinity_kv.vault_uri
}

output "resource_group_name" {
  description = "Name of the resource group"
  value       = azurerm_resource_group.selfinity_rg.name
}

output "app_service_plan_name" {
  description = "Name of the App Service Plan"
  value       = azurerm_service_plan.selfinity_plan.name
}

output "web_app_name" {
  description = "Name of the Web App"
  value       = azurerm_linux_web_app.selfinity_app.name
}

output "storage_account_name" {
  description = "Name of the Storage Account"
  value       = azurerm_storage_account.selfinity_storage.name
}

output "key_vault_name" {
  description = "Name of the Key Vault"
  value       = azurerm_key_vault.selfinity_kv.name
}

output "postgresql_server_name" {
  description = "Name of the PostgreSQL server"
  value       = azurerm_postgresql_flexible_server.selfinity_pg.name
}

output "postgresql_database_name" {
  description = "Name of the PostgreSQL database"
  value       = azurerm_postgresql_flexible_server_database.selfinity_db.name
}

