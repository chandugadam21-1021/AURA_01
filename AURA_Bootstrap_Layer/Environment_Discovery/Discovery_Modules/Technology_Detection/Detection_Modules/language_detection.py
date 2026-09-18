from pathlib import Path
from collections import Counter


class LanguageDetectionModule:

    LANGUAGE_EXTENSIONS = {
        ".py": "Python",
        ".java": "Java",
        ".js": "JavaScript",
        ".jsx": "JavaScript",
        ".ts": "TypeScript",
        ".tsx": "TypeScript",
        ".go": "Go",
        ".rs": "Rust",
        ".c": "C",
        ".h": "C",
        ".cpp": "C++",
        ".cc": "C++",
        ".cxx": "C++",
        ".cs": "C#",
        ".php": "PHP",
        ".rb": "Ruby",
        ".swift": "Swift",
        ".kt": "Kotlin",
        ".kts": "Kotlin",
    }

    def __init__(self, files):
        self.files = [Path(file) for file in files]

    def Language_Detector(self):

        language_count = Counter(
            self.LANGUAGE_EXTENSIONS[file.suffix.lower()]
            for file in self.files
            if file.suffix.lower() in self.LANGUAGE_EXTENSIONS
        )

        languages = [
            language
            for language, _ in language_count.most_common()
        ]

        return {
            "primary_language": languages[0] if languages else None,
            "languages": languages,
        }