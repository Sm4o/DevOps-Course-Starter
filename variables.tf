variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "uksouth"
}

variable "GITHUB_CLIENT_ID" {
  type = string
}

variable "GITHUB_CLIENT_SECRET" {
  type = string
}

variable "SECRET_KEY" {
  type = string
}

variable "DATABASE_NAME" {
  type = string
  default = "terraformed-todo-app-sam-db"
}