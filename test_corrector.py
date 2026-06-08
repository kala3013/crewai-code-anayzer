"""
Quick test script to verify the CodeCorrector works on the example code.
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from standalone_analyzer import CodeAnalyzer
from standalone_corrector import CodeCorrector

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

# Run analysis
analyzer = CodeAnalyzer()
report = analyzer.analyze(EXAMPLE_CODE)
print("=" * 70)
print("  ANALYSIS OUTPUT")
print("=" * 70)
print(report)
print()

# Run correction
corrector = CodeCorrector()
corrected = corrector.correct(EXAMPLE_CODE, report)
print("=" * 70)
print("  CORRECTION OUTPUT (Code Corrector)")
print("=" * 70)
print(corrected)
print()

# Validate corrected code
print("=" * 70)
print("  VALIDATION")
print("=" * 70)
try:
    compile(corrected, '<string>', 'exec')
    print("  ✓ Compiled successfully - no syntax errors!")
    
    # Try executing
    namespace = {}
    exec(corrected, namespace)
    print("  ✓ Executed successfully!")
    
    # Test the function
    if 'fibonacci_iterative' in namespace:
        print("  ✓ Function 'fibonacci_iterative' found!")
        results = namespace['fibonacci_iterative'](10)
        print(f"  ✓ fibonacci_iterative(10) = {results}")
        expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
        if results == expected:
            print("  ✓ Output matches expected Fibonacci sequence!")
        else:
            print(f"  ✗ Expected: {expected}")
except SyntaxError as e:
    print(f"  ✗ SyntaxError: {e}")
except Exception as e:
    print(f"  ✗ Runtime error: {e}")