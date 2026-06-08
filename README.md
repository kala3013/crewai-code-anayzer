# Code Analysis & Correction System

A self-contained Python tool that automatically **analyzes** Python code for errors and **corrects** them. Inspired by multi-agent AI systems like CrewAI, this program uses three modular components — **Code Analyzer**, **Code Corrector**, and **Manager** — working together in a sequential pipeline.

No external API keys, internet access, or AI services required. Pure Python rule-based engine.

---

## 🧠 System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     PipelineManager                         │
│                      (Manager)                              │
├─────────────────────────────────────────────────────────────┤
│  Step 1                    Step 2                    Step 3 │
│  ┌──────────────┐         ┌──────────────┐         ┌──────┐ │
│  │Code Analyzer │ ──────▶ │Code Corrector│ ──────▶ │Valid.│ │
│  │ (detects     │         │  (fixes      │         │(test)│ │
│  │  errors)     │         │   errors)    │         │      │ │
│  └──────────────┘         └──────────────┘         └──────┘ │
└─────────────────────────────────────────────────────────────┘
```

### Components

| Component | Role | Description |
|-----------|------|-------------|
| **Code Analyzer** | Error Detection | Scans Python code for syntax, indentation, logical, and runtime errors. Produces a numbered error report with line numbers. |
| **Code Corrector** | Error Fixing | Automatically fixes indentation, missing colons, and misplaced return statements. Outputs the complete corrected code. |
| **Manager** | Orchestration | Runs the pipeline: analysis → correction → validation. Validates output by compiling, executing, and testing the corrected code. |

---

## ✨ Features

- **Syntax Error Detection** — missing colons, invalid Python syntax
- **Indentation Correction** — fixes loop bodies at wrong indentation levels (e.g., Fibonacci bug)
- **Conditional Block Handling** — correctly handles `if`/`elif`/`else` blocks and their bodies
- **Return Statement Placement** — automatically moves function-level `return` statements outside of loops
- **Runtime Validation** — compiles and executes corrected code to verify correctness
- **Functional Testing** — tests corrected functions with sample inputs
- **Detailed Reports** — comprehensive error report, fix summary, and final output

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- No additional packages required (uses only the Python standard library)

### Installation

```bash
# Clone or download the project
cd crewai-code-analyzer
```

### Running the Demo

```bash
python standalone_main.py
```

This runs the full pipeline on the built-in example (buggy Fibonacci sequence code).

### Running Tests

```bash
# Test the analyzer only
python test_analyzer.py

# Test the full analysis + correction pipeline
python test_corrector.py
```

---

## 📋 Example

### Input (Buggy Code)

```python
def fibonacci_iterative(n):

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

    return fib_sequence
```

### Analysis Output

```
  ✗ 3 ERROR(S) FOUND:

  1. Line 21: SyntaxError - expected an indented block after 'for' statement on line 19
  2. Line 21: IndentationError - Expected an indented block after 'for i in range(2, n)'
  3. Line 21: IndentationError - Expected indented block after 'for' loop at line 19
```

### Corrected Output

```python
def fibonacci_iterative(n):

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

    return fib_sequence
```

### Validation Result

```
  ✓ Code compiled successfully - No syntax errors
  ✓ Code executed successfully - No runtime errors
  ✓ fibonacci_iterative(10) = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
  ✓ Function output matches expected Fibonacci sequence!
```

---

## 📁 File Structure

```
crewai-code-analyzer/
│
├── standalone_main.py          # Entry point — runs the full pipeline
├── standalone_analyzer.py      # Code Analyzer — detects errors
├── standalone_corrector.py     # Code Corrector — fixes errors
├── standalone_manager.py       # Pipeline Manager — orchestrates & validates
│
├── test_analyzer.py            # Test script for the analyzer
├── test_corrector.py           # Test script for the full pipeline
│
├── main.py                     # (Original) CrewAI entry point (requires OpenAI API key)
├── run_demo.py                 # (Original) CrewAI demo script
├── .env                        # (Original) API key configuration
│
└── src/                        # (Original) CrewAI agent/task definitions
    ├── agents.py
    ├── tasks.py
    ├── crew_setup.py
    └── code_interpreter_tool.py
```

---

## 🛠️ How It Works

### Code Analyzer
1. Parses each line, classifying it as header, continuation, return, or regular content
2. Checks syntax using `ast.parse()` 
3. Analyzes indentation consistency (tabs vs spaces, wrong levels)
4. Detects logic errors (e.g., `return` outside function)
5. Executes the code in a sandbox to catch runtime errors

### Code Corrector
1. Identifies each block header (`def`, `if`, `for`, `while`, etc.)
2. Collects consecutive body lines after each header
3. Adjusts body indentation to be one level deeper than the header
4. Handles continuation keywords (`elif`, `else`) — keeps them at matching header level
5. Moves the last `return` in a loop body back to the function body level
6. Adds missing colons where needed

### Pipeline Manager
1. Calls the Analyzer to produce error report
2. Passes the error report + original code to the Corrector
3. Validates the corrected code:
   - Compiles with `compile()`
   - Executes with `exec()`
   - Runs functional tests (e.g., Fibonacci sequence)
4. Generates a comprehensive final report

---

## 🔧 Customization

You can analyze your own Python code by modifying the `EXAMPLE_CODE` variable in `standalone_main.py`:

```python
EXAMPLE_CODE = '''def my_function(x):
    if x > 0:
    print("Positive")
    return x
'''
```

Or import the components directly:

```python
from standalone_analyzer import CodeAnalyzer
from standalone_corrector import CodeCorrector
from standalone_manager import PipelineManager

analyzer = CodeAnalyzer()
corrector = CodeCorrector()
manager = PipelineManager(analyzer, corrector)

results = manager.run_pipeline(your_code_string)
print(results['analysis_output'])
print(results['correction_output'])
print(results['validation'])
```

---

## 🧪 Test Results

| Test | Result |
|------|--------|
| Fibonacci code with indentation errors | ✅ 3 errors detected, 2 fixes applied, corrected code produces correct Fibonacci sequence |
| Valid Python code (no errors) | ✅ No errors reported, code passes through unchanged |
| Missing colons | ✅ Colons automatically added |
| Return inside loop | ✅ Return moved to function body level |

---

## 📝 License

This project is provided for educational and demonstration purposes.#   c r e w a i - c o d e - a n a l y z e r  
 #   c r e w a i - c o d e - a n a y z e r  
 