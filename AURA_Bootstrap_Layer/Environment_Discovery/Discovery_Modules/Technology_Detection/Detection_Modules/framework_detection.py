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

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Framework_Detector(self):

        detected_frameworks = []

        for file in self.files:

            file_name = file.name.lower()

            if file_name in {
                "requirements.txt",
                "pyproject.toml",
                "package.json",
                "pom.xml",
                "build.gradle"
            }:

                try:
                    content = file.read_text(
                        encoding="utf-8",
                        errors="ignore"
                    ).lower()

                except OSError:
                    continue

                for dependency, framework in self.FRAMEWORK_DEPENDENCIES.items():

                    if dependency in content:

                        if framework not in detected_frameworks:
                            detected_frameworks.append(framework)

        if not detected_frameworks:

            return {
                "primary_framework": None,
                "frameworks": []
            }

        return {
            "primary_framework": detected_frameworks[0],
            "frameworks": detected_frameworks
        }