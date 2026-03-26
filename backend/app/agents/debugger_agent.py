"""
AI Mentor - Debugger Agent.

Analyzes code errors, explains bugs, provides corrected code, and suggests best practices.
"""

from typing import Dict, Any, Optional
from loguru import logger
from .base_agent import invoke_agent
from .prompts.debugger import DEBUGGER_SYSTEM_PROMPT


async def debug_code(
    code: str,
    error_message: Optional[str] = None,
    expected_behavior: Optional[str] = None,
    topic: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Analyze code for bugs and provide fixes.

    Args:
        code: The buggy code
        error_message: Error output (if any)
        expected_behavior: What the code should do
        topic: Learning context topic

    Returns:
        Debug analysis with fix and explanation
    """
    system_prompt = DEBUGGER_SYSTEM_PROMPT.format(
        code=code,
        error=error_message or "No error message provided",
        expected=expected_behavior or "Not specified",
        topic=topic or "General programming",
    )

    user_message = f"""Please analyze this code and help me debug it:

```python
{code}
```

Error: {error_message or 'No specific error, but code does not work as expected'}
Expected: {expected_behavior or 'Not specified'}
"""

    logger.info(f"Debugging code for topic: {topic}")
    result = await invoke_agent(system_prompt, user_message, parse_json=True)

    # Ensure required fields
    if "issue_summary" not in result:
        result.setdefault("issue_summary", "Analysis could not be completed")
    if "root_cause" not in result:
        result.setdefault("root_cause", "Unable to determine root cause")
    if "corrected_code" not in result:
        result.setdefault("corrected_code", code)
    if "explanation" not in result:
        result.setdefault("explanation", "Please review the code manually")
    if "best_practices" not in result:
        result.setdefault("best_practices", [])
    if "related_concepts" not in result:
        result.setdefault("related_concepts", [])

    return result
