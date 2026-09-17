from .Deployment_Detection_Modules.docker_detection import DockerDetectionModule
from .Deployment_Detection_Modules.kubernetes_detection import KubernetesDetectionModule
from .Deployment_Detection_Modules.local_vm_detection import LocalVMDetectionModule


class DeploymentDetectionModule:

    #docker
    def Detect_Docker(self, files):

        docker_mod = DockerDetectionModule(files) 

        return docker_mod.Docker_Detector()

    #kubernetes
    def Detect_Kubernetes(self, files):

        kubernetes_mod = KubernetesDetectionModule(files)

        return kubernetes_mod.Kubernetes_Detector()

    #loca/vm
    def Detect_Local_VM(self, files):

        local_vm_mod = LocalVMDetectionModule(files)

        return local_vm_mod.Local_VM_Detector()