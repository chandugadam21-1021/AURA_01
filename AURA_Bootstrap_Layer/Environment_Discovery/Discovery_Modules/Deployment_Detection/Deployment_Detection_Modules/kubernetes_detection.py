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

    KUBERNETES_FILES_LOWER = {
        name.lower()
        for name in KUBERNETES_FILES
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Kubernetes_Detector(self):

        detected_files = {
            file.name
            for file in self.files
            if file.name.lower() in self.KUBERNETES_FILES_LOWER
        }

        return {
            "kubernetes": bool(detected_files),
            "kubernetes_files": sorted(detected_files),
        }