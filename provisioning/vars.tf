variable "cloud_api_access_file" {
    description = "File path to access cloud api credentials"
}

variable "working_project" {
    description = "Project where all the operations will be executed, and the infrastructure will belong to"
}

variable "working_region" {
    description = "Cloud Region for the zones where all operations will be performed"
    default = "europe-north1"
}

variable "working_zone" {
    description = "This is the zone where all the operations will be performed"
    default = "europe-north1-a"
}
