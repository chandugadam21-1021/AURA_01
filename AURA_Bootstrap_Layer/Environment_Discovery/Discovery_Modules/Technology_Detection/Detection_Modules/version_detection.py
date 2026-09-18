from pathlib import Path
import re


class VersionDetectionModule:

    VERSION_FILES = {
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "package-lock.json",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "Dockerfile",
        ".python-version",
        ".nvmrc",
    }

    VERSION_PATTERNS = {
        "python": (
            r'python_requires\s*=\s*["\']([^"\']+)',
            r'python\s*=\s*["\']([^"\']+)',
            r'python_version\s*=\s*["\']([^"\']+)',
            r'python:([0-9.]+)',
        ),

        "node.js": (
            r'"node"\s*:\s*"([^"]+)"',
            r'node:([0-9.]+)',
        ),

        "fastapi": (
            r'fastapi\s*==\s*([0-9.]+)',
            r'fastapi\s*>=\s*([0-9.]+)',
            r'fastapi\s*<=\s*([0-9.]+)',
            r'"fastapi"\s*:\s*"([^"]+)"',
        ),

        "django": (
            r'django\s*==\s*([0-9.]+)',
            r'django\s*>=\s*([0-9.]+)',
            r'django\s*<=\s*([0-9.]+)',
            r'"django"\s*:\s*"([^"]+)"',
        ),

        "flask": (
            r'flask\s*==\s*([0-9.]+)',
            r'flask\s*>=\s*([0-9.]+)',
            r'flask\s*<=\s*([0-9.]+)',
            r'"flask"\s*:\s*"([^"]+)"',
        ),
    }

    def __init__(self, files, technology_data):
        self.files = [Path(file) for file in files]
        self.technology_data = technology_data

    def Version_Detector(self):

        versions = {}

        technologies = self._get_technologies()

        for file in self.files:

            if file.name.lower() not in {
                name.lower()
                for name in self.VERSION_FILES
            }:
                continue

            try:
                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )
            except OSError:
                continue

            for technology in technologies:

                version = self._find_version(
                    technology,
                    content,
                    file.name
                )

                if version:
                    versions[technology] = version

        return {
            "versions": versions
        }

    def _get_technologies(self):

        technologies = []

        categories = (
            "language",
            "framework",
            "runtime",
            "database",
            "messaging",
        )

        for category in categories:

            data = self.technology_data.get(
                category,
                {}
            )

            technology = data.get(
                self._primary_key(category)
            )

            if technology:
                technologies.append(technology)

        return technologies

    def _primary_key(self, category):

        if category == "language":
            return "primary_language"

        if category == "framework":
            return "primary_framework"

        if category == "runtime":
            return "primary_runtime"

        if category == "database":
            return "primary_database"

        if category == "messaging":
            return "primary_messaging"

        return None

    def _find_version(
        self,
        technology,
        content,
        file_name
    ):

        technology_lower = technology.lower()

        # Python version file
        if (
            technology_lower == "python"
            and file_name.lower() == ".python-version"
        ):
            return self._file_version(content)

        # Node.js version file
        if (
            technology_lower == "node.js"
            and file_name.lower() == ".nvmrc"
        ):
            return self._file_version(content)

        patterns = self.VERSION_PATTERNS.get(
            technology_lower
        )

        if patterns:
            version = self._search_patterns(
                patterns,
                content
            )

            if version:
                return version

        return self._find_generic_version(
            technology,
            content
        )

    def _file_version(self, content):

        version = content.strip()

        return version if version else None

    def _find_generic_version(
        self,
        technology,
        content
    ):

        escaped_name = re.escape(
            technology
        )

        patterns = (
            rf'{escaped_name}\s*==\s*([0-9.]+)',
            rf'{escaped_name}\s*>=\s*([0-9.]+)',
            rf'{escaped_name}\s*<=\s*([0-9.]+)',
            rf'"{escaped_name}"\s*:\s*"([^"]+)"',
        )

        return self._search_patterns(
            patterns,
            content,
            ignore_case=True
        )

    @staticmethod
    def _search_patterns(
        patterns,
        content,
        ignore_case=True
    ):

        flags = re.IGNORECASE if ignore_case else 0

        for pattern in patterns:

            match = re.search(
                pattern,
                content,
                flags
            )

            if match:
                return match.group(1)

        return None