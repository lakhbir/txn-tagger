from rule_manager import RuleManager
from categorizer import Categorizer
from csv_loader import CSVLoader
import file_writer

csv_config = "c:/Users/punja/development/txn-tagger/src/config/csv_config.yaml"
rules = "c:/Users/punja/development/txn-tagger/src/config/rules_1.yaml"
csv = "c:/Users/punja/development/txn-tagger/src/resources/2025_chase_card_yearToDate.csv"
output = "c:/Users/punja/development/txn-tagger/src/resources/chase_tagged.csv"

csv_loader = CSVLoader(csv_config)
df_txn = csv_loader.load_transactions(csv)
ruleManager = RuleManager(rules_file=rules)
categorizer = Categorizer(rule_manager=ruleManager)

df = categorizer.categorize_transactions(df_txn)

file_writer.write_to_file(df,output)


# print(df)




