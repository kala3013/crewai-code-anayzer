"""
Code Analyzer & Correction System
==================================
A self-contained Python tool that:
1. Analyzes Python code for syntax, indentation, and logical errors (Code Analyzer)
2. Corrects identified errors automatically (Code Corrector)
3. Manages the full pipeline with validation (Manager)

No external API keys required. Pure Python rule-based engine.
"""

from standalone_analyzer import CodeAnalyzer
from standalone_corrector import CodeCorrector
from standalone_manager import PipelineManager


# Built-in example buggy code with indentation errors
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


def main():
    """Main entry point for the Code Analysis and Correction System."""
    
    print()
    print("=" * 70)
    print("       Code Analysis & Correction System")
    print("  AI-powered Python code error detection and fixing")
    print("=" * 70)
    print()

    # Display input code
    print("-" * 70)
    print("INPUT CODE:")
    print("-" * 70)
    print(EXAMPLE_CODE)
    print("-" * 70)
    print()

    # Create the components
    print("Creating pipeline components...")
    print("  • Code Analyzer: Identifies syntax, indentation & logical errors")
    print("  • Code Corrector: Fixes identified errors")
    print("  • Manager: Oversees the analysis and correction process")
    print("  • Process: Sequential (analysis → correction → validation)")
    print()

    analyzer = CodeAnalyzer()
    corrector = CodeCorrector()
    manager = PipelineManager(analyzer, corrector)

    # Run the pipeline
    print("Starting analysis and correction pipeline...")
    print("=" * 70)
    print()

    results = manager.run_pipeline(EXAMPLE_CODE)

    # Display results
    print()
    print("=" * 70)
    print("  RESULTS")
    print("=" * 70)
    print()
    
    print("*" * 70)
    print("  ANALYSIS OUTPUT (Code Analyzer)")
    print("*" * 70)
    print(results['analysis_output'])
    print()
    
    print("*" * 70)
    print("  CORRECTION OUTPUT (Code Corrector)")
    print("*" * 70)
    print(results['correction_output'])
    print()
    
    print(results['validation'])
    print()
    
    manager.print_summary()
    
    if results['success']:
        print()
        print("=" * 70)
        print("  ✓ Analysis and correction completed successfully!")
        print("=" * 70)
    else:
        print()
        print("=" * 70)
        print("  ✗ Pipeline encountered issues.")
        print("=" * 70)


if __name__ == "__main__":
    main()