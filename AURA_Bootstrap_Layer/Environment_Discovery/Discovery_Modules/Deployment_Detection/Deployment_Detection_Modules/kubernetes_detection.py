from pathlib import Path


class KubernetesDetectionModule:

    KUBERNETES_FILES = {
        "deployment.yaml",
        "deployment.yml",
        "service.yaml",
        "service.yml",
        "configmap.yaml",
        "configmap.yml",
        "secret.yaml",
        "secret.yml",
        "ingress.yaml",
        "ingress.yml",
        "statefulset.yaml",
        "statefulset.yml",
        "daemonset.yaml",
        "daemonset.yml",
        "job.yaml",
        "job.yml",
        "cronjob.yaml",
        "cronjob.yml",
        "namespace.yaml",
        "namespace.yml",
        "kustomization.yaml",
        "kustomization.yml",
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Kubernetes_Detector(self):

        detected_files = []

        for file in self.files:

            if file.name.lower() in {
                name.lower()
                for name in self.KUBERNETES_FILES
            }:

                if file.name not in detected_files:
                    detected_files.append(file.name)

        return {
            "kubernetes": bool(detected_files),
            "kubernetes_files": detected_files
        }