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

        return {
            "primary_library": (
                detected_libraries[0]
                if detected_libraries
                else None
            ),
            "libraries": detected_libraries,
        }

    def _extract_libraries(self, file_name, content):

        parsers = {
            "requirements.txt": self._parse_requirements,
            "pyproject.toml": self._parse_pyproject,
            "Pipfile": self._parse_pipfile,
            "package.json": self._parse_package_json,
            "pom.xml": self._parse_pom,
            "build.gradle": self._parse_gradle,
            "build.gradle.kts": self._parse_gradle,
            "composer.json": self._parse_composer,
            "Gemfile": self._parse_gemfile,
            "go.mod": self._parse_go_mod,
            "Cargo.toml": self._parse_cargo,
        }

        parser = parsers.get(file_name)

        if not parser:
            return []

        return parser(content)

    # ------------------------------------------
    # Python
    # ------------------------------------------

    def _parse_requirements(self, content):

        libraries = []

        for line in content.splitlines():

            line = line.strip()

            if not line or line.startswith("#"):
                continue

            match = re.match(
                r"^([A-Za-z0-9_.-]+)",
                line
            )

            if match:
                libraries.append(match.group(1))

        return libraries

    def _parse_pyproject(self, content):

        return re.findall(
            r'["\']([A-Za-z0-9_.-]+)',
            content
        )

    def _parse_pipfile(self, content):

        libraries = []
        inside_dependencies = False

        for line in content.splitlines():

            line = line.strip()

            if line == "[packages]":
                inside_dependencies = True
                continue

            if line.startswith("["):
                inside_dependencies = False

            if inside_dependencies:

                match = re.match(
                    r"^([A-Za-z0-9_.-]+)\s*=",
                    line
                )

                if match:
                    libraries.append(match.group(1))

        return libraries

    # ------------------------------------------
    # Node.js
    # ------------------------------------------

    def _parse_package_json(self, content):

        libraries = []

        sections = (
            "dependencies",
            "devDependencies",
            "peerDependencies",
            "optionalDependencies",
        )

        for section in sections:

            pattern = (
                rf'"{section}"\s*:\s*\{{(.*?)\}}'
            )

            match = re.search(
                pattern,
                content,
                re.DOTALL
            )

            if not match:
                continue

            libraries.extend(
                re.findall(
                    r'"([^"]+)"\s*:',
                    match.group(1)
                )
            )

        return libraries

    # ------------------------------------------
    # Java - Maven
    # ------------------------------------------

    def _parse_pom(self, content):

        return re.findall(
            r"<artifactId>\s*([^<]+)\s*</artifactId>",
            content
        )

    # ------------------------------------------
    # Java - Gradle
    # ------------------------------------------

    def _parse_gradle(self, content):

        libraries = []

        pattern = (
            r"(?:implementation|api|compileOnly|runtimeOnly)"
            r"\s*[('\"]([^'\"]+)"
        )

        matches = re.findall(
            pattern,
            content
        )

        for dependency in matches:

            parts = dependency.split(":")

            if len(parts) >= 2:
                libraries.append(parts[-2])
            else:
                libraries.append(parts[0])

        return libraries

    # ------------------------------------------
    # PHP
    # ------------------------------------------

    def _parse_composer(self, content):

        return re.findall(
            r'"([^"]+)"\s*:\s*"[^"]+"',
            content
        )

    # ------------------------------------------
    # Ruby
    # ------------------------------------------

    def _parse_gemfile(self, content):

        return re.findall(
            r'gem\s+["\']([^"\']+)',
            content
        )

    # ------------------------------------------
    # Go
    # ------------------------------------------

    def _parse_go_mod(self, content):

        libraries = []

        inside_require = False

        for line in content.splitlines():

            line = line.strip()

            if line.startswith("require ("):
                inside_require = True
                continue

            if inside_require and line == ")":
                inside_require = False
                continue

            if inside_require:

                match = re.match(
                    r"^([A-Za-z0-9_.\-/]+)",
                    line
                )

                if match:
                    libraries.append(match.group(1))

            elif line.startswith("require "):

                match = re.match(
                    r"^require\s+([A-Za-z0-9_.\-/]+)",
                    line
                )

                if match:
                    libraries.append(match.group(1))

        return libraries

    # ------------------------------------------
    # Rust
    # ------------------------------------------

    def _parse_cargo(self, content):

        libraries = []
        inside_dependencies = False

        for line in content.splitlines():

            line = line.strip()

            if line == "[dependencies]":
                inside_dependencies = True
                continue

            if line.startswith("["):
                inside_dependencies = False

            if inside_dependencies:

                match = re.match(
                    r"^([A-Za-z0-9_-]+)\s*=",
                    line
                )

                if match:
                    libraries.append(match.group(1))

        return libraries