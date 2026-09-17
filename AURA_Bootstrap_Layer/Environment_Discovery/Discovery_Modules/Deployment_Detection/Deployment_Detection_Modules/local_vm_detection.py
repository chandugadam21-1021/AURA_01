from pathlib import Path


class LocalVMDetectionModule:

    VM_INDICATORS = {
        "Vagrantfile",
        "vagrantfile",
        "vmware",
        "virtualbox",
        "hyperv",
        "hyper-v",
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Local_VM_Detector(self, docker_data=None, kubernetes_data=None):

        # -----------------------------------------
        # Check Docker
        # -----------------------------------------

        if docker_data and docker_data.get("docker"):
            return {
                "local_vm": False,
                "environment": "Container"
            }

        # -----------------------------------------
        # Check Kubernetes
        # -----------------------------------------

        if kubernetes_data and kubernetes_data.get("kubernetes"):
            return {
                "local_vm": False,
                "environment": "Kubernetes"
            }

        # -----------------------------------------
        # Check explicit VM indicators
        # -----------------------------------------

        for file in self.files:

            if file.name.lower() in {
                indicator.lower()
                for indicator in self.VM_INDICATORS
            }:
                return {
                    "local/virtual machine": True,
                    "environment": "Virtual Machine",
                }

        # -----------------------------------------
        # No container/orchestrator detected
        # -----------------------------------------

        return {
            "local/virtual machine": True,
            "environment": "Local/Virtual Machine"
        }