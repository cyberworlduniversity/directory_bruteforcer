"""Regression tests for bounded HTTP response handling."""

import ast
import unittest
from pathlib import Path


class DirectoryBruteforcerResponseTests(unittest.TestCase):
    def test_requests_are_streamed_inside_a_context_manager(self):
        source_path = Path(__file__).with_name("directory_bruteforcer.py")
        tree = ast.parse(source_path.read_text(encoding="utf-8"))

        streamed_request_lines = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.With):
                continue
            for item in node.items:
                call = item.context_expr
                if not isinstance(call, ast.Call):
                    continue
                func = call.func
                if (
                    isinstance(func, ast.Attribute)
                    and func.attr == "get"
                    and isinstance(func.value, ast.Name)
                    and func.value.id == "requests"
                ):
                    stream_enabled = any(
                        keyword.arg == "stream"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is True
                        for keyword in call.keywords
                    )
                    if stream_enabled:
                        streamed_request_lines.append(call.lineno)

        self.assertTrue(
            streamed_request_lines,
            "Directory scan requests must stream responses and close them via a context manager.",
        )


if __name__ == "__main__":
    unittest.main()
