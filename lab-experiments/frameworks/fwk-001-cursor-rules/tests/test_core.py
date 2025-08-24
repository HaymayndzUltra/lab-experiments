"""
Basic smoke tests for the Cursor Rules Framework.
"""

import pytest
import tempfile
import json
import os
from src.core import CursorRulesEngine, Rule


def test_rule_creation():
    """Test that rules can be created."""
    rule = Rule(
        name="test_rule",
        description="A test rule",
        severity="warning",
        pattern="TODO",
        message="Found TODO comment"
    )
    assert rule.name == "test_rule"
    assert rule.enabled is True


def test_engine_initialization():
    """Test that the engine initializes correctly."""
    engine = CursorRulesEngine()
    assert len(engine.rules) == 0


def test_engine_with_rules_file():
    """Test that the engine loads rules from a file."""
    # Create a temporary rules file
    rules_data = {
        "rules": [
            {
                "name": "test_rule",
                "description": "A test rule",
                "severity": "warning",
                "pattern": "TODO",
                "message": "Found TODO comment"
            }
        ]
    }
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        json.dump(rules_data, f)
        temp_file = f.name
    
    try:
        engine = CursorRulesEngine(temp_file)
        assert len(engine.rules) == 1
        assert engine.rules[0].name == "test_rule"
    finally:
        os.unlink(temp_file)


def test_file_validation():
    """Test that file validation works."""
    engine = CursorRulesEngine()
    
    # Add a test rule
    rule = Rule(
        name="todo_rule",
        description="Find TODO comments",
        severity="warning",
        pattern="TODO",
        message="Found TODO comment"
    )
    engine.rules.append(rule)
    
    # Create a temporary test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as f:
        f.write("# This is a test file\n# TODO: Add more tests\nprint('hello')")
        temp_file = f.name
    
    try:
        results = engine.validate_file(temp_file)
        assert len(results) == 1
        assert results[0]['rule_name'] == "todo_rule"
        assert results[0]['severity'] == "warning"
    finally:
        os.unlink(temp_file)


if __name__ == "__main__":
    # Run basic tests
    test_rule_creation()
    test_engine_initialization()
    print("All basic tests passed!")
