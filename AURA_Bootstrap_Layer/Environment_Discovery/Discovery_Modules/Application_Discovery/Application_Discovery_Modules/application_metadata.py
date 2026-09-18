from pathlib import Path


class ApplicationMetadata:

    SOURCE_EXTENSIONS = {
        ".py",
        ".java",
        ".js",
        ".jsx",
        ".ts",
        ".tsx",
        ".go",
        ".rs",
        ".c",
        ".cpp",
    }

    CONFIGURATION_FILES = {
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "pom.xml",
        "build.gradle",
        "docker-compose.yml",
        "docker-compose.yaml",
        "Dockerfile",
    }

    def __init__(self, root_path, files):
        self.root_path = Path(root_path)
        self.files = [Path(file) for file in files]

    def collect(self):
        return {
            "root_path": str(self.root_path.resolve()),
            "file_count": len(self.files),
            "directory_count": self._directory_count(),
            "source_file_count": self._source_file_count(),
            "configuration_files": self._configuration_files(),
        }

    def _directory_count(self):
        return sum(
            path.is_dir()
            for path in self.root_path.rglob("*")
        )

    def _source_file_count(self):
        return sum(
            file.suffix.lower() in self.SOURCE_EXTENSIONS
            for file in self.files
        )

    def _configuration_files(self):
        return [
            str(file)
            for file in self.files
            if file.name in self.CONFIGURATION_FILES
        ]