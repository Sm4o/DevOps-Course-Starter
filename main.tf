terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }

  backend "azurerm" {
    resource_group_name  = "OpenCohort1_SamuilPetrov_ProjectExercise"
    storage_account_name = "tfstate14862"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "OpenCohort1_SamuilPetrov_ProjectExercise"
}


resource "azurerm_app_service_plan" "main" {
  name                = "${var.prefix}-terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true

  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_app_service" "main" {
  name                = "${var.prefix}-terraformed-todo-app-sam"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id

  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|sm4o/todo.app:latest"
  }

  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "DB_CONNECTION"              = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255/DefaultDatabase?ssl=true&replicaSet=globaldb&retrywrites=false&maxIdleTimeMS=120000"
    "DATABASE_NAME"              = "${var.DATABASE_NAME}"
    "FLASK_APP"                  = "todo_app/app"
    "FLASK_ENV"                  = "production"
    "SECRET_KEY"                 = "${var.SECRET_KEY}"
    "GITHUB_CLIENT_ID"           = "${var.GITHUB_CLIENT_ID}"
    "GITHUB_CLIENT_SECRET"       = "${var.GITHUB_CLIENT_SECRET}"
    "LOG_LEVEL"                  = "${var.LOG_LEVEL}"
    "LOGGLY_TOKEN"               = "${var.LOGGLY_TOKEN}"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "todoapp-cosmosdb-account"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  offer_type          = "Standard"
  kind                = "MongoDB"

  capabilities {
    name = "MongoDBv3.4"
  }

  capabilities {
    name = "EnableMongo"
  }

  capabilities {
    name = "EnableServerless"
  }

  consistency_policy {
    consistency_level       = "BoundedStaleness"
    max_interval_in_seconds = 300
    max_staleness_prefix    = 100000
  }

  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = var.DATABASE_NAME
  account_name        = azurerm_cosmosdb_account.main.name
  resource_group_name = data.azurerm_resource_group.main.name
  lifecycle {
    prevent_destroy = true
  }
}
