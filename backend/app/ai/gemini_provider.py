import logging
from app.ai.base_provider import AIProvider
from app.ai.prompts import Prompts

logger = logging.getLogger(__name__)


class GeminiProvider(AIProvider):
    """Google Gemini provider for AI tasks."""

    def __init__(self, api_key: str = "", model_name: str = "gemini-pro"):
        self.api_key = api_key
        self.model_name = model_name
        self._client = None
        logger.debug(f"Initialized GeminiProvider with model: {model_name}")

    def _get_client(self):
        """Lazy-load the Gemini client."""
        if self._client is None:
            try:
                import google.generativeai as genai

                genai.configure(api_key=self.api_key)
                self._client = genai
                logger.debug("Gemini client initialized successfully")
            except ImportError:
                logger.error(
                    "google-generativeai not installed. Install with: pip install google-generativeai"
                )
                raise
            except Exception as e:
                logger.error(f"Failed to initialize Gemini client: {str(e)}")
                raise
        return self._client

    def analyze_problem(self, problem_statement: str) -> str:
        prompt = Prompts.analyze_problem_prompt(problem_statement)
        return self._call_api(prompt)

    def generate_hints(self, problem_statement: str, level: int) -> str:
        prompt = Prompts.generate_hints_prompt(problem_statement, level)
        return self._call_api(prompt)

    def generate_solution(self, problem_statement: str, language: str) -> str:
        prompt = Prompts.generate_solution_prompt(problem_statement, language)
        return self._call_api(prompt)

    def generate_testcases(self, problem_statement: str, count: int) -> str:
        prompt = Prompts.generate_testcases_prompt(problem_statement, count)
        return self._call_api(prompt)

    def review_code(self, problem_statement: str, code: str, language: str) -> str:
        prompt = Prompts.review_code_prompt(problem_statement, code, language)
        return self._call_api(prompt)

    def get_model_name(self) -> str:
        return self.model_name

    def _call_api(self, prompt: str) -> str:
        if not self.api_key:
            logger.warning("No Gemini API key provided, returning mock response")
            return self._get_mock_response(prompt)

        try:
            genai = self._get_client()
            model = genai.GenerativeModel(self.model_name)

            logger.debug(f"Calling Gemini API with model: {self.model_name}")
            response = model.generate_content(prompt)

            if response.text:
                logger.debug(f"Gemini API response received ({len(response.text)} chars)")
                return response.text
            else:
                logger.warning("Gemini API returned empty response")
                return "Error: Gemini returned empty response"

        except Exception as e:
            error_msg = f"Error calling Gemini API: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def _get_mock_response(self, prompt: str) -> str:
        return f"""[MOCK RESPONSE FROM {self.model_name}]

This is a mock response. To enable real API calls:
1. Set GEMINI_API_KEY in your .env file
2. Ensure the google-generativeai package is installed

Prompt received ({len(prompt)} characters):
{prompt[:200]}...

Mock Response:
This is a placeholder response. In production, this would contain:
- Comprehensive analysis of the problem
- Detailed hints or solutions
- Test case generation
- Code review insights

The response format and content would match the prompt's requirements."""
