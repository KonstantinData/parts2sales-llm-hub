# lang_de.py

# ------------------------------------------

# Purpose:
# Define idiomatic, structural, lexical, and tonal patterns for German prompts

# Goals:
# - Enable automated linguistic validation and quality scoring

# Use Cases:
# - Used by prompt validation tools for German prompt checking


# German idiomatic expressions for natural phrasing
# ------------------------------------------------
def idiomatic_expressions():
    return [
        "den Nagel auf den Kopf treffen",
        "das Kind beim Namen nennen",
        "ins kalte Wasser springen",
        "zwei Fliegen mit einer Klappe schlagen",
    ]


# Action verbs indicating clarity of instruction
# ---------------------------------------------
def action_keywords():
    return ["analysiere", "erstelle", "generiere", "identifiziere", "leite ab"]


# Words indicating logical structure
# ----------------------------------
def structure_keywords():
    return ["zuerst", "anschließend", "dann", "schließlich", "abschließend"]


# Phrases that should be avoided due to awkwardness
# --------------------------------------------------
def lexical_warnings():
    return ["durchführen eine Analyse", "machen eine Ableitung"]


# Tone-inappropriate words or phrases
# ------------------------------------
def tone_blacklist():
    return ["scheiß", "was soll der mist", "mir doch egal"]


# Check for use of actionable phrasing
# ------------------------------------
def is_actionable(text):
    return any(word in text.lower() for word in action_keywords())


# Detect structured flow using structural markers
# ------------------------------------------------
def has_structure(text):
    return sum(1 for word in structure_keywords() if word in text.lower()) >= 2


# Check for presence of idiomatic German phrasing
# ------------------------------------------------
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
        "grammar_check": "Behebe Grammatikfehler für bessere Verständlichkeit.",
        "idiomatic_check": "Nutze idiomatische Formulierungen für natürlichen Ausdruck.",
        "task_clarity": "Verwende klare Aktionsverben wie 'erstelle' oder 'analysiere'.",
        "structure_check": "Nutze Strukturmarker wie 'zuerst', 'dann', 'abschließend'.",
        "lexical_fit": "Vermeide unübliche oder holprige Wortkombinationen.",
        "tone_check": "Achte auf sachlichen, professionellen Tonfall.",
        "translation_integrity": "Struktur und Intention sollen mit dem Original übereinstimmen.",
    }
