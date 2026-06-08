"""
Main entry point for the CrewAI Code Analysis and Correction System.
Analyzes Python code for errors and corrects them using AI agents.
Non-interactive mode with built-in example code.
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def configure_api_key():
    """
    Loads the OpenAI API key from the .env file.
    Exits if no valid key is found.
    """
    api_key = os.getenv("OPENAI_API_KEY")

    if api_key and api_key != "your-openai-api-key-here":
        os.environ["OPENAI_API_KEY"] = api_key
        print("✓ OpenAI API key found in .env file")
        return

    print()
    print("=" * 60)
    print("  OpenAI API Key Required")
    print("=" * 60)
    print("Please add your OpenAI API key to the .env file.")
    print()
    print("Format in .env file:")
    print("  OPENAI_API_KEY=sk-your-key-here")
    print()
    print("Get your key at: https://platform.openai.com/api-keys")
    sys.exit(1)


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
    """Main function to run the code analysis and correction system."""
    print()
    print("=" * 70)
    print("       CrewAI Code Analysis & Correction System")
    print("  AI-powered Python code error detection and fixing")
    print("=" * 70)
    print()

    # Step 1: Configure API key
    configure_api_key()

    # Now import crew-related modules (after API key is set)
    from src.crew_setup import create_code_analysis_crew

    code_to_analyze = EXAMPLE_CODE

    print()
    print("-" * 70)
    print("INPUT CODE:")
    print("-" * 70)
    print(code_to_analyze)
    print("-" * 70)
    print()

    # Create crew with agents
    print("Creating crew with agents...")
    print("  • Code Analyzer: Identifies syntax, indentation & logical errors")
    print("  • Code Corrector: Fixes identified errors")
    print("  • Manager: Oversees the analysis and correction process")
    print("  • Process: Sequential (analysis → correction)")
    print("  • Planning: Enabled")
    print()

    print("Starting analysis and correction pipeline...")
    print("=" * 70)
    print()

    try:
        # Create and run the crew
        crew = create_code_analysis_crew(code_to_analyze)
        result = crew.kickoff()

        print()
        print("=" * 70)
        print("  FINAL RESULTS")
        print("=" * 70)
        print()

        # Display analysis results
        if len(crew.tasks) >= 1:
            print("*" * 70)
            print("  ANALYSIS OUTPUT (Code Analyzer)")
            print("*" * 70)
            analysis_output = crew.tasks[0].output
            if analysis_output:
                raw = analysis_output.raw_output if hasattr(analysis_output, 'raw_output') else str(analysis_output)
                print(raw)
            else:
                print("(No output captured)")
            print()

        # Display correction results
        if len(crew.tasks) >= 2:
            print("*" * 70)
            print("  CORRECTION OUTPUT (Code Corrector)")
            print("*" * 70)
            correction_output = crew.tasks[1].output
            if correction_output:
                raw = correction_output.raw_output if hasattr(correction_output, 'raw_output') else str(correction_output)
                print(raw)
            else:
                print("(No output captured)")
            print()

        print("=" * 70)
        print("  ✓ Analysis and correction completed successfully!")
        print("=" * 70)

    except Exception as e:
        print(f"\n✗ Error during execution: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()