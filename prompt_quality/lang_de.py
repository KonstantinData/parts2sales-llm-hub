# lang\_de.py

# ------------------------------------------

# Purpose:

# Define idiomatic, structural, lexical, and tonal patterns for German prompts

# Goals:

# - Enable automated linguistic validation and quality scoring

# Use Cases:

# - Used by prompt validation tools for German prompt checking

# German idiomatic expressions for natural phrasing

# ------------------------------------------------

def idiomatic\_expressions():
return \[
"den Nagel auf den Kopf treffen",
"das Kind beim Namen nennen",
"ins kalte Wasser springen",
"zwei Fliegen mit einer Klappe schlagen",
]

# Action verbs indicating clarity of instruction

# ---------------------------------------------

def action\_keywords():
return \["analysiere", "erstelle", "generiere", "identifiziere", "leite ab"]

# Words indicating logical structure

# ----------------------------------

def structure\_keywords():
return \["zuerst", "anschließend", "dann", "schließlich", "abschließend"]

# Phrases that should be avoided due to awkwardness

# --------------------------------------------------

def lexical\_warnings():
return \["durchführen eine Analyse", "machen eine Ableitung"]

# Tone-inappropriate words or phrases

# ------------------------------------

def tone\_blacklist():
return \["scheiß", "was soll der mist", "mir doch egal"]

# Check for use of actionable phrasing

# ------------------------------------

def is\_actionable(text):
return any(word in text.lower() for word in action\_keywords())

# Detect structured flow using structural markers

# ------------------------------------------------

def has\_structure(text):
return sum(1 for word in structure\_keywords() if word in text.lower()) >= 2

# Check for presence of idiomatic German phrasing

# ------------------------------------------------

def has\_idiom(text):
return any(phrase in text for phrase in idiomatic\_expressions())

# Check for known incorrect lexical patterns

# ------------------------------------------

def violates\_lexical\_rules(text):
return any(combo in text for combo in lexical\_warnings())

# Detect tonal violations (informal, unprofessional)

# --------------------------------------------------

def has\_tone\_issue(text):
return any(term in text.lower() for term in tone\_blacklist())

# Explanation map for validation result keys

# ------------------------------------------

def explanations():
return {
"grammar\_check": "Behebe Grammatikfehler für bessere Verständlichkeit.",
"idiomatic\_check": "Nutze idiomatische Formulierungen für natürlichen Ausdruck.",
"task\_clarity": "Verwende klare Aktionsverben wie 'erstelle' oder 'analysiere'.",
"structure\_check": "Nutze Strukturmarker wie 'zuerst', 'dann', 'abschließend'.",
"lexical\_fit": "Vermeide unübliche oder holprige Wortkombinationen.",
"tone\_check": "Achte auf sachlichen, professionellen Tonfall.",
"translation\_integrity": "Struktur und Intention sollen mit dem Original übereinstimmen.",
}
