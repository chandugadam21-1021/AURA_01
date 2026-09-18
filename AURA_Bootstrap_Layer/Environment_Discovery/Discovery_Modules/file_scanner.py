from pathlib import Path


class FileScanner:

    def __init__(self, target_application_path):
        self.root_path = Path(target_application_path)

        if not self.root_path.exists():
            raise FileNotFoundError(
                f"Target application does not exist: {self.root_path}"
            )

        if not self.root_path.is_dir():
            raise NotADirectoryError(
                f"Target application path is not a directory: {self.root_path}"
            )

    def scan(self):
        return [
            path
            for path in self.root_path.rglob("*")
            if path.is_file()
        ]