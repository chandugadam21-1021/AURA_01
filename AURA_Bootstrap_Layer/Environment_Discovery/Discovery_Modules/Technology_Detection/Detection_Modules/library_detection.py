from pathlib import Path
import re


class LibraryDetectionModule:

    LIBRARY_FILES = {
        "requirements.txt",
        "pyproject.toml",
        "Pipfile",
        "package.json",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
        "composer.json",
        "Gemfile",
        "go.mod",
        "Cargo.toml",
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Library_Detector(self):

        detected_libraries = []

        for file in self.files:

            if file.name not in self.LIBRARY_FILES:
                continue

            try:
                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                )

            except OSError:
                continue

            libraries = self._extract_libraries(
                file.name,
                content
            )

            for library in libraries:

                if library not in detected_libraries:
                    detected_libraries.append(library)

        if not detected_libraries:
            return {
                "primary_library": None,
                "libraries": []
            }

        return {
            "primary_library": detected_libraries[0],
            "libraries": detected_libraries
        }

    def _extract_libraries(self, file_name, content):

        libraries = []

        # -----------------------------------------
        # Python - requirements.txt
        # -----------------------------------------

        if file_name == "requirements.txt":

            for line in content.splitlines():

                line = line.strip()

                if not line:
                    continue

                if line.startswith("#"):
                    continue

                match = re.match(
                    r"^([A-Za-z0-9_.-]+)",
                    line
                )

                if match:
                    libraries.append(match.group(1))

        # -----------------------------------------
        # Python - pyproject.toml
        # -----------------------------------------

        elif file_name == "pyproject.toml":

            dependency_section = False

            for line in content.splitlines():

                line = line.strip()

                if "[project]" in line:
                    dependency_section = True

                if "dependencies" in line:
                    dependency_section = True

                if dependency_section:

                    match = re.search(
                        r'["\']([A-Za-z0-9_.-]+)',
                        line
                    )

                    if match:
                        libraries.append(match.group(1))

        # -----------------------------------------
        # Node.js - package.json
        # -----------------------------------------

        elif file_name == "package.json":

            sections = [
                "dependencies",
                "devDependencies"
            ]

            for section in sections:

                pattern = rf'"{section}"\s*:\s*\{{(.*?)\}}'

                matches = re.findall(
                    pattern,
                    content,
                    re.DOTALL
                )

                for match in matches:

                    dependencies = re.findall(
                        r'"([^"]+)"\s*:',
                        match
                    )

                    libraries.extend(dependencies)

        # -----------------------------------------
        # Java - pom.xml
        # -----------------------------------------

        elif file_name == "pom.xml":

            matches = re.findall(
                r"<artifactId>(.*?)</artifactId>",
                content
            )

            libraries.extend(matches)

        # -----------------------------------------
        # Java - Gradle
        # -----------------------------------------

        elif file_name in {
            "build.gradle",
            "build.gradle.kts"
        }:

            matches = re.findall(
                r"(?:implementation|api|compileOnly|runtimeOnly)"
                r"\s*[('\"]([^'\"]+)",
                content
            )

            for dependency in matches:

                parts = dependency.split(":")

                if parts:
                    libraries.append(parts[-2] if len(parts) >= 2 else parts[0])

        # -----------------------------------------
        # PHP - composer.json
        # -----------------------------------------

        elif file_name == "composer.json":

            matches = re.findall(
                r'"([^"]+)"\s*:\s*"[^"]+"',
                content
            )

            libraries.extend(matches)

        # -----------------------------------------
        # Ruby - Gemfile
        # -----------------------------------------

        elif file_name == "Gemfile":

            matches = re.findall(
                r'gem\s+["\']([^"\']+)',
                content
            )

            libraries.extend(matches)

        # -----------------------------------------
        # Go - go.mod
        # -----------------------------------------

        elif file_name == "go.mod":

            matches = re.findall(
                r"^\s*(?:require\s+)?([A-Za-z0-9_.\-/]+)",
                content,
                re.MULTILINE
            )

            libraries.extend(matches)

        # -----------------------------------------
        # Rust - Cargo.toml
        # -----------------------------------------

        elif file_name == "Cargo.toml":

            dependency_section = False

            for line in content.splitlines():

                line = line.strip()

                if line == "[dependencies]":
                    dependency_section = True
                    continue

                if line.startswith("[") and line != "[dependencies]":
                    dependency_section = False

                if dependency_section:

                    match = re.match(
                        r"^([A-Za-z0-9_-]+)\s*=",
                        line
                    )

                    if match:
                        libraries.append(match.group(1))

        return libraries