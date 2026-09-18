from pathlib import Path


class FileFilter:

    IGNORED_DIRECTORIES = {
        "__pycache__",
        "node_modules",
        ".git",
        ".venv",
        "venv",
        "target",
        "build",
        "dist",
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def filter(self):

        return [
            file
            for file in self.files
            if self._is_valid(file)
        ]

    def _is_valid(self, file):

        # Ignore hidden files
        if file.name.startswith("."):
            return False

        # Ignore files inside unnecessary directories
        if any(
            directory in file.parts
            for directory in self.IGNORED_DIRECTORIES
        ):
            return False

        return True