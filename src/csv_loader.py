from dataclasses import dataclass
from typing import List
import pandas as pd
import yaml  # Replace json with yaml

@dataclass
class Transaction:
    description: str
    amount: float  # Raw signed value (e.g., -50.00)
    transaction_date: str
    type: str  # 'debit' or 'credit'

class CSVLoader:
    def __init__(self, config_path: str):
      with open(config_path) as f:
            self.config = yaml.safe_load(f)["csv_config"]  # YAML loading

    
    def _clean_amount(self, amount_str: str) -> float:
        """Extract numerical value while preserving sign"""
        for symbol in self.config["amount_format"]["currency_symbols"]:
            amount_str = amount_str.replace(symbol, "")
        amount_str = amount_str.replace(
            self.config["amount_format"]["thousands_separator"], ""
        )
        decimal_sep = self.config["amount_format"]["decimal_separator"]
        if decimal_sep != ".":
            amount_str = amount_str.replace(decimal_sep, ".")
        return float(amount_str.strip())

    def _get_transaction_type(self, amount: float) -> str:
        """Determine type based on sign and config"""
        if amount < 0:
            return self.config["amount_format"]["negative_transaction_type"]
        return "credit" if self.config["amount_format"]["negative_transaction_type"] == "debit" else "debit"

    def _clean_column_names(self, df: pd.DataFrame) -> pd.DataFrame:
        """Trim + lowercase all CSV column names"""
        df.columns = [col.strip() for col in df.columns]
        return df

    def load_transactions(self, csv_path: str) -> List[Transaction]:
        df = pd.read_csv(csv_path)
        df = self._clean_column_names(df)
        

        print("Columns in CSV:", df.columns.tolist())  # Debug line
        df.rename(columns=self.config["columns"], inplace=True)
        
        # Process amounts and add transaction type
        # df["amount"] = df["amount"].apply(self._clean_amount)
        df["type"] = df["amount"].apply(self._get_transaction_type)
        return df
