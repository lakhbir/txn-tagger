from rule_manager import RuleManager
from categorizer import Categorizer
from csv_loader import CSVLoader


csv_config = "c:/Users/punja/development/txn-tagger/src/config/csv_config.yaml"
rules = "c:/Users/punja/development/txn-tagger/src/config/rules.yaml"
csv = "c:/Users/punja/development/txn-tagger/src/resources/chase.csv"


csv_loader = CSVLoader(csv_config)
df_txn = csv_loader.load_transactions(csv)

ruleManager = RuleManager(rules_path=rules)
categorizer = Categorizer(rule_manager=ruleManager)

df = categorizer.categorize_transactions(df_txn)


print(df)




