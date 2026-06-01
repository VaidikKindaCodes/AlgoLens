from app.ai.base_provider import AIProvider
from app.ai.prompts import Prompts
import logging

logger = logging.getLogger(__name__)


class MockOpenAIProvider(AIProvider):
    """Mock OpenAI provider for testing. Replace with real API calls when keys are available."""

    def __init__(self, api_key: str = ""):
        self.api_key = api_key
        self.model_name = "gpt-4"
        logger.debug(f"Initialized MockOpenAIProvider with model: {self.model_name}")

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
            logger.warning("No OpenAI API key provided, returning mock response")
            return self._get_mock_response(prompt)

        try:
            import openai
            openai.api_key = self.api_key
            logger.debug(f"Calling OpenAI API with model: {self.model_name}")
            response = openai.ChatCompletion.create(
                model=self.model_name,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7,
                max_tokens=2000,
            )
            logger.debug(f"OpenAI API response received ({len(response.choices[0].message.content)} chars)")
            return response.choices[0].message.content
        except Exception as e:
            error_msg = f"Error calling OpenAI API: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def _get_mock_response(self, prompt: str) -> str:
        return f"""[MOCK RESPONSE FROM {self.model_name}]

This is a mock response. To enable real API calls:
1. Set OPENAI_API_KEY in your .env file
2. Ensure the openai package is installed

Prompt received ({len(prompt)} characters):
{prompt[:200]}...

Mock Response:
This is a placeholder response. In production, this would contain:
- Comprehensive analysis of the problem
- Detailed hints or solutions
- Test case generation
- Code review insights

The response format and content would match the prompt's requirements."""
