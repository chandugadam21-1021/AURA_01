from pathlib import Path


class RuntimeDetectionModule:

    RUNTIME_INDICATORS = {
        # Python
        "requirements.txt": "Python",
        "pyproject.toml": "Python",
        "Pipfile": "Python",
        "manage.py": "Python",

        # JavaScript / TypeScript
        "package.json": "Node.js",
        "package-lock.json": "Node.js",
        "yarn.lock": "Node.js",
        "pnpm-lock.yaml": "Node.js",

        # Java
        "pom.xml": "JVM",
        "build.gradle": "JVM",
        "build.gradle.kts": "JVM",

        # C#
        "*.csproj": ".NET",
        "*.sln": ".NET",

        # PHP
        "composer.json": "PHP",

        # Ruby
        "Gemfile": "Ruby",

        # Go
        "go.mod": "Go",

        # Rust
        "Cargo.toml": "Rust",
    }

    EXACT_INDICATORS = {
        name.lower(): runtime
        for name, runtime in RUNTIME_INDICATORS.items()
        if not name.startswith("*")
    }

    EXTENSION_INDICATORS = {
        name[1:].lower(): runtime
        for name, runtime in RUNTIME_INDICATORS.items()
        if name.startswith("*")
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Runtime_Detector(self):

        detected_runtimes = {
            runtime
            for file in self.files
            if (runtime := self._detect_runtime(file.name))
        }

        runtimes = sorted(detected_runtimes)

        return {
            "primary_runtime": runtimes[0] if runtimes else None,
            "runtimes": runtimes,
        }

    def _detect_runtime(self, file_name):

        file_name = file_name.lower()

        # Exact filename
        if file_name in self.EXACT_INDICATORS:
            return self.EXACT_INDICATORS[file_name]

        # Extension-based indicator
        for extension, runtime in self.EXTENSION_INDICATORS.items():
            if file_name.endswith(extension):
                return runtime

        return None