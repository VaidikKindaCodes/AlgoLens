from pathlib import Path

from app.sandbox.languages import SupportedLanguage

BASE_DIR = Path(__file__).resolve().parents[2]
DOCKERFILES_DIR = BASE_DIR / "dockerfiles"

IMAGE_TAGS = {
    "python": "algolens-exec-python:latest",
    "cpp": "algolens-exec-cpp:latest",
    "java": "algolens-exec-java:latest",
    "javascript": "algolens-exec-javascript:latest",
    "go": "algolens-exec-go:latest",
}


def get_image_name(language: str) -> str:
    try:
        SupportedLanguage(language.lower())
    except ValueError:
        raise ValueError(f"Unsupported language: {language}")

    return IMAGE_TAGS[language.lower()]


def get_dockerfile_path(language: str) -> Path:
    try:
        SupportedLanguage(language.lower())
    except ValueError:
        raise ValueError(f"Unsupported language: {language}")

    return DOCKERFILES_DIR / language.lower() / "Dockerfile"


def get_build_context(language: str) -> Path:
    return get_dockerfile_path(language).parent
