"""Test script for the CodeInterpreterTool."""
import sys
import os

# Add the project directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.code_interpreter_tool import CodeInterpreterTool

# Test 1: Valid Python code
print("=" * 60)
print("TEST 1: Valid Python code")
print("=" * 60)
tool = CodeInterpreterTool()
result = tool._run('print("hello world")')
print(result)

# Test 2: Code with indentation errors (the example from task)
print("\n\n")
print("=" * 60)
print("TEST 2: Code with indentation errors")
print("=" * 60)
buggy_code = """def fibonacci_iterative(n):

    if n < 0:

        return []

    elif n == 1:

        return [0]

    elif n == 2:

        return [0, 1]



    fib_sequence = [0, 1]

    for i in range(2, n):

    next_fib = fib_sequence[-1] + fib_sequence[-2]

    fib_sequence.append(next_fib)

    return fib_sequence"""

result = tool._run(buggy_code)
print(result)

# Test 3: Verify all imports work
print("\n\n")
print("=" * 60)
print("TEST 3: Verify module imports")
print("=" * 60)
try:
    from src.agents import CodeAnalysisAgents
    print("✓ agents.py imports successfully")
    
    from src.tasks import CodeAnalysisTasks
    print("✓ tasks.py imports successfully")
    
    from src.crew_setup import create_code_analysis_crew
    print("✓ crew_setup.py imports successfully")
    
    print("\nAll imports successful!")
except Exception as e:
    print(f"Import error: {e}")