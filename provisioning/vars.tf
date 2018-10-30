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

// Variables for launching the benchmark
variable "benchmark_resolver_host" {
    description = "This is the target service for benchmarking, by default we test the EBI service"
    default = "identifiers.org"
}

variable "benchmark_resolver_protocol" {
    description = "Whether using HTTP or HTTPS(default)"
    default = "https"
}

variable "benchmark_target_resolver_service_name" {
    description = "The name of the target service for benchmarking, just for reporting purposes"
    default = "ebi"
}

variable "benchmark_request_mode" {
    description = "whether we're talking to an API or not(default)"
    default = "noapi"
}

variable "benchmark_benchmark_origin_name" {
    description = "The name of the benchmark source / origin, i.e. who is running the benchmark, for reporting purposes"
    default = "google_cloud"
}
