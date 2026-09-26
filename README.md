# 🧠 Code Analysis & Correction System

### 🔍 Analyze → 🛠️ Correct → ✅ Validate

> **An intelligent, self-contained Python code analysis pipeline that automatically detects, corrects, and validates common Python programming errors — without APIs, internet access, or external AI services.**

<p align="center">

![Python](https://img.shields.io/badge/Python-3.8%2B-3776AB?style=for-the-badge\&logo=python\&logoColor=white)
![AI](https://img.shields.io/badge/AI-Inspired%20Pipeline-8A2BE2?style=for-the-badge)
![Architecture](https://img.shields.io/badge/Architecture-Modular-orange?style=for-the-badge)
![Dependencies](https://img.shields.io/badge/Dependencies-Standard%20Library-success?style=for-the-badge)
![Status](https://img.shields.io/badge/Status-Active-brightgreen?style=for-the-badge)

</p>

<p align="center">

**A rule-based developer tool inspired by multi-agent AI architectures such as CrewAI.**

<br>

`Code Analyzer` → `Code Corrector` → `Pipeline Manager` → `Validation`

</p>

---

## 🚀 Project Overview

Writing code is only the first step.

Developers often spend significant time identifying:

* ❌ Syntax errors
* ❌ Incorrect indentation
* ❌ Missing colons
* ❌ Incorrect block structures
* ❌ Misplaced `return` statements
* ❌ Runtime failures
* ❌ Unexpected program output

This project demonstrates how a **modular intelligent pipeline** can automate several of these tasks.

The system takes buggy Python code as input and processes it through three major stages:

```text
        📝 Python Source Code
                 │
                 ▼
        ┌─────────────────┐
        │  🔍 Analyzer    │
        │ Error Detection │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  🛠️ Corrector   │
        │  Error Fixing   │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  🎯 Validator   │
        │ Compile + Run   │
        └────────┬────────┘
                 │
                 ▼
        ┌─────────────────┐
        │  📊 Final Report │
        └─────────────────┘
```

The entire process runs locally using **pure Python**.

---

# ✨ Key Features

<table>
<tr>
<td width="50%">

### 🔍 Intelligent Code Analysis

Detects common Python problems including:

* Syntax errors
* Indentation errors
* Missing colons
* Invalid block structures
* Logical issues
* Runtime problems

</td>

<td width="50%">

### 🛠️ Automated Correction

Automatically attempts to repair:

* Incorrect indentation
* Missing `:`
* Misplaced `return`
* Loop body indentation
* `if / elif / else` structures
* Function-level statements

</td>
</tr>

<tr>
<td width="50%">

### ✅ Runtime Validation

After correction, the system:

* Compiles the code
* Executes the code
* Detects runtime failures
* Tests functions
* Compares expected output

</td>

<td width="50%">

### 📊 Detailed Reporting

Generates:

* Error reports
* Line numbers
* Correction summaries
* Validation results
* Final execution output

</td>
</tr>
</table>

---

# 🧩 System Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    PIPELINE MANAGER                         │
│                                                             │
│   ┌───────────────┐      ┌───────────────┐                │
│   │ CODE ANALYZER │ ───▶ │ CODE CORRECTOR│                │
│   │               │      │               │                │
│   │ Detect Errors │      │ Fix Errors    │                │
│   └───────────────┘      └───────┬───────┘                │
│                                  │                          │
│                                  ▼                          │
│                         ┌─────────────────┐                │
│                         │    VALIDATOR    │                │
│                         │                 │                │
│                         │ Compile        │                │
│                         │ Execute        │                │
│                         │ Functional Test│                │
│                         └────────┬────────┘                │
│                                  │                          │
│                                  ▼                          │
│                         ┌─────────────────┐                │
│                         │  FINAL REPORT   │                │
│                         └─────────────────┘                │
└─────────────────────────────────────────────────────────────┘
```

---

# 🧠 Core Components

| Component               | Responsibility                                            | Technology                |
| ----------------------- | --------------------------------------------------------- | ------------------------- |
| 🔍 **Code Analyzer**    | Detects syntax, indentation, logical and runtime problems | Python AST + custom rules |
| 🛠️ **Code Corrector**  | Automatically modifies common coding mistakes             | Python                    |
| 🎯 **Pipeline Manager** | Coordinates the complete workflow                         | Python                    |
| ✅ **Validator**         | Compiles, executes and tests corrected code               | Python Runtime            |
| 🧪 **Test Suite**       | Verifies analyzer and correction behaviour                | Python                    |

---

# 🔄 How The Pipeline Works

### 01 — 📝 Input

The user provides Python source code.

```python
def fibonacci_iterative(n):

    fib_sequence = [0, 1]

    for i in range(2, n):

    next_fib = fib_sequence[-1] + fib_sequence[-2]

    fib_sequence.append(next_fib)

    return fib_sequence
```

---

### 02 — 🔍 Analyze

The Analyzer examines the source code and identifies structural problems.

```text
✗ 3 ERROR(S) FOUND

1. SyntaxError
   Expected an indented block after 'for'

2. IndentationError
   Expected indented block

3. IndentationError
   Invalid indentation inside loop
```

---

### 03 — 🛠️ Correct

The Corrector analyzes the detected structure and generates repaired code.

```python
def fibonacci_iterative(n):

    fib_sequence = [0, 1]

    for i in range(2, n):

        next_fib = fib_sequence[-1] + fib_sequence[-2]

        fib_sequence.append(next_fib)

    return fib_sequence
```

---

### 04 — ✅ Validate

The Manager validates the corrected program.

```text
✓ Code compiled successfully

✓ Code executed successfully

✓ fibonacci_iterative(10)

✓ Output matches expected result
```

---

# 🎯 Demonstration

## Buggy Code

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

## 🔍 Detected Problems

```text
┌────────────────────────────────────────────┐
│             ANALYSIS REPORT                │
├────────────────────────────────────────────┤
│                                            │
│ ✗ Missing indentation                     │
│ ✗ Invalid loop body structure             │
│ ✗ Unexpected indentation level            │
│                                            │
└────────────────────────────────────────────┘
```

## 🛠️ Corrected Code

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

## ✅ Validation

```text
✓ Compilation successful
✓ Execution successful
✓ Function test successful
✓ Output verified

fibonacci_iterative(10)

[0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
```

---

# 🛠️ Technology Stack

<p align="center">

<img src="https://skillicons.dev/icons?i=python,git,github,vscode" />

</p>

### Core Technologies

| Technology          | Usage                      |
| ------------------- | -------------------------- |
| 🐍 Python           | Core development           |
| 🌳 AST              | Python syntax analysis     |
| ⚙️ `compile()`      | Compilation validation     |
| ▶️ `exec()`         | Runtime execution          |
| 🧪 Python Testing   | Functional validation      |
| 📦 Standard Library | Zero external dependencies |
| 🔧 Git              | Version control            |
| 🐙 GitHub           | Source-code management     |

---

# 📁 Project Structure

```text
crewai-code-analyzer/
│
├── 🧠 standalone_analyzer.py
│   └── Code Analyzer
│
├── 🛠️ standalone_corrector.py
│   └── Code Correction Engine
│
├── 🎯 standalone_manager.py
│   └── Pipeline Manager + Validation
│
├── 🚀 standalone_main.py
│   └── Main Entry Point
│
├── 🧪 test_analyzer.py
│   └── Analyzer Tests
│
├── 🧪 test_corrector.py
│   └── Correction Pipeline Tests
│
├── 📄 main.py
│   └── Original CrewAI Entry Point
│
├── ▶️ run_demo.py
│   └── Original CrewAI Demo
│
├── 📂 src/
│   ├── agents.py
│   ├── tasks.py
│   ├── crew_setup.py
│   └── code_interpreter_tool.py
│
└── 📖 README.md
```

---

# ⚡ Getting Started

## Prerequisites

```text
Python 3.8+
Git
```

No API key is required.

No database is required.

No internet connection is required.

No external Python packages are required.

---

## 📥 Installation

```bash
git clone https://github.com/kala3013/crewai-code-analyzer.git

cd crewai-code-analyzer
```

---

## ▶️ Run the Demo

```bash
python standalone_main.py
```

The program runs the complete:

```text
Analysis
   ↓
Correction
   ↓
Validation
   ↓
Final Report
```

pipeline using the built-in Fibonacci example.

---

# 🧪 Run Tests

### Test Analyzer

```bash
python test_analyzer.py
```

### Test Full Correction Pipeline

```bash
python test_corrector.py
```

---

# 🔌 Use As A Python Module

The components can also be imported into another Python application.

```python
from standalone_analyzer import CodeAnalyzer
from standalone_corrector import CodeCorrector
from standalone_manager import PipelineManager

analyzer = CodeAnalyzer()
corrector = CodeCorrector()

manager = PipelineManager(
    analyzer,
    corrector
)

results = manager.run_pipeline(your_code_string)

print(results["analysis_output"])
print(results["correction_output"])
print(results["validation"])
```

---

# 🎨 Analyze Your Own Code

Modify `EXAMPLE_CODE` inside:

```text
standalone_main.py
```

Example:

```python
EXAMPLE_CODE = '''
def calculate(x):

    if x > 0:

    print("Positive")

    return x
'''
```

Then execute:

```bash
python standalone_main.py
```

---

# 🧪 Test Coverage

| Scenario                    | Result                 |
| --------------------------- | ---------------------- |
| Fibonacci indentation error | ✅ Detected & corrected |
| Valid Python code           | ✅ Pass-through         |
| Missing colon               | ✅ Corrected            |
| Incorrect loop indentation  | ✅ Corrected            |
| Misplaced return            | ✅ Corrected            |
| Compilation validation      | ✅ Supported            |
| Runtime validation          | ✅ Supported            |
| Functional testing          | ✅ Supported            |

---

# 💡 Design Philosophy

This project demonstrates an important software-engineering concept:

> **Break a complex problem into specialized, independently testable components.**

Instead of creating one large program, the system separates responsibilities:

```text
             COMPLEX PROBLEM
                    │
                    ▼
          ┌──────────────────┐
          │ Modular Pipeline │
          └────────┬─────────┘
                   │
       ┌───────────┼───────────┐
       ▼           ▼           ▼
   Analyze      Correct      Validate
       │           │           │
       └───────────┼───────────┘
                   ▼
              Final Result
```

This makes the project easier to:

* Extend
* Test
* Debug
* Maintain
* Integrate with future AI systems

---

# 🔮 Future Improvements

The current system uses deterministic rule-based correction. Future versions could introduce:

### 🤖 AI-Powered Code Repair

Integrate LLMs for advanced semantic error correction.

### 🌐 Web Interface

Build a browser-based code editor using:

```text
React
+
Monaco Editor
+
Python Backend
```

### 📊 Interactive Error Dashboard

Display:

* Error locations
* Error categories
* Suggested fixes
* Before/after comparison
* Validation status

### 🔐 Secure Code Sandbox

Run untrusted code inside isolated environments using containerization.

### 🧠 Multi-Agent Architecture

Expand the pipeline into specialized agents:

```text
             Manager Agent
                  │
        ┌─────────┼─────────┐
        ▼         ▼         ▼
    Analyzer   Corrector   Tester
      Agent      Agent      Agent
        │         │         │
        └─────────┼─────────┘
                  ▼
            Final Report
```

---

# 📈 Project Highlights

```text
┌──────────────────────────────────────────────┐
│              PROJECT HIGHLIGHTS              │
├──────────────────────────────────────────────┤
│                                              │
│  🧠 Rule-Based Code Intelligence             │
│  🔍 Automated Error Detection                │
│  🛠️ Automated Code Correction                │
│  🎯 Modular Pipeline Architecture            │
│  ✅ Compilation & Runtime Validation         │
│  🧪 Functional Testing                       │
│  📦 Zero External Dependencies               │
│  🔌 Easily Extensible Architecture           │
│                                              │
└──────────────────────────────────────────────┘
```

---

# 🎓 Learning Outcomes

Through this project, the following concepts are demonstrated:

* Python Abstract Syntax Tree
* Static code analysis
* Error classification
* Automated code transformation
* Indentation parsing
* Runtime execution
* Modular software architecture
* Pipeline design
* Functional testing
* Error handling
* Test-driven development concepts
* AI-agent-inspired architecture

---

# 👨‍💻 Developer

<p align="center">

### **Kalanidhi M C**

**Computer Science Engineering Student | Software Developer | Full Stack & AI Enthusiast**

<br>

<a href="https://github.com/kala3013">
<img src="https://img.shields.io/badge/GitHub-kala3013-181717?style=for-the-badge&logo=github">
</a>

<a href="https://www.linkedin.com/in/kalanidhi-m-c-b568782a5/">
<img src="https://img.shields.io/badge/LinkedIn-Kalanidhi%20M%20C-0A66C2?style=for-the-badge&logo=linkedin">
</a>

<a href="mailto:kalanidhimurugan@gmail.com">
<img src="https://img.shields.io/badge/Email-kalanidhimurugan%40gmail.com-EA4335?style=for-the-badge&logo=gmail&logoColor=white">
</a>

</p>

---

# ⭐ Support

If you find this project useful or interesting:

⭐ **Star the repository**

🍴 **Fork the project**

🐛 **Report issues**

💡 **Suggest improvements**

🤝 **Contribute**

---

<p align="center">

### 🧠 Analyze Code. 🛠️ Fix Errors. ✅ Validate Results.

**Built with Python & curiosity.**

</p>
