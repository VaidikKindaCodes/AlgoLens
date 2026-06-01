class Prompts:
    @staticmethod
    def analyze_problem_prompt(problem_statement: str) -> str:
        return f"""You are an expert competitive programming assistant. Analyze the following problem and provide:
1. Problem constraints and their implications
2. Key observations and insights
3. Suggested data structures
4. Suggested algorithms/approaches
5. Time and space complexity expectations
6. Difficulty estimation (Easy/Medium/Hard)

Problem:
{problem_statement}

Provide a comprehensive analysis that would help a programmer understand and solve this problem."""

    @staticmethod
    def generate_hints_prompt(problem_statement: str, level: int) -> str:
        level_text = {
            1: "Beginner - very basic hints about the problem",
            2: "Intermediate - hints about the approach and algorithm",
            3: "Advanced - hints about optimization and edge cases",
        }[level]

        return f"""You are an expert competitive programming coach. Generate {level_text} for this problem.
The hints should guide the solver without directly revealing the solution.

Problem:
{problem_statement}

Provide 3-5 targeted hints that help the solver progress."""

    @staticmethod
    def generate_solution_prompt(problem_statement: str, language: str) -> str:
        return f"""You are an expert competitive programmer. Generate a well-optimized solution for this problem.
The solution should:
1. Be correct and handle all edge cases
2. Have optimal or near-optimal complexity
3. Include explanatory comments
4. Follow best practices for {language}

Problem:
{problem_statement}

Provide a complete, production-quality solution in {language}."""

    @staticmethod
    def generate_testcases_prompt(problem_statement: str, count: int) -> str:
        return f"""You are an expert at generating comprehensive test cases. Create {count} test cases for this problem.

Include:
1. Sample/basic test cases
2. Edge cases
3. Large input test cases
4. Corner cases

For each test case, provide:
- Input
- Expected Output
- Brief explanation

Problem:
{problem_statement}

Generate {count} diverse test cases."""

    @staticmethod
    def review_code_prompt(problem_statement: str, code: str, language: str) -> str:
        return f"""You are an expert code reviewer for competitive programming. Review this solution and provide:
1. Correctness assessment
2. Potential bugs or edge cases not handled
3. Optimization opportunities
4. Complexity analysis
5. Code quality improvements
6. Alternative approaches

Problem:
{problem_statement}

Code ({language}):
```{language}
{code}
```

Provide a detailed, constructive review."""

    @staticmethod
    def stress_test_prompt(problem_statement: str, solution: str, brute_force: str, language: str) -> str:
        return f"""You are an expert at finding edge cases and bugs. Compare these two implementations:

Problem:
{problem_statement}

Solution (optimized):
```{language}
{solution}
```

Brute force (correct but slow):
```{language}
{brute_force}
```

Identify:
1. Cases where they might differ
2. Potential bugs in the optimized solution
3. Edge cases to test
4. Input constraints that would expose issues

Provide 5-10 specific test cases that could reveal discrepancies."""
