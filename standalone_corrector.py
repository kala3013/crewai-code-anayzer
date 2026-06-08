"""
Code Corrector - Fixes Python code indentation errors.
Simple robust approach: for each header, body = consecutive content lines until continuation/dedent.
For for/while loops, all lines at same indent become body (the bug fix), 
then the last return goes back to header level.
"""
import traceback


class CodeCorrector:
    def __init__(self):
        self.fixes_applied = []

    def correct(self, code: str, error_report: str = "") -> str:
        self.fixes_applied = []
        lines = code.split('\n')
        lines = [l.rstrip() for l in lines]
        lines = self._fix_missing_colons(lines)
        lines = self._fix_indentation(lines)
        cleaned = []
        prev_empty = False
        for line in lines:
            if not line.strip():
                if prev_empty:
                    continue
                prev_empty = True
            else:
                prev_empty = False
            cleaned.append(line)
        return '\n'.join(cleaned).strip()

    def _fix_missing_colons(self, lines):
        block_keywords = ['if', 'elif', 'else', 'for', 'while', 'try', 'except', 'finally', 'with', 'def', 'class']
        result = []
        for i, line in enumerate(lines):
            s = line.strip()
            if not s or s.startswith('#'):
                result.append(line)
                continue
            needs = False
            for kw in block_keywords:
                if s == kw or s.startswith(kw + ' '):
                    if not s.endswith(':'):
                        needs = True
                        break
            if needs:
                self.fixes_applied.append(f"Line {i + 1}: Added missing ':'")
                result.append(line.rstrip() + ':')
            else:
                result.append(line)
        return result

    def _fix_indentation(self, lines):
        INDENT = 4
        n = len(lines)

        # Classify
        is_blank = [False] * n
        stripped = [''] * n
        orig_indent = [0] * n
        is_header = [False] * n
        is_cont = [False] * n
        is_return = [False] * n
        is_loop = [False] * n  # for/while
        is_ifelif = [False] * n  # if/elif

        for i, line in enumerate(lines):
            s = line.strip()
            if not s or s.startswith('#'):
                is_blank[i] = True
                continue
            stripped[i] = s
            orig_indent[i] = len(line) - len(line.lstrip())
            is_header[i] = s.rstrip().endswith(':')
            is_cont[i] = any(s.startswith(k) for k in ['else:', 'elif ', 'except ', 'finally:'])
            is_return[i] = s.startswith('return ')
            is_loop[i] = s.startswith(('for ', 'while ')) and is_header[i]
            is_ifelif[i] = s.startswith(('if ', 'elif ')) and is_header[i] and not is_cont[i]

        result = list(lines)

        # Process each header to fix its body indentation
        for i in range(n):
            if is_blank[i] or not is_header[i]:
                continue

            header_indent = orig_indent[i]
            header_level = header_indent // INDENT

            body_indices = []
            j = i + 1
            while j < n:
                if is_blank[j]:
                    j += 1
                    continue
                if is_header[j] or is_cont[j]:
                    break
                # Line at less indent: closes the body (this line is sibling of header)
                if orig_indent[j] < header_indent:
                    break
                # For if/elif/else/except/finally etc: line at SAME indent is a sibling
                if is_ifelif[i] and orig_indent[j] == header_indent:
                    break
                # For continuity headers (elif is_cont but still a header)
                if is_cont[i] and orig_indent[j] == header_indent:
                    break
                # For for/while loops: line at same indent IS the body (the bug we fix)
                body_indices.append(j)
                j += 1

            if body_indices:
                new_indent = (header_level + 1) * INDENT
                for k in body_indices:
                    if not is_blank[k]:
                        result[k] = ' ' * new_indent + stripped[k]

        # Post-process for/while: the LAST body line that's a return goes back to header level
        for i in range(n):
            if is_blank[i] or not is_loop[i]:
                continue

            header_indent = orig_indent[i]

            # Find last body line
            j = i + 1
            last_body = None
            while j < n:
                if is_blank[j]:
                    j += 1
                    continue
                if is_header[j] or is_cont[j]:
                    break
                if orig_indent[j] < header_indent:
                    break
                if is_ifelif[j]:  # if/elif inside the loop would be at more indent
                    # Don't skip - it's part of the body, collect its body too
                    pass
                # Stop at lines that are same indent as header (siblings, not body)
                if orig_indent[j] == header_indent and not is_return[j]:
                    # For non-return lines at same indent: could be body or sibling
                    # Since we already identified body as all lines until a break condition,
                    # just track it
                    pass
                last_body = j
                j += 1

            if last_body is not None and is_return[last_body]:
                result[last_body] = ' ' * header_indent + stripped[last_body]

        # Record fixes
        for i in range(n):
            if not is_blank[i]:
                oi = orig_indent[i]
                ci = len(result[i]) - len(result[i].lstrip())
                if oi != ci:
                    self.fixes_applied.append(f"Line {i + 1}: Corrected indent ({oi} -> {ci})")

        return result

    def get_fixes_summary(self):
        if not self.fixes_applied:
            return "  No fixes were needed."
        return '\n'.join(f"  ✓ {fix}" for fix in self.fixes_applied)