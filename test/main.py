import json
from datetime import datetime
from main_l import CSVLoader

def main():
    # Create a test CSV file
    test_csv = """Transaction Details,Amount,Date
    Starbucks Coffee,$-5.99,2023-08-01
    Whole Foods Market,€49.50,2023-08-02
    Salary Deposit,"£2,000.00",2023-08-03
    """
    
    # Create test config.json
    config = {
        "csv_config": {
            "columns": {
                "description": "Transaction Details",
                "amount": "Amount",
                "transaction_date": "Date"
            },
            "amount_format": {
                "decimal_separator": ".",
                "thousands_separator": ",",
                "currency_symbols": ["$", "€", "£"],
                "negative_transaction_type": "debit"
            }
        }
    }
    
    # Save test files
    with open("test_config.json", "w") as f:
        json.dump(config, f, indent=2)
    
    with open("test_transactions.csv", "w") as f:
        f.write(test_csv)
    
    # Load and process
    loader = CSVLoader("test_config.json")
    transactions = loader.load_transactions("test_transactions.csv")
    
    # Print results
    print("\nProcessed Transactions:")
    for t in transactions:
        print(f"- {t.description}: {t.amount} ({t.type})")

if __name__ == "__main__":
    main()