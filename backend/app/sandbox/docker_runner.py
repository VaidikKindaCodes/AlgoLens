import shlex
import subprocess
import time
from dataclasses import dataclass
from pathlib import Path

from app.core.config import settings
from app.sandbox.docker_images import get_dockerfile_path, get_image_name
from app.sandbox.security import get_docker_resource_flags, get_docker_security_flags


@dataclass
class DockerExecutionResult:
    status: str
    output: str = ""
    error: str = ""
    execution_time_ms: float = 0.0


class DockerRunner:
    def __init__(self, timeout_seconds: int = 5):
        self.timeout_seconds = timeout_seconds

    def execute(
        self,
        language: str,
        workspace_path: Path,
        compile_cmd: list[str] | None,
        run_cmd: list[str],
        custom_input: str | None = None,
    ) -> DockerExecutionResult:
        try:
            image_name = self._prepare_image(language)
            container_id = self._create_container(image_name, workspace_path, compile_cmd, run_cmd)

            try:
                start_time = time.time()
                execution = subprocess.run(
                    ["docker", "start", "-a", container_id],
                    capture_output=True,
                    input=custom_input or "",
                    timeout=self.timeout_seconds,
                    text=True,
                )
                execution_time_ms = (time.time() - start_time) * 1000
                exit_code = self._inspect_container_exit_code(container_id)
                status = self._translate_status(exit_code)
                error_output = ""
                if status != "accepted":
                    error_output = execution.stderr.strip() or execution.stdout.strip()

                return DockerExecutionResult(
                    status=status,
                    output=execution.stdout,
                    error=error_output,
                    execution_time_ms=execution_time_ms,
                )
            except subprocess.TimeoutExpired:
                self._kill_container(container_id)
                return DockerExecutionResult(
                    status="time_limit",
                    error=f"Code execution exceeded {self.timeout_seconds} seconds",
                )
            finally:
                self._remove_container(container_id)

        except Exception as exc:
            return DockerExecutionResult(
                status="runtime_error",
                error=f"Docker execution failed: {exc}",
            )

    def _prepare_image(self, language: str) -> str:
        image_name = get_image_name(language)
        if self._image_exists(image_name):
            return image_name

        dockerfile_path = get_dockerfile_path(language)
        if not dockerfile_path.exists():
            raise RuntimeError(
                f"Docker image '{image_name}' is unavailable and dockerfile '{dockerfile_path}' was not found"
            )

        build_result = subprocess.run(
            [
                "docker",
                "build",
                "-t",
                image_name,
                "-f",
                str(dockerfile_path),
                str(dockerfile_path.parent),
            ],
            capture_output=True,
            text=True,
            timeout=settings.DOCKER_IMAGE_BUILD_TIMEOUT_SECONDS,
        )

        if build_result.returncode != 0:
            raise RuntimeError(
                f"Docker image build failed: {build_result.stderr or build_result.stdout}"
            )

        return image_name

    def _image_exists(self, image_name: str) -> bool:
        result = subprocess.run(
            ["docker", "image", "inspect", image_name],
            capture_output=True,
            text=True,
        )
        return result.returncode == 0

    def _create_container(
        self,
        image_name: str,
        workspace_path: Path,
        compile_cmd: list[str] | None,
        run_cmd: list[str],
    ) -> str:
        workspace_path = workspace_path.resolve()
        bound_workspace = workspace_path.as_posix() if workspace_path.drive else str(workspace_path)
        command = self._build_container_command(compile_cmd, run_cmd)

        create_args = [
            "docker",
            "create",
            "-i",
            "--workdir",
            "/workspace",
            "--user",
            "sandbox",
            *get_docker_security_flags(),
            *get_docker_resource_flags(),
            "-v",
            f"{bound_workspace}:/workspace:rw",
            image_name,
            "sh",
            "-c",
            command,
        ]

        result = subprocess.run(
            create_args,
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def _build_container_command(
        self,
        compile_cmd: list[str] | None,
        run_cmd: list[str],
    ) -> str:
        compile_shell = shlex.join(compile_cmd) if compile_cmd else ""
        run_shell = shlex.join(run_cmd)
        script_lines = ["set -o pipefail"]

        if compile_shell:
            script_lines.append(
                f"if ! {compile_shell}; then exit 100; fi"
            )

        script_lines.append(
            f"if ! {run_shell}; then exit 101; fi"
        )

        return " && ".join(script_lines)

    def _inspect_container_exit_code(self, container_id: str) -> int:
        result = subprocess.run(
            ["docker", "inspect", "--format={{.State.ExitCode}}", container_id],
            capture_output=True,
            text=True,
            check=True,
        )
        return int(result.stdout.strip())

    def _kill_container(self, container_id: str) -> None:
        subprocess.run(["docker", "kill", container_id], capture_output=True, text=True)

    def _remove_container(self, container_id: str) -> None:
        subprocess.run(["docker", "rm", "-f", container_id], capture_output=True, text=True)

    def _translate_status(self, exit_code: int) -> str:
        if exit_code == 0:
            return "accepted"
        if exit_code == 100:
            return "compile_error"
        return "runtime_error"
