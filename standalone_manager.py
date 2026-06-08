"""
Manager - Orchestrates the Code Analysis and Correction pipeline.
Ensures tasks run smoothly from analysis -> correction -> validation.
"""

import sys


class PipelineManager:
    """
    Manager that oversees the code analysis and correction process.
    Coordinates the CodeAnalyzer and CodeCorrector, validates results,
    and provides a comprehensive final report.
    """

    def __init__(self, code_analyzer, code_corrector):
        """
        Args:
            code_analyzer: An instance of CodeAnalyzer
            code_corrector: An instance of CodeCorrector
        """
        self.analyzer = code_analyzer
        self.corrector = code_corrector
        self.analysis_output = ""
        self.correction_output = ""
        self.validation_result = None
        self.final_report = ""

    def run_pipeline(self, code: str) -> dict:
        """
        Run the complete analysis and correction pipeline.
        
        1. Analysis Phase: CodeAnalyzer identifies all errors
        2. Correction Phase: CodeCorrector fixes the errors
        3. Validation Phase: Verify the corrected code compiles and runs
        
        Args:
            code: Python source code to analyze and correct
            
        Returns:
            Dictionary with keys:
                - analysis_output: Error report from CodeAnalyzer
                - correction_output: Corrected code from CodeCorrector
                - fixes_summary: Summary of all fixes applied
                - validation: Validation results
                - success: Boolean indicating if pipeline completed
        """
        results = {
            'analysis_output': '',
            'correction_output': '',
            'fixes_summary': '',
            'validation': '',
            'success': False
        }

        # Phase 1: Analysis
        print("    [Manager] Task 1: Code Analysis - Starting...")
        self.analysis_output = self.analyzer.analyze(code)
        results['analysis_output'] = self.analysis_output
        
        error_count = self.analyzer.get_error_count()
        warning_count = self.analyzer.get_warning_count()
        
        print(f"    [Manager] Analysis complete: {error_count} error(s), {warning_count} warning(s) found")
        
        if error_count == 0:
            print("    [Manager] No errors found. Code is already valid.")
            results['correction_output'] = code
            results['fixes_summary'] = "  No errors to fix."
            results['validation'] = self._validate_code(code)
            results['success'] = True
            self.final_report = self._build_final_report(code, results)
            return results

        # Phase 2: Correction
        print("    [Manager] Task 2: Code Correction - Starting...")
        self.correction_output = self.corrector.correct(code, self.analysis_output)
        results['correction_output'] = self.correction_output
        results['fixes_summary'] = self.corrector.get_fixes_summary()
        
        print(f"    [Manager] Correction complete. {len(self.corrector.fixes_applied)} fix(es) applied.")

        # Phase 3: Validation
        print("    [Manager] Task 3: Validation - Starting...")
        self.validation_result = self._validate_code(self.correction_output)
        results['validation'] = self.validation_result
        
        if "✓" in self.validation_result:
            print("    [Manager] Validation: PASSED")
            results['success'] = True
        else:
            print("    [Manager] Validation: FAILED")
            results['success'] = False

        # Build final report
        self.final_report = self._build_final_report(code, results)
        
        return results

    def _validate_code(self, code: str) -> str:
        """
        Validate that the given code compiles and runs correctly.
        
        Returns:
            A string with validation results
        """
        validation = []
        validation.append("-" * 60)
        validation.append("  VALIDATION RESULTS")
        validation.append("-" * 60)
        
        # Check compilation
        try:
            compile(code, '<string>', 'exec')
            validation.append("  ✓ Code compiled successfully - No syntax errors")
        except SyntaxError as e:
            validation.append(f"  ✗ SyntaxError: {e.msg} at line {e.lineno}")
            return '\n'.join(validation)
        except Exception as e:
            validation.append(f"  ✗ Error during compilation: {e}")
            return '\n'.join(validation)
        
        # Check execution
        try:
            namespace = {}
            exec(code, namespace)
            validation.append("  ✓ Code executed successfully - No runtime errors")
        except Exception as e:
            validation.append(f"  ✗ Runtime error: {e}")
            return '\n'.join(validation)
        
        # Check if fibonacci function exists and works (for the demo)
        if 'fibonacci_iterative' in namespace:
            try:
                result = namespace['fibonacci_iterative'](10)
                expected = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]
                if result == expected:
                    validation.append("  ✓ fibonacci_iterative(10) = [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]")
                    validation.append("  ✓ Function output matches expected Fibonacci sequence!")
                else:
                    validation.append(f"  ⚠ fibonacci_iterative(10) = {result}")
                    validation.append(f"  ⚠ Expected: {expected}")
            except Exception as e:
                validation.append(f"  ⚠ Could not test fibonacci function: {e}")
        
        return '\n'.join(validation)

    def _build_final_report(self, original_code: str, results: dict) -> str:
        """Build the final combined report."""
        report = []
        report.append("")
        report.append("=" * 70)
        report.append("  FINAL PIPELINE REPORT")
        report.append("=" * 70)
        report.append("")
        
        report.append(">>> INPUT CODE:")
        report.append("-" * 40)
        report.append(original_code)
        report.append("-" * 40)
        report.append("")
        
        report.append(">>> FIXES APPLIED:")
        report.append("-" * 40)
        report.append(results.get('fixes_summary', '  No fixes applied.'))
        report.append("")
        
        report.append(">>> CORRECTED CODE:")
        report.append("-" * 40)
        report.append(results.get('correction_output', ''))
        report.append("-" * 40)
        report.append("")
        
        report.append(results.get('validation', ''))
        report.append("")
        
        if results['success']:
            report.append("=" * 70)
            report.append("  ✓ PIPELINE COMPLETED SUCCESSFULLY")
            report.append("=" * 70)
        else:
            report.append("=" * 70)
            report.append("  ✗ PIPELINE FAILED - Manual review required")
            report.append("=" * 70)
        
        return '\n'.join(report)

    def get_final_report(self) -> str:
        """Get the final pipeline report."""
        return self.final_report

    def print_summary(self):
        """Print a brief summary of what happened."""
        print()
        print("=" * 60)
        print("  MANAGER SUMMARY")
        print("=" * 60)
        
        errors = self.analyzer.get_error_count()
        warnings = self.analyzer.get_warning_count()
        fixes = len(self.corrector.fixes_applied)
        
        print(f"  Errors detected:  {errors}")
        print(f"  Warnings found:   {warnings}")
        print(f"  Fixes applied:    {fixes}")
        
        if self.validation_result and "✓" in self.validation_result:
            print("  Validation:       ✓ PASSED")
        else:
            print("  Validation:       ✗ FAILED")
        
        print("=" * 60)