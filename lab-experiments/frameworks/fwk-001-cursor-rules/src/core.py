"""
Core engine for Cursor Rules Framework.
"""

import json
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

logger = logging.getLogger(__name__)


@dataclass
class Rule:
    """Represents a single coding rule."""
    name: str
    description: str
    severity: str  # 'error', 'warning', 'info'
    pattern: str
    message: str
    enabled: bool = True


class CursorRulesEngine:
    """Main engine for processing and applying cursor rules."""
    
    def __init__(self, rules_file: Optional[str] = None):
        self.rules: List[Rule] = []
        if rules_file:
            self.load_rules(rules_file)
    
    def load_rules(self, rules_file: str) -> None:
        """Load rules from a JSON file."""
        try:
            with open(rules_file, 'r') as f:
                rules_data = json.load(f)
            self.rules = [Rule(**rule) for rule in rules_data.get('rules', [])]
        except Exception as e:
            logger.error(f"Failed to load rules: {e}")
            raise
    
    def validate_file(self, file_path: str) -> List[Dict[str, Any]]:
        """Validate a file against all enabled rules."""
        results = []
        try:
            with open(file_path, 'r') as f:
                content = f.read()
            
            for rule in [r for r in self.rules if r.enabled]:
                if rule.pattern in content:
                    results.append({
                        'rule_name': rule.name,
                        'severity': rule.severity,
                        'message': rule.message,
                        'file': file_path
                    })
        except Exception as e:
            logger.error(f"Error validating file {file_path}: {e}")
        
        return results
