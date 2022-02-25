variable "prefix" {
  description = "The prefix used for all resources in this environment"
}

variable "location" {
  description = "The Azure location where all resources in this deployment should be created"
  default     = "uksouth"
}

variable "GITHUB_CLIENT_ID" {
  type    = string
  default = "627a47faec12864e9953"
}

variable "GITHUB_CLIENT_SECRET" {
  type      = string
  sensitive = true
}

variable "SECRET_KEY" {
  type      = string
  sensitive = true
}

variable "DATABASE_NAME" {
  type    = string
  default = "terraformed-todo-app-sam-db"
}
