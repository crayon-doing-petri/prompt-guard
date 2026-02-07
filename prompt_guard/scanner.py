"""
Prompt Guard - Pattern scanner.

Runs all pattern sets against a single text string.
Used for scanning both original and decoded text.
"""

import re
from typing import Tuple, List

from prompt_guard.models import Severity
from prompt_guard.patterns import (
    CRITICAL_PATTERNS,
    SECRET_PATTERNS,
    PATTERNS_EN, PATTERNS_KO, PATTERNS_JA, PATTERNS_ZH,
    PATTERNS_RU, PATTERNS_ES, PATTERNS_DE, PATTERNS_FR,
    PATTERNS_PT, PATTERNS_VI,
    SCENARIO_JAILBREAK, EMOTIONAL_MANIPULATION, AUTHORITY_RECON,
    COGNITIVE_MANIPULATION, PHISHING_SOCIAL_ENG, SYSTEM_FILE_ACCESS,
    MALWARE_DESCRIPTION, INDIRECT_INJECTION, CONTEXT_HIJACKING,
    SAFETY_BYPASS,
)


def scan_text_for_patterns(text: str) -> Tuple[List[str], List[str], Severity]:
    """
    Run all pattern sets against a single text string.
    Returns (reasons, patterns_matched, max_severity).
    Used for scanning both original and decoded text.
    """
    reasons = []
    patterns_matched = []
    max_severity = Severity.SAFE
    text_lower = text.lower()

    # Critical patterns
    for pattern in CRITICAL_PATTERNS:
        try:
            if re.search(pattern, text_lower, re.IGNORECASE):
                reasons.append("critical_pattern")
                patterns_matched.append(pattern)
                max_severity = Severity.CRITICAL
        except re.error:
            pass

    # Secret patterns
    for lang, patterns in SECRET_PATTERNS.items():
        for pattern in patterns:
            try:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    max_severity = Severity.CRITICAL
                    reasons.append(f"secret_request_{lang}")
                    patterns_matched.append(f"{lang}:secret:{pattern[:40]}")
            except re.error:
                pass

    # Language-specific patterns
    all_lang_patterns = [
        (PATTERNS_EN, "en"), (PATTERNS_KO, "ko"), (PATTERNS_JA, "ja"),
        (PATTERNS_ZH, "zh"), (PATTERNS_RU, "ru"), (PATTERNS_ES, "es"),
        (PATTERNS_DE, "de"), (PATTERNS_FR, "fr"), (PATTERNS_PT, "pt"),
        (PATTERNS_VI, "vi"),
    ]
    severity_map = {
        "instruction_override": Severity.HIGH,
        "role_manipulation": Severity.MEDIUM,
        "system_impersonation": Severity.HIGH,
        "jailbreak": Severity.HIGH,
        "output_manipulation": Severity.LOW,
        "data_exfiltration": Severity.CRITICAL,
        "social_engineering": Severity.HIGH,
    }
    for pattern_set, lang in all_lang_patterns:
        for category, patterns in pattern_set.items():
            for pattern in patterns:
                try:
                    if re.search(pattern, text_lower, re.IGNORECASE):
                        cat_severity = severity_map.get(category, Severity.MEDIUM)
                        if cat_severity.value > max_severity.value:
                            max_severity = cat_severity
                        reasons.append(f"{category}_{lang}")
                        patterns_matched.append(f"{lang}:{pattern[:50]}")
                except re.error:
                    pass

    # Versioned pattern sets
    versioned_sets = [
        (SCENARIO_JAILBREAK, "scenario_jailbreak", Severity.HIGH),
        (EMOTIONAL_MANIPULATION, "emotional_manipulation", Severity.HIGH),
        (AUTHORITY_RECON, "authority_recon", Severity.MEDIUM),
        (COGNITIVE_MANIPULATION, "cognitive_manipulation", Severity.MEDIUM),
        (PHISHING_SOCIAL_ENG, "phishing_social_eng", Severity.CRITICAL),
        (SYSTEM_FILE_ACCESS, "system_file_access", Severity.CRITICAL),
        (MALWARE_DESCRIPTION, "malware_description", Severity.HIGH),
        (INDIRECT_INJECTION, "indirect_injection", Severity.HIGH),
        (CONTEXT_HIJACKING, "context_hijacking", Severity.MEDIUM),
        (SAFETY_BYPASS, "safety_bypass", Severity.HIGH),
    ]
    for patterns, category, severity in versioned_sets:
        for pattern in patterns:
            try:
                if re.search(pattern, text_lower, re.IGNORECASE):
                    if severity.value > max_severity.value:
                        max_severity = severity
                    if category not in reasons:
                        reasons.append(category)
                    patterns_matched.append(f"versioned:{category}:{pattern[:40]}")
            except re.error:
                pass

    return reasons, patterns_matched, max_severity
