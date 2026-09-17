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

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Runtime_Detector(self):

        detected_runtimes = []

        for file in self.files:

            file_name = file.name

            runtime = self._detect_runtime(file_name)

            if runtime and runtime not in detected_runtimes:
                detected_runtimes.append(runtime)

        if not detected_runtimes:
            return {
                "primary_runtime": None,
                "runtimes": []
            }

        return {
            "primary_runtime": detected_runtimes[0],
            "runtimes": detected_runtimes
        }

    def _detect_runtime(self, file_name):

        for indicator, runtime in self.RUNTIME_INDICATORS.items():

            if indicator.startswith("*"):

                extension = indicator[1:]

                if file_name.endswith(extension):
                    return runtime

            elif file_name.lower() == indicator.lower():

                return runtime

        return None