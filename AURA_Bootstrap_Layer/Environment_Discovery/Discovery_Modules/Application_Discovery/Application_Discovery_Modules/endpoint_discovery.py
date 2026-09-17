import re
from pathlib import Path


class EndpointDiscovery:

    def __init__(self, files):

        self.files = [Path(file) for file in files]

    def discover(self):

        endpoints = []

        for file in self.files:

            if file.suffix.lower() != ".py":
                continue

            endpoints.extend(
                self._scan_python_file(file)
            )

        return endpoints

    def _scan_python_file(self, file):

        endpoints = []

        try:

            content = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )

        except OSError:

            return endpoints

        # FastAPI
        fastapi_pattern = (
            r'@\w+\.(get|post|put|patch|delete|options|head)'
            r'\(\s*["\']([^"\']+)'
        )

        for match in re.finditer(
            fastapi_pattern,
            content
        ):

            method = match.group(1).upper()
            path = match.group(2)

            endpoints.append({
                "method": method,
                "path": path,
                "source": str(file),
            })

        # Flask
        flask_pattern = (
            r'@app\.route\('
            r'\s*["\']([^"\']+)'
        )

        for match in re.finditer(
            flask_pattern,
            content
        ):

            path = match.group(1)

            endpoints.append({
                "method": "UNKNOWN",
                "path": path,
                "source": str(file),
            })

        return endpoints