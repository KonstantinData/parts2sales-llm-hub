# scripts/prompt_selector.py
# CLI Tool: Select and inspect prompts from prompt_registry.yaml

import yaml
import argparse
import os

REGISTRY_PATH = os.path.join(os.path.dirname(__file__), "../prompt_registry.yaml")


def load_registry():
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def list_tasks(registry):
    print("\nAvailable Prompt Tasks:\n")
    for key in sorted(registry.keys()):
        print(f"- {key}: {registry[key].get('description', '')}")


def show_prompt_info(registry, task):
    entry = registry.get(task)
    if not entry:
        print(f"\n❌ Task '{task}' not found in registry.")
        return

    print(f"\n📌 Prompt Task: {task}")
    print(f"   Description: {entry.get('description')}")
    print(f"   Production Prompt: {entry.get('production_prompt')}")
    print(f"   Metadata File:     {entry.get('metadata_file')}")
    print(f"   Version (prod):    {entry.get('current_version_prod')}")
    print(f"   Version (dev):     {entry.get('current_version_dev')}")


def main():
    parser = argparse.ArgumentParser(description="Prompt Selector CLI")
    parser.add_argument(
        "--list", action="store_true", help="List all available prompt tasks"
    )
    parser.add_argument(
        "--task", type=str, help="Show details for a specific prompt task"
    )
    args = parser.parse_args()

    registry = load_registry()

    if args.list:
        list_tasks(registry)
    elif args.task:
        show_prompt_info(registry, args.task)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
