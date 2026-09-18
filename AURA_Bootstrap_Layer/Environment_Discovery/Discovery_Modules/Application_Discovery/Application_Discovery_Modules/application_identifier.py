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

    WEB_INDICATORS = {
        "package.json",
        "requirements.txt",
        "pyproject.toml",
        "pom.xml",
        "build.gradle",
    }

    CLI_INDICATORS = {
        "cli.py",
        "main.py",
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

        if file_names & self.WEB_INDICATORS:
            return "Web Application"

        if file_names & self.CLI_INDICATORS:
            return "CLI Application"

        return "Unknown"