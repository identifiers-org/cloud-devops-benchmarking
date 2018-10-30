// Run Resolution API benchmarks
provider "google" {
    credentials = "${file("${var.cloud_api_access_file}")}"
    project     = "${var.working_project}"
    region      = "${var.working_region}"
}

resource "google_compute_address" "static" {
    name = "ipv4-address"
}

resource "google_compute_instance" "resolverBenchmarkVM" {
    name = "resolverbenchmarkvm"
    machine_type = "g1-small"
    zone = "${var.working_zone}"

    tags = ["${var.working_region}", "resolver-benchmark"]

    boot_disk {
        initialize_params {
            image = "debian-cloud/debian-9"
        }
    }

    network_interface {
        network = "default"
        access_config {
            nat_ip = "${google_compute_address.static.address}"
        }
    }

    metadata {
        region = "${var.working_region}"
        app = "resolver-benchmark"
    }

    service_account {
        scopes = ["userinfo-email", "compute-ro", "storage-ro"]
    }
}
