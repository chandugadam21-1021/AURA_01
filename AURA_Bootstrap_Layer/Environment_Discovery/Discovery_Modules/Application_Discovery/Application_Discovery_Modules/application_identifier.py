from pathlib import Path


class ApplicationIdentifier:

    ENTRY_POINTS = {
        "main.py",
        "app.py",
        "server.py",
        "index.js",
        "server.js",
        "main.js",
        "Main.java",
        "Application.java",
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def identify(self):

        return {
            "application_name": self._application_name(),
            "application_type": self._application_type(),
            "entry_point": self._entry_point(),
        }

    def _application_name(self):

        if not self.files:
            return "Unknown"

        return self.files[0].parents[-1].name

    def _entry_point(self):

        for file in self.files:

            if file.name in self.ENTRY_POINTS:
                return str(file)

        return None

    def _application_type(self):

        file_names = {
            file.name.lower()
            for file in self.files
        }

        # Web application indicators
        web_files = {
            "package.json",
            "requirements.txt",
            "pyproject.toml",
            "pom.xml",
            "build.gradle",
        }

        if file_names.intersection(web_files):
            return "Web Application"

        # CLI indicators
        cli_files = {
            "cli.py",
            "main.py",
        }

        if file_names.intersection(cli_files):
            return "CLI Application"

        return "Unknown"