"""
Demo script that runs the CrewAI code analysis and correction pipeline
non-interactively using the example fibonacci code.
"""
import os
import sys
from dotenv import load_dotenv

# Load API key from .env
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
if not api_key or api_key == "your-openai-api-key-here":
    print("ERROR: OpenAI API key not found in .env file!")
    print("Please add your key to .env or run main.py interactively.")
    sys.exit(1)

os.environ["OPENAI_API_KEY"] = api_key

from src.crew_setup import create_code_analysis_crew

# The example buggy code with indentation errors
EXAMPLE_CODE = """def fibonacci_iterative(n):

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

print("=" * 70)
print("  CrewAI Code Analysis & Correction System - DEMO")
print("=" * 70)
print()
print("Input code:")
print("-" * 40)
print(EXAMPLE_CODE)
print("-" * 40)
print()
print("Creating crew (Code Analyzer + Code Corrector + Manager)...")
print("Process: Sequential | Planning: Enabled")
print()
print("Starting pipeline...")
print("=" * 70)

try:
    crew = create_code_analysis_crew(EXAMPLE_CODE)
    result = crew.kickoff()
    
    print()
    print("=" * 70)
    print("  RESULTS")
    print("=" * 70)
    
    if len(crew.tasks) >= 1:
        print()
        print(">>> ANALYSIS OUTPUT (Code Analyzer):")
        print("-" * 60)
        analysis_output = crew.tasks[0].output
        if analysis_output:
            print(analysis_output.raw_output if hasattr(analysis_output, 'raw_output') else str(analysis_output))
        else:
            print("(No output)")
    
    if len(crew.tasks) >= 2:
        print()
        print(">>> CORRECTION OUTPUT (Code Corrector):")
        print("-" * 60)
        correction_output = crew.tasks[1].output
        if correction_output:
            print(correction_output.raw_output if hasattr(correction_output, 'raw_output') else str(correction_output))
        else:
            print("(No output)")
    
    print()
    print("=" * 70)
    print("  DEMO COMPLETED SUCCESSFULLY")
    print("=" * 70)

except Exception as e:
    print(f"\nERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)