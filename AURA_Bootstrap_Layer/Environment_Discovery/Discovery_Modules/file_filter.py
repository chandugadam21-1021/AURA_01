from pathlib import Path


class FileFilter:

    def __init__(self, files):
        self.files = files

    def filter(self):

        filtered_files = []

        for file in self.files:

            file = Path(file)

            # Ignore hidden files
            if file.name.startswith("."):
                continue

            # Ignore common unnecessary directories
            if any(
                directory in file.parts
                for directory in [
                    "__pycache__",
                    "node_modules",
                    ".git",
                    ".venv",
                    "venv",
                    "target",
                    "build",
                    "dist"
                ]
            ):
                continue

            filtered_files.append(file)

        return filtered_files