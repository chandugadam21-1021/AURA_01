import re
from pathlib import Path


class EndpointDiscovery:

    HTTP_METHODS = (
        "get",
        "post",
        "put",
        "patch",
        "delete",
        "options",
        "head",
    )

    PYTHON_EXTENSIONS = {".py"}

    FASTAPI_PATTERN = re.compile(
        r'@\w+\.(get|post|put|patch|delete|options|head)\s*\(\s*["\']([^"\']+)["\']'
    )

    FLASK_PATTERN = re.compile(
        r'@(?:app|blueprint)\.route\s*\(\s*["\']([^"\']+)["\']'
    )

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def discover(self):
        endpoints = []

        for file in self.files:
            if file.suffix.lower() not in self.PYTHON_EXTENSIONS:
                continue

            endpoints.extend(
                self._scan_python_file(file)
            )

        return endpoints

    def _scan_python_file(self, file):
        try:
            content = file.read_text(
                encoding="utf-8",
                errors="ignore"
            )
        except OSError:
            return []

        endpoints = []

        endpoints.extend(
            self._detect_fastapi(content, file)
        )

        endpoints.extend(
            self._detect_flask(content, file)
        )

        return endpoints

    def _detect_fastapi(self, content, file):
        return [
            {
                "method": match.group(1).upper(),
                "path": match.group(2),
                "source": str(file),
                "framework": "FastAPI",
            }
            for match in self.FASTAPI_PATTERN.finditer(content)
        ]

    def _detect_flask(self, content, file):
        return [
            {
                "method": "UNKNOWN",
                "path": match.group(1),
                "source": str(file),
                "framework": "Flask",
            }
            for match in self.FLASK_PATTERN.finditer(content)
        ]