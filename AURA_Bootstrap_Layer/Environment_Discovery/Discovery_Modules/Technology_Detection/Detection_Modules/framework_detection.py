from pathlib import Path


class FrameworkDetectionModule:

    FRAMEWORK_DEPENDENCIES = {
        # Python
        "fastapi": "FastAPI",
        "django": "Django",
        "flask": "Flask",
        "tornado": "Tornado",
        "sanic": "Sanic",

        # JavaScript / TypeScript
        "express": "Express",
        "@nestjs/core": "NestJS",
        "next": "Next.js",
        "nuxt": "Nuxt.js",

        # Java
        "spring-boot": "Spring Boot",
        "quarkus": "Quarkus",

        # PHP
        "laravel": "Laravel",
        "symfony": "Symfony",

        # Ruby
        "rails": "Ruby on Rails",

        # C#
        "aspnet": "ASP.NET",
        "microsoft.aspnetcore": "ASP.NET Core",
    }

    FRAMEWORK_FILES = {
        "requirements.txt",
        "pyproject.toml",
        "package.json",
        "pom.xml",
        "build.gradle",
        "build.gradle.kts",
    }

    FRAMEWORK_DEPENDENCIES_LOWER = {
        dependency.lower(): framework
        for dependency, framework in FRAMEWORK_DEPENDENCIES.items()
    }

    FRAMEWORK_FILES_LOWER = {
        file.lower()
        for file in FRAMEWORK_FILES
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Framework_Detector(self):

        detected_frameworks = set()

        for file in self.files:

            if file.name.lower() not in self.FRAMEWORK_FILES_LOWER:
                continue

            try:
                content = file.read_text(
                    encoding="utf-8",
                    errors="ignore"
                ).lower()
            except OSError:
                continue

            for dependency, framework in self.FRAMEWORK_DEPENDENCIES_LOWER.items():

                if dependency in content:
                    detected_frameworks.add(framework)

        frameworks = sorted(detected_frameworks)

        return {
            "primary_framework": frameworks[0] if frameworks else None,
            "frameworks": frameworks,
        }