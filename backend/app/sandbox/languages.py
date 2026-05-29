from enum import Enum


class SupportedLanguage(str, Enum):
    PYTHON = "python"
    CPP = "cpp"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    GO = "go"


LANGUAGE_EXTENSIONS = {
    "python": ".py",
    "cpp": ".cpp",
    "java": ".java",
    "javascript": ".js",
    "go": ".go",
}

LANGUAGE_COMPILE_COMMANDS = {
    "cpp": ["g++", "-o", "program", "program.cpp"],
    "java": ["javac", "Program.java"],
    "go": ["go", "build", "-o", "program", "program.go"],
}

LANGUAGE_RUN_COMMANDS = {
    "python": ["python", "program.py"],
    "cpp": ["./program"],
    "java": ["java", "Program"],
    "javascript": ["node", "program.js"],
    "go": ["./program"],
}
