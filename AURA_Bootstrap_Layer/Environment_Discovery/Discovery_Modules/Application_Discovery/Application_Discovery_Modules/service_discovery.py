from pathlib import Path
import re


class ServiceDiscovery:

    COMPOSE_FILES = {
        "docker-compose.yml",
        "docker-compose.yaml",
        "compose.yml",
        "compose.yaml",
    }

    APPLICATION_EXTENSIONS = {
        ".py",
        ".java",
        ".js",
        ".ts",
        ".go",
    }

    IGNORED_DIRECTORIES = {
        "node_modules",
        "__pycache__",
        ".git",
        ".venv",
        "venv",
        "env",
        "build",
        "dist",
        "test",
        "tests",
        "examples",
        "docs",
    }

    COMPOSE_SERVICE_PATTERN = re.compile(
        r"^ {2}([A-Za-z0-9_-]+):\s*$"
    )

    def __init__(self, root_path):
        self.root_path = Path(root_path)

    def discover(self):
        compose_services = self._docker_compose_services()

        # Compose gives stronger evidence of actual services.
        if compose_services:
            return compose_services

        return self._directory_services()

    # ------------------------------------------
    # Docker Compose discovery
    # ------------------------------------------

    def _docker_compose_services(self):
        services = []

        for compose_file in self._compose_files():

            try:
                content = compose_file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )
            except OSError:
                continue

            inside_services = False

            for line in content.splitlines():

                stripped = line.strip()

                if stripped == "services:":
                    inside_services = True
                    continue

                if inside_services:

                    # Leave the services section when
                    # another top-level YAML section begins.
                    if line and not line.startswith(" "):
                        break

                    match = self.COMPOSE_SERVICE_PATTERN.match(line)

                    if match:
                        services.append(match.group(1))

        return list(dict.fromkeys(services))

    def _compose_files(self):
        return [
            self.root_path / name
            for name in self.COMPOSE_FILES
            if (self.root_path / name).is_file()
        ]

    # ------------------------------------------
    # Directory-based discovery
    # ------------------------------------------

    def _directory_services(self):
        services = []

        try:
            directories = self.root_path.iterdir()
        except OSError:
            return services

        for directory in directories:

            if not self._is_candidate_directory(directory):
                continue

            if self._contains_application_files(directory):
                services.append(directory.name)

        return services

    def _is_candidate_directory(self, directory):
        return (
            directory.is_dir()
            and not directory.name.startswith(".")
            and directory.name not in self.IGNORED_DIRECTORIES
        )

    def _contains_application_files(self, directory):
        try:
            return any(
                file.is_file()
                and file.suffix.lower() in self.APPLICATION_EXTENSIONS
                for file in directory.rglob("*")
            )
        except OSError:
            return False