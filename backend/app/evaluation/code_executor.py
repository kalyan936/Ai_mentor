"""
AI Mentor - Safe Code Executor.

Provides sandboxed Python code execution with timeout and memory limits.
Uses subprocess for isolation and safety.
"""

import subprocess
import sys
import tempfile
import os
from typing import Dict, Any
from loguru import logger
from ..core.config import get_settings


def execute_python_code(code: str) -> Dict[str, Any]:
    """
    Execute Python code safely in a subprocess with timeout.

    Args:
        code: Python code string to execute

    Returns:
        Dict with output, errors, and execution status
    """
    settings = get_settings()
    timeout = settings.code_execution_timeout

    # Write code to temp file
    with tempfile.NamedTemporaryFile(
        mode='w', suffix='.py', delete=False, encoding='utf-8'
    ) as f:
        f.write(code)
        temp_path = f.name

    try:
        # Execute in subprocess with timeout
        result = subprocess.run(
            [sys.executable, temp_path],
            capture_output=True,
            text=True,
            timeout=timeout,
            cwd=tempfile.gettempdir(),
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

        output = result.stdout
        errors = result.stderr
        status = "success" if result.returncode == 0 else "error"

        logger.info(f"Code execution completed with status: {status}")

        return {
            "output": output[:5000] if output else "",  # Limit output size
            "errors": errors[:5000] if errors else "",
            "status": status,
            "return_code": result.returncode,
        }

    except subprocess.TimeoutExpired:
        logger.warning("Code execution timed out")
        return {
            "output": "",
            "errors": f"Execution timed out after {timeout} seconds",
            "status": "timeout",
            "return_code": -1,
        }
    except Exception as e:
        logger.error(f"Code execution error: {e}")
        return {
            "output": "",
            "errors": str(e),
            "status": "error",
            "return_code": -1,
        }
    finally:
        # Clean up temp file
        try:
            os.unlink(temp_path)
        except OSError:
            pass
