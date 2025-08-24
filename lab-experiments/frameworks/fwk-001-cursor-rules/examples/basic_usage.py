"""
Basic usage example for the Cursor Rules Framework.

This example shows how to create rules and validate files.
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from core import CursorRulesEngine, Rule


def main():
    """Demonstrate basic framework usage."""
    print("=== Cursor Rules Framework - Basic Usage Example ===\n")
    
    # Create a new rules engine
    engine = CursorRulesEngine()
    
    # Add some example rules
    rules = [
        Rule(
            name="todo_comment",
            description="Find TODO comments in code",
            severity="warning",
            pattern="TODO",
            message="Found TODO comment - consider addressing this"
        ),
        Rule(
            name="print_statement",
            description="Find print statements (use logging instead)",
            severity="info",
            pattern="print(",
            message="Consider using logging instead of print statements"
        ),
        Rule(
            name="hardcoded_password",
            description="Find potential hardcoded passwords",
            severity="error",
            pattern="password = ",
            message="Hardcoded passwords are a security risk"
        )
    ]
    
    for rule in rules:
        engine.rules.append(rule)
    
    print(f"Loaded {len(engine.rules)} rules:")
    for rule in engine.rules:
        print(f"  - {rule.name}: {rule.description} ({rule.severity})")
    
    # Create a sample file to test
    sample_code = '''# Sample Python file
import os

# TODO: Add proper error handling
def process_data():
    password = "secret123"  # This should trigger an error
    print("Processing data...")  # This should trigger a warning
    
    if os.path.exists("config.txt"):
        print("Config file found")  # Another warning
        # TODO: Implement configuration loading
    
    return True
'''
    
    # Write sample file
    sample_file = "sample_code.py"
    with open(sample_file, "w") as f:
        f.write(sample_code)
    
    print(f"\nCreated sample file: {sample_file}")
    
    # Validate the file
    print("\nValidating sample file...")
    results = engine.validate_file(sample_file)
    
    if results:
        print("Found issues:")
        for result in results:
            print(f"  [{result['severity'].upper()}] {result['rule_name']}: {result['message']}")
    else:
        print("No issues found!")
    
    # Clean up
    os.remove(sample_file)
    print(f"\nCleaned up sample file")


if __name__ == "__main__":
    main()
