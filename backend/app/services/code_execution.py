from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.exceptions import ValidationError
from app.models.code_execution import CodeExecution
from app.sandbox.executor import CodeExecutor
from app.schemas.workspace import CodeExecutionRequest


class CodeExecutionService:
    def __init__(self, db: Session):
        self.db = db
        self.executor = CodeExecutor(timeout_seconds=settings.CODE_EXECUTION_TIMEOUT_SECONDS)

    def execute_code(
        self,
        user_id: int,
        workspace_id: int | None,
        data: CodeExecutionRequest,
    ) -> CodeExecution:
        if len(data.code) > settings.MAX_CODE_LENGTH:
            raise ValidationError(f"Code exceeds maximum length of {settings.MAX_CODE_LENGTH} characters")

        if data.custom_input and len(data.custom_input) > settings.MAX_INPUT_LENGTH:
            raise ValidationError(f"Input exceeds maximum length of {settings.MAX_INPUT_LENGTH} characters")

        if data.language.lower() not in settings.SUPPORTED_LANGUAGES:
            raise ValidationError(f"Language '{data.language}' is not supported")

        result = self.executor.execute(data.language, data.code, data.custom_input)

        execution = CodeExecution(
            user_id=user_id,
            workspace_id=workspace_id,
            language=data.language,
            code=data.code,
            custom_input=data.custom_input or "",
            output=result.output,
            error=result.error,
            execution_time_ms=result.execution_time_ms,
            status=result.status,
        )
        self.db.add(execution)
        self.db.commit()
        self.db.refresh(execution)

        return execution

    def get_execution_history(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[CodeExecution], int]:
        query = select(CodeExecution).where(
            CodeExecution.user_id == user_id
        ).order_by(CodeExecution.created_at.desc())

        executions = self.db.execute(
            query.offset(skip).limit(limit)
        ).scalars().all()

        total = self.db.query(CodeExecution).filter(
            CodeExecution.user_id == user_id
        ).count()

        return executions, total
