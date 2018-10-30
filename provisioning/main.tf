// Run Resolution API benchmarks
provider "google" {
    credentials = "${file("${cloud_api_access_file}")}"
    project     = "${working_project}"
    region      = "${working_region}"
}
