from pathlib import Path


class DockerDetectionModule:

    DOCKER_FILES = {
        "Dockerfile",
        "docker-compose.yml",
        "docker-compose.yaml",
        "compose.yml",
        "compose.yaml",
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Docker_Detector(self):

        detected_files = {
            file.name
            for file in self.files
            if file.name in self.DOCKER_FILES
        }

        return {
            "docker": bool(detected_files),
            "docker_files": sorted(detected_files),
        }