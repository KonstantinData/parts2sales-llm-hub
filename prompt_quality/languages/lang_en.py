# lang\_en.py

# ------------------------------------------

# Purpose:

# Define idiomatic, structural, lexical, and tonal patterns for English prompts

# Goals:

# - Enable automated linguistic validation and quality scoring

# Use Cases:

# - Used by prompt validation tools for English prompt checking

# English idiomatic expressions for natural phrasing

# -------------------------------------------------

def idiomatic\_expressions():
return \[
"hit the ground running",
"rule of thumb",
"think outside the box",
"back to the drawing board",
]

# Action verbs indicating clarity of instruction

# ---------------------------------------------

def action\_keywords():
return \["analyze", "create", "generate", "identify", "derive"]

# Words indicating logical structure

# ----------------------------------

def structure\_keywords():
return \["first", "then", "next", "finally", "in conclusion"]

# Phrases that should be avoided due to awkwardness

# --------------------------------------------------

def lexical\_warnings():
return \["analyze of", "do a derivation"]

# Tone-inappropriate words or phrases

# -----------------------------------

def tone\_blacklist():
return \["whatever", "damn", "wtf"]

# Check for use of actionable phrasing

# ------------------------------------

def is\_actionable(text):
return any(word in text.lower() for word in action\_keywords())

# Detect structured flow using structural markers

# ------------------------------------------------

def has\_structure(text):
return sum(1 for word in structure\_keywords() if word in text.lower()) >= 2

# Check for presence of idiomatic English phrasing

# -------------------------------------------------

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
"grammar\_check": "Fix grammar issues for clearer understanding.",
"idiomatic\_check": "Consider using idiomatic phrases for natural tone.",
"task\_clarity": "Clarify the instruction using action verbs like 'generate' or 'identify'.",
"structure\_check": "Add structure markers like 'first', 'then', 'finally' to guide the flow.",
"lexical\_fit": "Avoid awkward phrasing or uncommon combinations.",
"tone\_check": "Use a professional and neutral tone.",
"translation\_integrity": "Check that structure and intent match the source.",
}
