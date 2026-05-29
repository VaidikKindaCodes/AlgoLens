from sqlalchemy import select
from sqlalchemy.orm import Session

from sqlalchemy import select
from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.ai.orchestrator import AIOrchestrator
from app.core.exceptions import NotFoundError
from app.models.ai_session import AISession
from app.models.problem_analysis import ProblemAnalysis
from app.models.ai_credential import AICredential
from app.services.ai_credentials import AICredentialService
from app.schemas.problem import (
    CodeReviewRequest,
    ProblemAnalyzeRequest,
    ProblemHintsRequest,
    ProblemSolutionRequest,
    ProblemTestCasesRequest,
)


class ProblemService:
    def __init__(self, db: Session):
        self.db = db
        self.ai = AIOrchestrator()
        self.cred_service = AICredentialService(db)

    def _get_user_credential(self, user_id: int):
        
        cred = self.cred_service.get_default_credential(user_id)
        
        if not cred:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No AI credential configured. Please add an AI credential in Settings before using AI features.")
        return {"provider": cred.provider, "api_key": self.cred_service.decrypt_key(cred), "model_name": cred.model_name}

    def analyze_problem(
        self, user_id: int, data: ProblemAnalyzeRequest
    ) -> ProblemAnalysis:
        user_cred = self._get_user_credential(user_id)
        response, model_used = self.ai.analyze_problem(
            data.problem_statement,
            provider_name=(user_cred.get("provider") if user_cred else None),
            api_key=(user_cred.get("api_key") if user_cred else None),
            model_name=(user_cred.get("model_name") if user_cred else None),
        )

        analysis = ProblemAnalysis(
            user_id=user_id,
            problem_statement=data.problem_statement,
            response=response,
            model_used=model_used,
        )
        self.db.add(analysis)
        self.db.commit()
        self.db.refresh(analysis)

        return analysis

    def generate_hints(
        self, user_id: int, workspace_id: int | None, data: ProblemHintsRequest
    ) -> AISession:
        user_cred = self._get_user_credential(user_id)
        response, model_used = self.ai.generate_hints(
            data.problem_statement,
            data.level,
            provider_name=(user_cred.get("provider") if user_cred else None),
            api_key=(user_cred.get("api_key") if user_cred else None),
            model_name=(user_cred.get("model_name") if user_cred else None),
        )

        session = AISession(
            user_id=user_id,
            workspace_id=workspace_id,
            action_type="generate_hints",
            prompt=data.problem_statement,
            response=response,
            model_used=model_used,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def generate_solution(
        self, user_id: int, workspace_id: int | None, data: ProblemSolutionRequest
    ) -> AISession:
        user_cred = self._get_user_credential(user_id)
        response, model_used = self.ai.generate_solution(
            data.problem_statement,
            data.language,
            provider_name=(user_cred.get("provider") if user_cred else None),
            api_key=(user_cred.get("api_key") if user_cred else None),
            model_name=(user_cred.get("model_name") if user_cred else None),
        )

        session = AISession(
            user_id=user_id,
            workspace_id=workspace_id,
            action_type="generate_solution",
            prompt=f"Language: {data.language}\nProblem: {data.problem_statement}",
            response=response,
            model_used=model_used,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def generate_testcases(
        self, user_id: int, workspace_id: int | None, data: ProblemTestCasesRequest
    ) -> AISession:
        user_cred = self._get_user_credential(user_id)
        response, model_used = self.ai.generate_testcases(
            data.problem_statement,
            data.count,
            provider_name=(user_cred.get("provider") if user_cred else None),
            api_key=(user_cred.get("api_key") if user_cred else None),
            model_name=(user_cred.get("model_name") if user_cred else None),
        )

        session = AISession(
            user_id=user_id,
            workspace_id=workspace_id,
            action_type="generate_testcases",
            prompt=f"Count: {data.count}\nProblem: {data.problem_statement}",
            response=response,
            model_used=model_used,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def review_code(
        self, user_id: int, workspace_id: int | None, data: CodeReviewRequest
    ) -> AISession:
        user_cred = self._get_user_credential(user_id)
        response, model_used = self.ai.review_code(
            data.problem_statement,
            data.code,
            data.language,
            provider_name=(user_cred.get("provider") if user_cred else None),
            api_key=(user_cred.get("api_key") if user_cred else None),
            model_name=(user_cred.get("model_name") if user_cred else None),
        )

        session = AISession(
            user_id=user_id,
            workspace_id=workspace_id,
            action_type="review_code",
            prompt=f"Language: {data.language}\nProblem: {data.problem_statement}\nCode: {data.code}",
            response=response,
            model_used=model_used,
        )
        self.db.add(session)
        self.db.commit()
        self.db.refresh(session)

        return session

    def get_problem_analyses(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[ProblemAnalysis], int]:
        query = select(ProblemAnalysis).where(
            ProblemAnalysis.user_id == user_id
        )
        analyses = self.db.execute(
            query.offset(skip).limit(limit)
        ).scalars().all()
        total = self.db.execute(
            select(ProblemAnalysis).where(ProblemAnalysis.user_id == user_id)
        ).scalars().all().__len__()

        return analyses, total

    def get_problem_analysis(self, user_id: int, analysis_id: int) -> ProblemAnalysis:
        analysis = self.db.execute(
            select(ProblemAnalysis).where(
                ProblemAnalysis.user_id == user_id,
                ProblemAnalysis.id == analysis_id,
            )
        ).scalar()
        if not analysis:
            raise NotFoundError("Problem analysis not found")
        return analysis

    def delete_problem_analysis(self, user_id: int, analysis_id: int) -> bool:
        analysis = self.get_problem_analysis(user_id, analysis_id)
        self.db.delete(analysis)
        self.db.commit()
        return True

    def get_ai_sessions(
        self, user_id: int, skip: int = 0, limit: int = 100
    ) -> tuple[list[AISession], int]:
        query = select(AISession).where(
            AISession.user_id == user_id
        )
        sessions = self.db.execute(
            query.offset(skip).limit(limit)
        ).scalars().all()
        total = self.db.query(AISession).filter(
            AISession.user_id == user_id
        ).count()

        return sessions, total

    def get_ai_session(self, user_id: int, session_id: int) -> AISession:
        session = self.db.execute(
            select(AISession).where(
                AISession.user_id == user_id,
                AISession.id == session_id,
            )
        ).scalar()
        if not session:
            raise NotFoundError("AI session not found")
        return session

    def delete_ai_session(self, user_id: int, session_id: int) -> bool:
        session = self.get_ai_session(user_id, session_id)
        self.db.delete(session)
        self.db.commit()
        return True
