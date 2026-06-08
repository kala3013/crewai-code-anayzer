"""
Quick test script to verify the CodeAnalyzer works on the example code.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from standalone_analyzer import CodeAnalyzer

# The example buggy code
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

# Test the analyzer
analyzer = CodeAnalyzer()
report = analyzer.analyze(EXAMPLE_CODE)
print(report)
print()
print(f"Errors found: {analyzer.get_error_count()}")
print(f"Warnings found: {analyzer.get_warning_count()}")
print(f"Has errors: {analyzer.has_errors()}")