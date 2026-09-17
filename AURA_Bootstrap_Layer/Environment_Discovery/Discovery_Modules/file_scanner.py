from pathlib import Path

class FileScanner:

    def __init__(self, TARGET_APPLICATION_PATH):

        self.root_path = Path(TARGET_APPLICATION_PATH)

        if not self.root_path.exists():
            raise FileNotFoundError(
                f"Target application does not exist: {self.root_path}"
            )

        if not self.root_path.is_dir():
            raise ValueError(
                f"Target application path is not a directory: {self.root_path}"
            )  

    def scan(self):
        files =[]

        for path in self.root_path.rglob("*"):
            if path.is_file():
                files.append(path)

        return files