from rule_manager import RuleManager
import pandas as pd
import re

class Categorizer:
    def __init__(self, rule_manager: RuleManager):
        self.rule_manager = rule_manager
    
    def _match_rule(self, description: str) -> tuple:
        """Return (category, subcategory) tuple"""
        desc_lower = description.lower()
        for rule in self.rule_manager.rules:
            if any(keyword in desc_lower for keyword in rule["keywords"]):
                return (rule["category"], rule.get("subcategory", None))
        return ("Uncategorized", None)

    # def _match_rule(self, description: str) -> tuple:
    #     """Match partial words and handle special characters"""
    #     # Clean description: lowercase + remove non-alphanumeric
    #     desc_clean = re.sub(r'[^a-z0-9 ]', '', description.lower())
        
    #     for rule in self.rule_manager.rules:
    #         for keyword in rule["keywords"]:
    #             # Check if keyword appears as whole/partial word
    #             if re.search(rf'\b{keyword}\b', desc_clean, re.IGNORECASE):
    #                 return (rule["category"], rule.get("subcategory"))
    #     return ("Uncategorized", None)
    
    def categorize_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add category and subcategory columns"""
        # Apply the match function and split the tuple into two columns
        df[["category", "subcategory"]] = df["description"].apply(
            lambda desc: self._match_rule(desc)
        ).apply(pd.Series)  # Split tuples into columns
        return df