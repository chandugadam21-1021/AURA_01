from pathlib import Path
import re


class ServiceDiscovery:

    def __init__(self, root_path):
        self.root_path = Path(root_path)

    def discover(self):

        services = []

        services.extend(self._docker_compose_services())
        services.extend(self._directory_services())

        # Remove duplicates
        services = list(dict.fromkeys(services))

        return services

    # ------------------------------------------
    # Docker Compose
    # ------------------------------------------

    def _docker_compose_services(self):

        services = []

        compose_files = [
            "docker-compose.yml",
            "docker-compose.yaml",
            "compose.yml",
            "compose.yaml",
        ]

        for name in compose_files:

            compose_file = self.root_path / name

            if not compose_file.exists():
                continue

            try:

                content = compose_file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

                inside_services = False

                for line in content.splitlines():

                    if line.strip() == "services:":
                        inside_services = True
                        continue

                    if inside_services:

                        match = re.match(
                            r"^  ([a-zA-Z0-9_-]+):\s*$",
                            line
                        )

                        if match:
                            services.append(match.group(1))

            except OSError:
                pass

        return services

    # ------------------------------------------
    # Directory based discovery
    # ------------------------------------------

    def _directory_services(self):

        services = []

        for directory in self.root_path.iterdir():

            if not directory.is_dir():
                continue

            if directory.name.startswith("."):
                continue

            # Ignore common non-service directories
            if directory.name in {
                "node_modules",
                "__pycache__",
                ".git",
                ".venv",
                "venv",
                "build",
                "dist",
            }:
                continue

            # A directory containing application files
            files = list(directory.rglob("*"))

            has_application_files = any(
                file.is_file()
                and file.suffix.lower() in {
                    ".py",
                    ".java",
                    ".js",
                    ".ts",
                    ".go",
                }
                for file in files
            )

            if has_application_files:
                services.append(directory.name)

        return services