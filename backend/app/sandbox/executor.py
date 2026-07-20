import os
import tempfile
import time
from pathlib import Path

from app.core.exceptions import InvalidLanguageError
from app.sandbox.docker_runner import DockerRunner
from app.sandbox.languages import LANGUAGE_COMPILE_COMMANDS, LANGUAGE_EXTENSIONS, LANGUAGE_RUN_COMMANDS, SupportedLanguage


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
        return LANGUAGE_COMPILE_COMMANDS.get(language)

    def _run_command(self, language: str, tmpdir_path: Path) -> list[str]:
        try:
            return LANGUAGE_RUN_COMMANDS[language]
        except KeyError:
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
                run_cmd = self._run_command(language, tmpdir_path)
                docker_result = DockerRunner(timeout_seconds=self.timeout_seconds).execute(
                    language,
                    tmpdir_path,
                    compile_cmd,
                    run_cmd,
                    custom_input,
                )

                return ExecutionResult(
                    status=docker_result.status,
                    output=docker_result.output,
                    error=docker_result.error,
                    execution_time_ms=docker_result.execution_time_ms,
                )
            except Exception as e:
                return ExecutionResult(
                    status="runtime_error",
                    error=f"Execution error: {str(e)}",
                )
