from abc import ABC, abstractmethod


class AIProvider(ABC):
    """Base interface for AI providers"""

    @abstractmethod
    def analyze_problem(self, problem_statement: str) -> str:
        """Analyze a competitive programming problem"""
        pass

    @abstractmethod
    def generate_hints(self, problem_statement: str, level: int) -> str:
        """Generate hints for a problem (level 1-3)"""
        pass

    @abstractmethod
    def generate_solution(self, problem_statement: str, language: str) -> str:
        """Generate a solution for a problem in a specific language"""
        pass

    @abstractmethod
    def generate_testcases(self, problem_statement: str, count: int) -> str:
        """Generate test cases for a problem"""
        pass

    @abstractmethod
    def review_code(self, problem_statement: str, code: str, language: str) -> str:
        """Review code for a problem"""
        pass

    @abstractmethod
    def get_model_name(self) -> str:
        """Get the name of the model being used"""
        pass
