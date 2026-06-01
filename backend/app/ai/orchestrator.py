import logging
from app.ai.base_provider import AIProvider
from app.ai.openai_provider import MockOpenAIProvider
from app.ai.huggingface_provider import HuggingFaceProvider
from app.ai.gemini_provider import GeminiProvider
from app.core.config import settings
from app.core.exceptions import AIServiceError

logger = logging.getLogger(__name__)


class AIOrchestrator:
    """Orchestrates AI provider selection and supports per-call API keys."""

    def __init__(self):
        # Keep a registry of provider factories for defaults
        self.registry = {
            "openai": lambda api_key, model: MockOpenAIProvider(api_key),
            "huggingface": lambda api_key, model: HuggingFaceProvider(api_key, model or settings.HUGGINGFACE_DEFAULT_MODEL),
            "gemini": lambda api_key, model: GeminiProvider(api_key, model or "gemini-pro"),
        }

    def _get_provider_instance(self, provider_name: str | None, api_key: str | None, model_name: str | None = None) -> AIProvider:
        selected_provider = (provider_name or settings.DEFAULT_AI_MODEL or "openai").lower()
        api_key_to_use = api_key or getattr(settings, f"{selected_provider.upper()}_API_KEY", "")
        
        logger.info(
            f"Provider selection - Selected provider: {selected_provider}, "
            f"Model: {model_name or 'default'}, "
            f"API key configured: {'Yes' if api_key_to_use else 'No'}"
        )
        
        factory = self.registry.get(selected_provider)
        if not factory:
            logger.warning(f"Provider '{selected_provider}' not found in registry. Falling back to OpenAI.")
            return MockOpenAIProvider(api_key or settings.OPENAI_API_KEY)
        
        provider_instance = factory(api_key_to_use, model_name)
        logger.debug(f"Provider instantiated: {type(provider_instance).__name__}")
        return provider_instance

    def analyze_problem(self, problem_statement: str, provider_name: str | None = None, api_key: str | None = None, model_name: str | None = None) -> tuple[str, str]:
        try:
            provider = self._get_provider_instance(provider_name, api_key, model_name)
            logger.info(f"analyze_problem: Using {type(provider).__name__} (model: {provider.get_model_name()})")
            response = provider.analyze_problem(problem_statement)
            return response, provider.get_model_name()
        except Exception as e:
            logger.error(f"Failed to analyze problem: {str(e)}", exc_info=True)
            raise AIServiceError(f"Failed to analyze problem: {str(e)}")

    def generate_hints(self, problem_statement: str, level: int, provider_name: str | None = None, api_key: str | None = None, model_name: str | None = None) -> tuple[str, str]:
        try:
            provider = self._get_provider_instance(provider_name, api_key, model_name)
            logger.info(f"generate_hints: Using {type(provider).__name__} (model: {provider.get_model_name()})")
            response = provider.generate_hints(problem_statement, level)
            return response, provider.get_model_name()
        except Exception as e:
            logger.error(f"Failed to generate hints: {str(e)}", exc_info=True)
            raise AIServiceError(f"Failed to generate hints: {str(e)}")

    def generate_solution(self, problem_statement: str, language: str, provider_name: str | None = None, api_key: str | None = None, model_name: str | None = None) -> tuple[str, str]:
        try:
            provider = self._get_provider_instance(provider_name, api_key, model_name)
            logger.info(f"generate_solution: Using {type(provider).__name__} (model: {provider.get_model_name()})")
            response = provider.generate_solution(problem_statement, language)
            return response, provider.get_model_name()
        except Exception as e:
            logger.error(f"Failed to generate solution: {str(e)}", exc_info=True)
            raise AIServiceError(f"Failed to generate solution: {str(e)}")

    def generate_testcases(self, problem_statement: str, count: int, provider_name: str | None = None, api_key: str | None = None, model_name: str | None = None) -> tuple[str, str]:
        try:
            provider = self._get_provider_instance(provider_name, api_key, model_name)
            logger.info(f"generate_testcases: Using {type(provider).__name__} (model: {provider.get_model_name()})")
            response = provider.generate_testcases(problem_statement, count)
            return response, provider.get_model_name()
        except Exception as e:
            logger.error(f"Failed to generate test cases: {str(e)}", exc_info=True)
            raise AIServiceError(f"Failed to generate test cases: {str(e)}")

    def review_code(self, problem_statement: str, code: str, language: str, provider_name: str | None = None, api_key: str | None = None, model_name: str | None = None) -> tuple[str, str]:
        try:
            provider = self._get_provider_instance(provider_name, api_key, model_name)
            logger.info(f"review_code: Using {type(provider).__name__} (model: {provider.get_model_name()})")
            response = provider.review_code(problem_statement, code, language)
            return response, provider.get_model_name()
        except Exception as e:
            logger.error(f"Failed to review code: {str(e)}", exc_info=True)
            raise AIServiceError(f"Failed to review code: {str(e)}")

    def switch_provider(self, provider_name: str) -> None:
        # switching dynamic providers is not supported; clients should set provider per-request or via ai-credentials
        raise AIServiceError("Provider switching at runtime is deprecated. Use per-request provider selection or set a default AI credential.")
