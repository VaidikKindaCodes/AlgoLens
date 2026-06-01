from app.ai.base_provider import AIProvider
from app.ai.prompts import Prompts
import requests
import logging

logger = logging.getLogger(__name__)


class HuggingFaceProvider(AIProvider):
    """Simple Hugging Face Inference API provider."""

    def __init__(self, api_key: str = "", model_name: str = "gpt2"):
        self.api_key = api_key
        self.model_name = model_name
        logger.debug(f"Initialized HuggingFaceProvider with model: {model_name}")

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
            logger.warning("No HuggingFace API key provided, returning mock response")
            return self._get_mock_response(prompt)

        url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        headers = {"Authorization": f"Bearer {self.api_key}"}
        payload = {"inputs": prompt, "options": {"wait_for_model": True}}

        try:
            logger.debug(f"Calling HuggingFace API with model: {self.model_name}")
            resp = requests.post(url, headers=headers, json=payload, timeout=30)
            resp.raise_for_status()
            data = resp.json()
            logger.debug(f"HuggingFace API response received")
            # Hugging Face Inference may return a list of generated texts
            if isinstance(data, list) and len(data) > 0:
                # Try to extract text from common shapes
                first = data[0]
                if isinstance(first, dict):
                    return first.get("generated_text") or str(first)
                return str(first)
            if isinstance(data, dict) and "generated_text" in data:
                return data["generated_text"]
            return str(data)
        except Exception as e:
            error_msg = f"Error calling Hugging Face Inference API: {str(e)}"
            logger.error(error_msg)
            return error_msg

    def _get_mock_response(self, prompt: str) -> str:
        return f"[MOCK HUGGINGFACE RESPONSE]\nModel: {self.model_name}\nPrompt: {prompt[:200]}..."