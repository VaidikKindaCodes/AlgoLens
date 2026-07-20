from app.sandbox.executor import CodeExecutor
result = CodeExecutor(timeout_seconds=5).execute("python", "print(\"hello\")", None)
print(result.status, repr(result.output), repr(result.error), result.execution_time_ms)
