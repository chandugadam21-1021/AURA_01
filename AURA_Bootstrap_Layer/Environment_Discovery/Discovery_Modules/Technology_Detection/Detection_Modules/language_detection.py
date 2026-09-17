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

        language_count = Counter()

        for file in self.files:

            language = self.LANGUAGE_EXTENSIONS.get(
                file.suffix.lower()
            )

            if language:
                language_count[language] += 1

        if not language_count:
            return {
                "primary_language": None,
                "languages": []
            }

        languages = []

        for language, count in language_count.most_common():

            languages.append(language)

        return {
            "primary_language": languages[0],
            "languages": languages
        }