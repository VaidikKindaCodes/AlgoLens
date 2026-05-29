import os
import subprocess
import tempfile
import time
import sys
from pathlib import Path

from app.core.exceptions import InvalidLanguageError
from app.sandbox.languages import LANGUAGE_EXTENSIONS, SupportedLanguage


class ExecutionResult:
    def __init__(
        self,
        status: str,
        output: str = "",
        error: str = "",
        execution_time_ms: float = 0,
        memory_usage_bytes: int | None = None,
    ):
        self.status = status
        self.output = output
        self.error = error
        self.execution_time_ms = execution_time_ms
        self.memory_usage_bytes = memory_usage_bytes


class CodeExecutor:
    def __init__(self, timeout_seconds: int = 5):
        self.timeout_seconds = timeout_seconds

    @staticmethod
    def _compiled_executable_name() -> str:
        return "program.exe" if os.name == "nt" else "program"

    def _compile_command(self, language: str, tmpdir_path: Path) -> list[str] | None:
        executable_path = tmpdir_path / self._compiled_executable_name()
        source_path = tmpdir_path / f"program{LANGUAGE_EXTENSIONS[language]}"

        if language == "cpp":
            return ["g++", "-o", str(executable_path), str(source_path)]
        if language == "java":
            return ["javac", str(tmpdir_path / "Program.java")]
        if language == "go":
            return ["go", "build", "-o", str(executable_path), str(source_path)]
        return None

    def _run_command(self, language: str, tmpdir_path: Path) -> list[str]:
        source_path = tmpdir_path / f"program{LANGUAGE_EXTENSIONS[language]}"
        executable_path = tmpdir_path / self._compiled_executable_name()

        if language == "python":
            return [sys.executable, str(source_path)]
        if language == "cpp":
            return [str(executable_path)]
        if language == "java":
            return ["java", "-cp", str(tmpdir_path), "Program"]
        if language == "javascript":
            return ["node", str(source_path)]
        if language == "go":
            return [str(executable_path)]
        raise InvalidLanguageError(language)

    def validate_language(self, language: str) -> None:
        try:
            SupportedLanguage(language.lower())
        except ValueError:
            raise InvalidLanguageError(language)

    def execute(
        self, language: str, code: str, custom_input: str | None = None
    ) -> ExecutionResult:
        self.validate_language(language)
        language = language.lower()

        with tempfile.TemporaryDirectory() as tmpdir:
            tmpdir_path = Path(tmpdir)
            ext = LANGUAGE_EXTENSIONS[language]
            code_file = tmpdir_path / f"program{ext}"
            code_file.write_text(code)

            try:
                compile_cmd = self._compile_command(language, tmpdir_path)
                if compile_cmd:
                    result = subprocess.run(
                        compile_cmd,
                        cwd=tmpdir_path,
                        capture_output=True,
                        timeout=self.timeout_seconds,
                        text=True,
                    )
                    if result.returncode != 0:
                        return ExecutionResult(
                            status="compile_error",
                            error=result.stderr or result.stdout,
                        )

                run_cmd = self._run_command(language, tmpdir_path)
                start_time = time.time()

                result = subprocess.run(
                    run_cmd,
                    cwd=tmpdir_path,
                    input=custom_input or "",
                    capture_output=True,
                    timeout=self.timeout_seconds,
                    text=True,
                )

                execution_time = (time.time() - start_time) * 1000

                if result.returncode != 0:
                    return ExecutionResult(
                        status="runtime_error",
                        error=result.stderr or result.stdout,
                        execution_time_ms=execution_time,
                    )

                return ExecutionResult(
                    status="accepted",
                    output=result.stdout,
                    execution_time_ms=execution_time,
                )

            except subprocess.TimeoutExpired:
                return ExecutionResult(
                    status="time_limit",
                    error=f"Code execution exceeded {self.timeout_seconds} seconds",
                )
            except Exception as e:
                return ExecutionResult(
                    status="runtime_error",
                    error=f"Execution error: {str(e)}",
                )
