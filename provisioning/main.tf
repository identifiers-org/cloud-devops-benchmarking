// Run Resolution API benchmarks
provider "google" {
    credentials = "${file("${var.cloud_api_access_file}")}"
    project     = "${var.working_project}"
    region      = "${var.working_region}"
}

resource "google_compute_address" "static" {
    name = "ipv4-address"
}

data "template_file" "launchscript" {
    template = "${file("launch_benchmark.sh")}"

    vars {
        RESOLVER_HOST = "${var.benchmark_resolver_host}"
        RESOLVER_PROTOCOL = "${var.benchmark_resolver_protocol}"
        TARGET_RESOLVER_SERVICE_NAME = "${var.benchmark_target_resolver_service_name}"
        REQUEST_MODE = "${var.benchmark_request_mode}"
        BENCHMARK_ORIGIN_NAME = "${var.benchmark_benchmark_origin_name}"
    }
}

resource "google_compute_instance" "resolverBenchmarkVM" {
    name = "resolverbenchmarkvm-${var.working_region}"
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
        user-data = "${data.template_file.launchscript.rendered}"
    }

    service_account {
        scopes = ["userinfo-email", "compute-ro", "storage-ro"]
    }
}
