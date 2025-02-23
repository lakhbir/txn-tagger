import yaml  # Replace json with yaml

class RuleManager:
    def __init__(self, rules_path: str):
        self.rules_path = rules_path
        self.rules = []
        self.load_rules()

    def load_rules(self):
        """Load rules and ensure keywords are lowercase"""
        with open(self.rules_path) as f:
            config = yaml.safe_load(f)
            for rule in config["rules"]:
                # Convert keywords to lowercase
                rule["keywords"] = [kw.strip().lower() for kw in rule["keywords"]]
                self.rules.append(rule)
            self.rules.sort(key=lambda x: x["priority"], reverse=True)

    