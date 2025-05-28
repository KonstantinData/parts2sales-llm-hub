# lang_en.py

# ------------------------------------------

# Purpose:
# Define idiomatic, structural, lexical, and tonal patterns for English prompts

# Goals:
# - Enable automated linguistic validation and quality scoring

# Use Cases:
# - Used by prompt validation tools for English prompt checking


# English idiomatic expressions for natural phrasing
# -------------------------------------------------
def idiomatic_expressions():
    return [
        "hit the ground running",
        "rule of thumb",
        "think outside the box",
        "back to the drawing board",
    ]


# Action verbs indicating clarity of instruction
# ---------------------------------------------
def action_keywords():
    return ["analyze", "create", "generate", "identify", "derive"]


# Words indicating logical structure
# ----------------------------------
def structure_keywords():
    return ["first", "then", "next", "finally", "in conclusion"]


# Phrases that should be avoided due to awkwardness
# --------------------------------------------------
def lexical_warnings():
    return ["analyze of", "do a derivation"]


# Tone-inappropriate words or phrases
# -----------------------------------
def tone_blacklist():
    return ["whatever", "damn", "wtf"]


# Check for use of actionable phrasing
# ------------------------------------
def is_actionable(text):
    return any(word in text.lower() for word in action_keywords())


# Detect structured flow using structural markers
# ------------------------------------------------
def has_structure(text):
    return sum(1 for word in structure_keywords() if word in text.lower()) >= 2


# Check for presence of idiomatic English phrasing
# -------------------------------------------------
def has_idiom(text):
    return any(phrase in text for phrase in idiomatic_expressions())


# Check for known incorrect lexical patterns
# ------------------------------------------
def violates_lexical_rules(text):
    return any(combo in text for combo in lexical_warnings())


# Detect tonal violations (informal, unprofessional)
# --------------------------------------------------
def has_tone_issue(text):
    return any(term in text.lower() for term in tone_blacklist())


# Explanation map for validation result keys
# ------------------------------------------
def explanations():
    return {
        "grammar_check": "Fix grammar issues for clearer understanding.",
        "idiomatic_check": "Consider using idiomatic phrases for natural tone.",
        "task_clarity": "Clarify the instruction using action verbs like 'generate' or 'identify'.",
        "structure_check": "Add structure markers like 'first', 'then', 'finally' to guide the flow.",
        "lexical_fit": "Avoid awkward phrasing or uncommon combinations.",
        "tone_check": "Use a professional and neutral tone.",
        "translation_integrity": "Check that structure and intent match the source.",
    }
