"""
DEPRECATED: Use 'prompt_guard' instead of 'scripts.detect'.

This module exists for backward compatibility only and will be removed in v4.0.
"""

import warnings
warnings.warn(
    "Import from 'prompt_guard' instead of 'scripts.detect'. "
    "The 'scripts.detect' module is deprecated and will be removed in v4.0.",
    DeprecationWarning,
    stacklevel=2,
)

# Re-export everything from the new package
from prompt_guard import *  # noqa: F401,F403
from prompt_guard.engine import PromptGuard  # noqa: F401
from prompt_guard.models import Severity, Action, DetectionResult, SanitizeResult  # noqa: F401
from prompt_guard.cli import main  # noqa: F401

# Re-export all pattern constants for code that accesses them directly
from prompt_guard.patterns import *  # noqa: F401,F403
from prompt_guard.normalizer import HOMOGLYPHS  # noqa: F401

if __name__ == "__main__":
    main()
