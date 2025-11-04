terraform {
  required_version = ">= 1.0"
  
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
}

provider "azurerm" {
  features {}
}

# Resource Group
resource "azurerm_resource_group" "selfinity_rg" {
  name     = var.resource_group_name
  location = var.location

  tags = {
    environment = "selfinity"
    managed_by  = "terraform"
  }
}

# App Service Plan
resource "azurerm_service_plan" "selfinity_plan" {
  name                = var.app_service_plan_name
  resource_group_name = azurerm_resource_group.selfinity_rg.name
  location            = azurerm_resource_group.selfinity_rg.location
  sku_name            = "B1"
  os_type             = "Linux"

  tags = {
    environment = "selfinity"
    managed_by  = "terraform"
  }
}

# PostgreSQL Flexible Server
resource "azurerm_postgresql_flexible_server" "selfinity_pg" {
  name                   = var.pg_server_name
  resource_group_name    = azurerm_resource_group.selfinity_rg.name
  location               = azurerm_resource_group.selfinity_rg.location
  version                = "15"
  delegated_subnet_id    = null
  private_dns_zone_id    = null
  administrator_login    = var.pg_admin_username
  administrator_password = var.pg_admin_password
  zone                   = "1"
  storage_mb             = 32768
  
  sku_name = "B_Standard_B1ms"

  tags = {
    environment = "selfinity"
    managed_by  = "terraform"
  }
}

# PostgreSQL Database
resource "azurerm_postgresql_flexible_server_database" "selfinity_db" {
  name      = var.pg_database_name
  server_id = azurerm_postgresql_flexible_server.selfinity_pg.id
  collation = "en_US.utf8"
  charset   = "utf8"
}

# PostgreSQL Firewall Rule - Allow Azure Services
resource "azurerm_postgresql_flexible_server_firewall_rule" "allow_azure_services" {
  name             = "AllowAzureServices"
  server_id        = azurerm_postgresql_flexible_server.selfinity_pg.id
  start_ip_address = "0.0.0.0"
  end_ip_address   = "0.0.0.0"
}

# Storage Account
resource "azurerm_storage_account" "selfinity_storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.selfinity_rg.name
  location                 = azurerm_resource_group.selfinity_rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  tags = {
    environment = "selfinity"
    managed_by  = "terraform"
  }
}

# Key Vault
resource "azurerm_key_vault" "selfinity_kv" {
  name                = var.key_vault_name
  location            = azurerm_resource_group.selfinity_rg.location
  resource_group_name = azurerm_resource_group.selfinity_rg.name
  tenant_id           = data.azurerm_client_config.current.tenant_id
  sku_name            = "standard"

  soft_delete_retention_days = 7
  purge_protection_enabled   = false

  tags = {
    environment = "selfinity"
    managed_by  = "terraform"
  }
}

# Key Vault Access Policy for Web App
resource "azurerm_key_vault_access_policy" "selfinity_app_access" {
  key_vault_id = azurerm_key_vault.selfinity_kv.id
  tenant_id    = data.azurerm_client_config.current.tenant_id
  object_id    = azurerm_linux_web_app.selfinity_app.identity[0].principal_id

  secret_permissions = [
    "Get",
    "List",
  ]
}

# Key Vault Secret for SECRET_KEY
resource "azurerm_key_vault_secret" "secret_key" {
  name         = "secret-key"
  value        = var.secret_key
  key_vault_id = azurerm_key_vault.selfinity_kv.id

  depends_on = [azurerm_key_vault.selfinity_kv]
}

# Web App (Linux Web App for Containers)
resource "azurerm_linux_web_app" "selfinity_app" {
  name                = var.web_app_name
  resource_group_name = azurerm_resource_group.selfinity_rg.name
  location            = azurerm_service_plan.selfinity_plan.location
  service_plan_id     = azurerm_service_plan.selfinity_plan.id

  site_config {
    always_on = false
    application_stack {
      docker_image_name      = var.docker_image
    }
  }

  app_settings = {
    # Docker configuration for Docker Hub
    DOCKER_REGISTRY_SERVER_URL = "https://index.docker.io/v1"

    # Database URL
    DATABASE_URL = "postgresql://${azurerm_postgresql_flexible_server.selfinity_pg.administrator_login}:${azurerm_postgresql_flexible_server.selfinity_pg.administrator_password}@${azurerm_postgresql_flexible_server.selfinity_pg.fqdn}:5432/${azurerm_postgresql_flexible_server_database.selfinity_db.name}?sslmode=require"

    # Secret Key - Reference from Key Vault
    SECRET_KEY = "@Microsoft.KeyVault(SecretUri=${azurerm_key_vault_secret.secret_key.id})"

    # Storage Account
    AZURE_STORAGE_ACCOUNT_NAME = azurerm_storage_account.selfinity_storage.name
    AZURE_STORAGE_ACCOUNT_KEY  = azurerm_storage_account.selfinity_storage.primary_access_key

    # Key Vault URI
    KEY_VAULT_URI = azurerm_key_vault.selfinity_kv.vault_uri

    # DOCKER_IMAGE
    DOCKER_ENABLE_CI = "true"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = {
    environment = "selfinity"
    managed_by  = "terraform"
  }

  depends_on = [
    azurerm_postgresql_flexible_server_database.selfinity_db,
    azurerm_key_vault_secret.secret_key
  ]
}

# Data source for current client config
data "azurerm_client_config" "current" {}

