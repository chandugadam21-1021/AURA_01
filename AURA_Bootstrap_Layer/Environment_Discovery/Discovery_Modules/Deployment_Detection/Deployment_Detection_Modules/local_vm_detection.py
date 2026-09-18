from pathlib import Path


class LocalVMDetectionModule:

    VM_INDICATORS = {
        "vagrantfile",
        "vmware",
        "virtualbox",
        "hyperv",
        "hyper-v",
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Local_VM_Detector(self, docker_data=None, kubernetes_data=None):

        if docker_data and docker_data.get("docker"):
            return self._environment_result(
                local_vm=False,
                environment="Container"
            )

        if kubernetes_data and kubernetes_data.get("kubernetes"):
            return self._environment_result(
                local_vm=False,
                environment="Kubernetes"
            )

        if self._has_vm_indicator():
            return self._environment_result(
                local_vm=True,
                environment="Virtual Machine"
            )

        return self._environment_result(
            local_vm=True,
            environment="Local/Virtual Machine"
        )

    def _has_vm_indicator(self):
        return any(
            file.name.lower() in self.VM_INDICATORS
            for file in self.files
        )

    @staticmethod
    def _environment_result(local_vm, environment):
        return {
            "local_vm": local_vm,
            "environment": environment,
        }