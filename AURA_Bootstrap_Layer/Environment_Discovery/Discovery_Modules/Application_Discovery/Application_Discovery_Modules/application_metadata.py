from pathlib import Path


class ApplicationMetadata:

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
            1
            for path in self.root_path.rglob("*")
            if path.is_dir()
        )

    def _source_file_count(self):

        source_extensions = {
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

        return sum(
            1
            for file in self.files
            if file.suffix.lower()
            in source_extensions
        )

    def _configuration_files(self):

        configuration_names = {
            "requirements.txt",
            "pyproject.toml",
            "package.json",
            "pom.xml",
            "build.gradle",
            "docker-compose.yml",
            "docker-compose.yaml",
            "Dockerfile",
        }

        return [
            str(file)
            for file in self.files
            if file.name in configuration_names
        ]