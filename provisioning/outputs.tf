output "vm-project" {
    value = "${var.working_project}"
}

output "vm-zone" {
    value = "${var.working_zone}"
}

// Machine IP address
output "vm-ip-address" {
    value = "${google_compute_address.static.address}"
}

// Machine ID
output "vm-id" {
    value = "${google_compute_instance.resolverBenchmarkVM.id}"
}
