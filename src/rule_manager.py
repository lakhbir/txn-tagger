# import yaml  # Replace json with yaml

# class RuleManager:
#     def __init__(self, rules_path: str):
#         self.rules_path = rules_path
#         self.rules = []
#         self.load_rules()

#     def load_rules(self):
#         """Load rules and ensure keywords are lowercase"""
#         with open(self.rules_path) as f:
#             config = yaml.safe_load(f)
#             for rule in config["rules"]:
#                 # Convert keywords to lowercase
#                 rule["keywords"] = [kw.strip().lower() for kw in rule["keywords"]]
#                 self.rules.append(rule)
#             self.rules.sort(key=lambda x: x["priority"], reverse=True)

            
import yaml
from typing import List, Dict

class RuleManager:
    def __init__(self, rules_file: str):
        self.rules_file = rules_file
        self.rules: List[Dict] = []
        self.load_rules()

    def load_rules(self) -> None:
        """Load and parse the YAML rules file with nested categories/subcategories."""
        try:
            with open(self.rules_file, "r") as f:
                data = yaml.safe_load(f)
                self.rules = data.get("rules", [])
        except Exception as e:
            raise ValueError(f"Error loading rules from {self.rules_file}: {e}")

    def get_rules(self) -> List[Dict]:
        """Return the loaded rules."""
        return self.rules
    