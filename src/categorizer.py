from rule_manager import RuleManager
import pandas as pd
import re

class Categorizer:
    def __init__(self, rule_manager: RuleManager):
        self.rule_manager = rule_manager
    
    # def _match_rule(self, description: str) -> tuple:
    #     """Return (category, subcategory) tuple"""
    #     desc_lower = description.lower()
    #     for rule in self.rule_manager.rules:
    #         if any(keyword in desc_lower for keyword in rule["keywords"]):
    #             return (rule["category"], rule.get("subcategory", None))
    #     return ("Uncategorized", None)
    
    # def _match_rule(self, description: str, existing_category: str) -> tuple:
    #     """
    #     Match transaction to a category/subcategory using BOTH description and existing category.
    #     Rules are checked in priority order (ascending).
    #     """
    #     desc_lower = description.lower()
    #     existing_category_lower = existing_category.lower() if existing_category else ""

    #     # Sort rules by priority (lower number = higher priority)
    #     sorted_rules = sorted(
    #         self.rule_manager.rules,
    #         key=lambda x: x.get("priority", 999)  # Default priority for rules without it
    #     )

    #     for rule in sorted_rules:
    #         # Check if existing category matches the rule's target
    #         category_match = (
    #             existing_category_lower
    #             and existing_category_lower in [c.lower() for c in rule.get("existing_categories", [])]
    #         )

    #         # Check if description contains any keywords
    #         keyword_match = any(
    #             keyword.lower() in desc_lower 
    #             for keyword in rule.get("keywords", [])
    #         )

    #         if category_match or keyword_match:
    #             return (rule["category"], rule.get("subcategory", None))

    #     return ("Uncategorized", None)

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
    
    # def categorize_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
    #     """Add category and subcategory columns"""
    #     # Apply the match function and split the tuple into two columns
    #     df[["category", "subcategory"]] = df["description"].apply(
    #         lambda desc: self._match_rule(desc)
    #     ).apply(pd.Series)  # Split tuples into columns
    #     return df
    
    def categorize_transactions(self, df: pd.DataFrame) -> pd.DataFrame:
        """Add category and subcategory columns using DataFrame input."""
        # Pass the entire DataFrame to _match_rule and assign results
        df[["category", "subcategory"]] = self._match_rule(df)
        return df
    
    def _match_rule_1(self, df: pd.DataFrame) -> pd.DataFrame:

        """Match rules against the entire DataFrame (vectorized)."""
        # Initialize default values
        df["category"] = "Uncategorized"
        df["subcategory"] = None
        
        # Sort rules by priority (ascending)
        sorted_rules = sorted(
            self.rule_manager.rules, 
            key=lambda x: x.get("priority", 999)
        )
        
        # Apply rules in priority order
        for rule in sorted_rules:
            # Create masks for keyword and category matches
            keyword_mask = df["description"].str.lower().str.contains(
                '|'.join(rule["keywords"]), 
                case=False, na=False
            )
            category_mask = df["Category"].str.lower().isin(
                [c.lower() for c in rule.get("Category", [])]
            )
            combined_mask = keyword_mask | category_mask
            
            # Apply rule to unmatched rows
            update_mask = combined_mask & (df["category"] == "Uncategorized")
            df.loc[update_mask, "category"] = rule["category"]
            df.loc[update_mask, "subcategory"] = rule.get("subcategory")
        
        return df[["category", "subcategory"]]
        
    def _match_rule(self, df: pd.DataFrame) -> pd.DataFrame:
        """Match transactions to categories/subcategories using nested YAML rules."""
        # Initialize defaults
        df["category"] = "Uncategorized"
        df["subcategory"] = None

        # Process categories in the order defined in YAML
        for category_rule in self.rule_manager.rules:
            category_name = category_rule["category"]
            subcategories = category_rule.get("subcategories", [])

            

            # Sort subcategories by priority (ascending)
            sorted_subcats = sorted(
                subcategories,
                key=lambda x: x.get("priority", 9999)  # Default priority if missing
            )


            # Check subcategories in priority order
            for subcat in sorted_subcats:
                print(subcat)
                keywords = subcat.get("keywords", [])
          

                # Keyword match (case-insensitive)
                keyword_mask = df["description"].str.lower().str.contains(
                    '|'.join([k.lower() for k in keywords]),
                    case=False, na=False
                )

            
                # Existing category match (case-insensitive)
                category_mask = df["Category"].str.lower().isin(
                    [c.lower() for c in keywords]
                )

                # Combined matches
                combined_mask = keyword_mask | category_mask


                # Update only unmatched rows
                update_mask = combined_mask & (df["category"] == "Uncategorized")
                df.loc[update_mask, "category"] = category_name
                df.loc[update_mask, "subcategory"] = subcat.get("name")

        return df[["category", "subcategory"]]