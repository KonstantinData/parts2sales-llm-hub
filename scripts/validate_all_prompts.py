
import os
import json

ROOT = "prompts"
REQUIRED_KEYS = {"input", "expected"}

def validate_prompt_file(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            if not REQUIRED_KEYS.issubset(data):
                print(f"❌ Missing keys in {path}")
                return False
        return True
    except Exception as e:
        print(f"❌ Error in {path}: {e}")
        return False

def scan_all():
    valid = True
    for root, _, files in os.walk(ROOT):
        for file in files:
            if file.endswith(".json"):
                full_path = os.path.join(root, file)
                if not validate_prompt_file(full_path):
                    valid = False
    return valid

if __name__ == "__main__":
    if scan_all():
        print("✅ All prompt files valid")
    else:
        print("❌ Some prompt files failed validation")
