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

    def __init__(self, files, technology_data):
        self.files = [Path(file) for file in files]
        self.technology_data = technology_data

    def Version_Detector(self):

        versions = {}

        detected_technologies = self._get_technologies()

        for file in self.files:

            if file.name not in self.VERSION_FILES:
                continue

            try:
                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except OSError:
                continue

            for technology in detected_technologies:

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

        # Language
        language_data = self.technology_data.get(
            "language",
            {}
        )

        primary_language = language_data.get(
            "primary_language"
        )

        if primary_language:
            technologies.append(primary_language)

        # Framework
        framework_data = self.technology_data.get(
            "framework",
            {}
        )

        primary_framework = framework_data.get(
            "primary_framework"
        )

        if primary_framework:
            technologies.append(primary_framework)

        # Runtime
        runtime_data = self.technology_data.get(
            "runtime",
            {}
        )

        primary_runtime = runtime_data.get(
            "primary_runtime"
        )

        if primary_runtime:
            technologies.append(primary_runtime)

        # Database
        database_data = self.technology_data.get(
            "database",
            {}
        )

        primary_database = database_data.get(
            "primary_database"
        )

        if primary_database:
            technologies.append(primary_database)

        return technologies

    def _find_version(self, technology, content, file_name):

        technology_lower = technology.lower()

        # -----------------------------------------
        # Python
        # -----------------------------------------

        if technology_lower == "python":

            if file_name == ".python-version":

                version = content.strip()

                if version:
                    return version

            patterns = [
                r'python_requires\s*=\s*["\']([^"\']+)',
                r'python\s*=\s*["\']([^"\']+)',
                r'python_version\s*=\s*["\']([^"\']+)',
                r'python:([0-9.]+)',
            ]

            return self._search_patterns(
                patterns,
                content
            )

        # -----------------------------------------
        # Node.js
        # -----------------------------------------

        if technology_lower == "node.js":

            if file_name == ".nvmrc":

                version = content.strip()

                if version:
                    return version

            patterns = [
                r'"node"\s*:\s*"([^"]+)"',
                r'node:([0-9.]+)',
            ]

            return self._search_patterns(
                patterns,
                content
            )

        # -----------------------------------------
        # FastAPI
        # -----------------------------------------

        if technology_lower == "fastapi":

            patterns = [
                r'fastapi\s*==\s*([0-9.]+)',
                r'fastapi\s*>=\s*([0-9.]+)',
                r'fastapi\s*<=\s*([0-9.]+)',
                r'"fastapi"\s*:\s*"([^"]+)"',
            ]

            return self._search_patterns(
                patterns,
                content,
                ignore_case=True
            )

        # -----------------------------------------
        # Django
        # -----------------------------------------

        if technology_lower == "django":

            patterns = [
                r'django\s*==\s*([0-9.]+)',
                r'django\s*>=\s*([0-9.]+)',
                r'django\s*<=\s*([0-9.]+)',
                r'"django"\s*:\s*"([^"]+)"',
            ]

            return self._search_patterns(
                patterns,
                content,
                ignore_case=True
            )

        # -----------------------------------------
        # Flask
        # -----------------------------------------

        if technology_lower == "flask":

            patterns = [
                r'flask\s*==\s*([0-9.]+)',
                r'flask\s*>=\s*([0-9.]+)',
                r'"flask"\s*:\s*"([^"]+)"',
            ]

            return self._search_patterns(
                patterns,
                content,
                ignore_case=True
            )

        # -----------------------------------------
        # Generic dependency version
        # -----------------------------------------

        escaped_name = re.escape(technology)

        patterns = [
            rf'{escaped_name}\s*==\s*([0-9.]+)',
            rf'{escaped_name}\s*>=\s*([0-9.]+)',
            rf'"{escaped_name}"\s*:\s*"([^"]+)"',
        ]

        return self._search_patterns(
            patterns,
            content,
            ignore_case=True
        )

    def _search_patterns(
        self,
        patterns,
        content,
        ignore_case=False
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