from app.core.config import settings


def get_docker_security_flags() -> list[str]:
    return [
        "--read-only",
        "--network",
        "none",
        "--cap-drop",
        "ALL",
        "--security-opt",
        "no-new-privileges",
        "--tmpfs",
        "/tmp:rw,noexec,nosuid,size=64m",
    ]


def get_docker_resource_flags() -> list[str]:
    return [
        "--cpus",
        str(settings.DOCKER_EXECUTOR_CPUS),
        "--memory",
        settings.DOCKER_EXECUTOR_MEMORY,
        "--pids-limit",
        str(settings.DOCKER_EXECUTOR_PIDS_LIMIT),
    ]
