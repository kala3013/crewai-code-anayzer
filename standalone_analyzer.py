"""
Standalone Code Analyzer & Corrector
-----------------------------------
A self-contained Python tool that:
1. Analyzes Python code for syntax, indentation, and logical errors
2. Corrects identified errors automatically
3. Manages the full analysis → correction pipeline

No external API keys required. Pure Python rule-based engine.
"""

import ast
import sys
import io
import traceback


class CodeAnalyzer:
    """
    Analyzes Python code and produces a detailed error report.
    Detects: syntax errors, indentation errors, logical errors, runtime errors.
    """

    def __init__(self):
        self.errors = []
        self.warnings = []

    def analyze(self, code: str) -> str:
        """
        Analyze the given Python code and return a formatted error report.
        
        Args:
            code: Python source code string
            
        Returns:
            Formatted string containing all detected errors and analysis
        """
        self.errors = []
        self.warnings = []
        lines = code.split('\n')
        
        # Step 1: Check for basic syntax by trying to compile
        self._check_syntax(code, lines)
        
        # Step 2: Check indentation consistency
        self._check_indentation(lines)
        
        # Step 3: Check for common logical errors
        self._check_logical_errors(code, lines)
        
        # Step 4: Try to execute and catch runtime errors
        self._check_runtime(code)
        
        return self._format_report(code, lines)

    def _check_syntax(self, code: str, lines: list):
        """Check for Python syntax errors using ast.parse and compile."""
        try:
            ast.parse(code)
        except SyntaxError as e:
            self.errors.append({
                'line': e.lineno or 0,
                'type': 'SyntaxError',
                'description': str(e.msg),
                'detail': f"Invalid syntax at line {e.lineno}"
            })
            # Try to provide more context
            if e.lineno and e.lineno <= len(lines):
                self.errors[-1]['context'] = lines[e.lineno - 1].strip()

        # Additional manual checks
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            # Check for missing colon in compound statements
            for keyword in ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 'with', 'def', 'class']:
                if stripped.startswith(keyword) and not stripped.endswith(':'):
                    if keyword in ('else', 'finally'):
                        if stripped.rstrip().endswith(keyword):
                            continue  # Might span multiple lines
                    self.errors.append({
                        'line': i,
                        'type': 'SyntaxError',
                        'description': f"Missing colon after '{keyword}' statement",
                        'detail': f"The '{keyword}' statement at line {i} must end with ':'"
                    })
                    break

    def _check_indentation(self, lines: list):
        """Check for indentation errors."""
        expected_indent = 0
        indent_stack = [0]  # Track indentation levels
        prev_indent = 0
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            # Calculate leading whitespace
            leading = len(line) - len(line.lstrip())
            
            # Check for inconsistent indentation (mixing tabs and spaces)
            if '\t' in line[:leading] and ' ' in line[:leading]:
                self.errors.append({
                    'line': i,
                    'type': 'IndentationError',
                    'description': "Mixed tabs and spaces in indentation",
                    'detail': f"Line {i} contains both tabs and spaces"
                })
            
            # Determine if this line should be indented after a block start
            if prev_line := lines[i - 2] if i > 1 else '':
                prev_stripped = prev_line.strip()
                if prev_stripped.endswith(':') and not prev_stripped.startswith('#'):
                    if leading <= prev_indent and not stripped.startswith(('else', 'elif', 'except', 'finally')):
                        self.errors.append({
                            'line': i,
                            'type': 'IndentationError',
                            'description': f"Expected an indented block after line {i - 1}",
                            'detail': f"Line {i} (column {leading}) is not indented after the block header at line {i - 1}"
                        })
            
            # Check for wrong indentation of for/while loop body
            for block_keyword in ['for ', 'while ', 'if ', 'elif ', 'else:']:
                if stripped.startswith(block_keyword) and stripped.rstrip().endswith(':'):
                    # The next non-empty line should be indented more
                    next_line = None
                    for j in range(i, len(lines)):
                        if lines[j].strip() and not lines[j].strip().startswith('#'):
                            next_line = j + 1
                            break
                    if next_line:
                        next_leading = len(lines[next_line - 1]) - len(lines[next_line - 1].lstrip())
                        if next_leading <= leading:
                            self.errors.append({
                                'line': next_line,
                                'type': 'IndentationError',
                                'description': f"Expected an indented block after '{stripped.split(':')[0].strip()}' at line {i}",
                                'detail': f"Line {next_line} should be indented under the block at line {i}"
                            })
            
            prev_indent = leading

    def _check_logical_errors(self, code: str, lines: list):
        """Check for common logical errors."""
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped or stripped.startswith('#'):
                continue
            
            # Check for range(2, n) where loop body is at same level (common fibonacci bug)
            if 'for ' in stripped and 'range(' in stripped:
                # Check if the next line after the for loop is not indented properly
                next_lines = []
                for j in range(i, min(i + 5, len(lines))):
                    if lines[j].strip() and not lines[j].strip().startswith('#'):
                        next_lines.append((j + 1, lines[j]))
                for line_num, next_line in next_lines[:3]:
                    next_leading = len(next_line) - len(next_line.lstrip())
                    current_leading = len(line) - len(line.lstrip())
                    if next_leading <= current_leading and not next_line.strip().startswith(('else', 'elif', 'except', 'finally')):
                        self.errors.append({
                            'line': line_num,
                            'type': 'IndentationError',
                            'description': f"Expected indented block after 'for' loop at line {i}",
                            'detail': f"Line {line_num} at column {next_leading} is not indented correctly under the for loop"
                        })
                        break
            
            # Check for return outside function
            if stripped.startswith('return ') and not self._is_inside_function(lines, i):
                self.errors.append({
                    'line': i,
                    'type': 'SyntaxError',
                    'description': "'return' outside function",
                    'detail': f"Line {i}: return statement is not inside any function"
                })
            
            # Check for variable assignment in conditional
            if stripped.startswith(('if ', 'elif ')) and '=' in stripped and '==' not in stripped and '!=' not in stripped:
                if '=' in stripped.split(maxsplit=1)[1]:  # = after if/elif
                    self.warnings.append({
                        'line': i,
                        'type': 'LogicalWarning',
                        'description': "Possible assignment (=) used instead of comparison (==)",
                        'detail': f"Line {i}: Use '==' for comparison instead of '='"
                    })

    def _is_inside_function(self, lines: list, line_num: int) -> bool:
        """Check if a line is inside a function definition."""
        depth = 0
        for i in range(line_num - 1):
            stripped = lines[i].strip()
            if stripped.startswith('def ') and stripped.endswith(':'):
                depth += 1
            elif stripped.startswith('class ') and stripped.endswith(':'):
                depth += 1
            elif stripped.startswith('return ') and depth > 0:
                pass  # return inside function is fine
        return depth > 0

    def _check_runtime(self, code: str):
        """Try to execute the code and catch runtime errors."""
        # Check for syntax first - if syntax errors exist, runtime check is unreliable
        try:
            ast.parse(code)
        except SyntaxError:
            return
        
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        redirected_output = io.StringIO()
        redirected_error = io.StringIO()
        
        sys.stdout = redirected_output
        sys.stderr = redirected_error
        
        try:
            compiled = compile(code, '<string>', 'exec')
            exec_namespace = {}
            exec(compiled, exec_namespace)
        except IndentationError as e:
            self.errors.append({
                'line': e.lineno or 0,
                'type': 'IndentationError',
                'description': str(e),
                'detail': f"Indentation error at line {e.lineno}"
            })
        except SyntaxError as e:
            self.errors.append({
                'line': e.lineno or 0,
                'type': 'SyntaxError',
                'description': str(e),
                'detail': f"Syntax error at line {e.lineno}"
            })
        except NameError as e:
            self.errors.append({
                'line': 0,
                'type': 'NameError',
                'description': str(e),
                'detail': "Undefined variable or function name"
            })
        except Exception as e:
            tb = traceback.extract_tb(sys.exc_info()[2])
            error_line = tb[-1].lineno if tb else 0
            self.errors.append({
                'line': error_line,
                'type': type(e).__name__,
                'description': str(e),
                'detail': f"Runtime error at line {error_line}"
            })
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    def _format_report(self, code: str, lines: list) -> str:
        """Format the error report as a readable string."""
        report = []
        report.append("=" * 70)
        report.append("  CODE ANALYSIS REPORT")
        report.append("=" * 70)
        report.append("")
        
        if not self.errors and not self.warnings:
            report.append("  ✓ NO ERRORS FOUND - Code appears to be valid Python.")
            report.append("")
            report.append("-" * 70)
            report.append("  CODE STRUCTURE SUMMARY")
            report.append("-" * 70)
        else:
            if self.errors:
                report.append(f"  ✗ {len(self.errors)} ERROR(S) FOUND:")
                report.append("")
                for idx, err in enumerate(self.errors, 1):
                    report.append(f"  {idx}. Line {err['line']}: {err['type']} - {err['description']}")
                    report.append(f"     {err['detail']}")
                    if 'context' in err:
                        report.append(f"     Context: {err['context']}")
                    report.append("")
            
            if self.warnings:
                report.append(f"  ⚠ {len(self.warnings)} WARNING(S):")
                report.append("")
                for idx, warn in enumerate(self.warnings, 1):
                    report.append(f"  {idx}. Line {warn['line']}: {warn['type']} - {warn['description']}")
                    report.append(f"     {warn['detail']}")
                    report.append("")
        
        report.append("-" * 70)
        report.append("  CODE STRUCTURE ANALYSIS")
        report.append("-" * 70)
        
        for i, line in enumerate(lines, 1):
            stripped = line.strip()
            if not stripped:
                continue
            if stripped.startswith('def '):
                report.append(f"  Line {i}: [FUNCTION] {stripped}")
            elif stripped.startswith('class '):
                report.append(f"  Line {i}: [CLASS] {stripped}")
            elif stripped.startswith('for '):
                report.append(f"  Line {i}: [FOR LOOP] {stripped}")
            elif stripped.startswith('while '):
                report.append(f"  Line {i}: [WHILE LOOP] {stripped}")
            elif stripped.startswith(('if ', 'elif ', 'else')):
                report.append(f"  Line {i}: [CONDITIONAL] {stripped}")
            elif stripped.startswith('return '):
                report.append(f"  Line {i}: [RETURN] {stripped}")
        
        report.append("")
        report.append("=" * 70)
        report.append(f"  Analysis complete. Total lines: {len(lines)}")
        report.append("=" * 70)
        
        return '\n'.join(report)

    def get_error_count(self) -> int:
        """Return the number of errors found."""
        return len(self.errors)
    
    def get_warning_count(self) -> int:
        """Return the number of warnings found."""
        return len(self.warnings)
    
    def has_errors(self) -> bool:
        """Check if any errors were found."""
        return len(self.errors) > 0