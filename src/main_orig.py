import csv
import json
import re
import html
import pandas as pd

def writeCsv(listOfRecords, filePath):

    # mydict =[{'name': 'Kelvin Gates', 'age': '19', 'country': 'USA'}, 
    #          {'name': 'Blessing Iroko', 'age': '25', 'country': 'Nigeria'}, 
    #          {'name': 'Idong Essien', 'age': '42', 'country': 'Ghana'}]

    # fields = ['name', 'age', 'country'] 

    fields = ['Description', 
              'Amount', 
              'Category', 
              'Relation to Category',
              'Sub Category',
              'Transaction Date', 
              'Data Source', 
              'Month-Year', 
              'Type',
              'Frequency'] 

    with open(filePath, 'w', newline='') as file: 
        writer = csv.DictWriter(file, fieldnames=fields)

        writer.writeheader()
        writer.writerows(listOfRecords)


#======

def subCategoryMapper(match,default):
    description  = match
    category     = default
   
    a_string = description.lower()

    
    phoneList = ["tmobile"]
    gasList = ["sunoco", "sinclair"]
    subscriptionList = ["netflix", "audible","kumon"]

    if any(x in a_string for x in phoneList):
        return "Phone"
    elif  any(x in a_string for x in subscriptionList):
        return "Subscription"
    elif  any(x in a_string for x in ["peco","PECO"]):
        return "Electricity"
    elif  any(x in a_string for x in ["rcn"]):
        return "Internet"
    elif  any(x in a_string for x in ["progressive"]):
        return "Insurance"
    else:
        return category


def getMonthYear(date):
    print(date)
    # date_obj = datetime.strptime(date, "%m/%d/%Y")
    # month = date_obj.month
    # year = date_obj.year
    # return month+"-"+year

  
    # date_series = pd.to_datetime(date).strftime("%m/%d/%Y")
    # print(date_series.dt.month)
    # month = date_series.date.month
    # year = date_series.date.year

    ts = pd.Timestamp(date)
    month = str(ts.month).zfill(2)
    year  = str(ts.year).zfill(2)
    return month+"-"+year
    # print(f"Month: {month}, Year: {year}")  # Output: Month: 7, Year: 2022

def processChaseCard(fileLocation):
    expenses = []
    payments = []
    with open(fileLocation, newline='') as csvfile:
        
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader, None) 

        for row in spamreader:
            transactionDate  = row[0]
            postDate  = row[1]
            description  = row[2]
            category  = row[3]
            type      = row[4]
            amount    = row[5]
            relationToCategory = category

            record= {
                "Transaction Date": transactionDate,
                "Description"     : description,
                "Category"        : category,
                "Type"            : type,
                "Amount"          : amount,
                "Relation to Category" : relationToCategory,
                "Sub Category": subCategoryMapper( row[2],row[3]),
                "Month-Year"  : getMonthYear(transactionDate),
                "Data Source" : "Chase Card"
                }
            expenses.append(record)
            
        print(json.dumps(expenses))
        
    return expenses

def transformCitizensBank(description):
    
    category = ""
    subCategory = ""
    frequency = ""

    if description:
        # NEVER TRUST THE INPUT FROM USER, so do your due dilegence
        str_lower = description.lower()

        bills_and_utilities = ['PECO', 'CROSSCOUNTRY','aqua','CITIZENSBANK',
                            'chase',"tjx",'kohls','MORTG','DOVENMUEHLE','RCN','ASTOUND','GODADDY','NERFIRMS']
        bills_and_Utilities_lower = [x.lower() for x in bills_and_utilities]
        for item in bills_and_Utilities_lower:
            if item in str_lower:
                category = "Bills & Utilities"
                if item in ['tjx','chase','kohls','citizensbank']:
                    subCategory = "Credit Card"
                    frequency = "On Demand"

                elif item in ['aqua']:
                    subCategory = "Water"
                    frequency = "Monthly"

                elif item in ['peco']:
                    subCategory = "Electricity"
                    frequency = "Monthly"

                elif item in ['rcn','astound','comcast']:
                    subCategory = "Internet"
                    frequency = "Monthly"
                    
                elif item in ['crosscountry','mortgage','mortg','dovenmuehle']:
                    subCategory = "Mortgage"
                    frequency = "Monthly"
            
                
        personal = ['VGI', 'KUMON','NERFIRMS','GODADDY','VANGUARD BUY','BARCLAYS','investment','check']
        personal_lower = [x.lower() for x in personal]
        for item in personal_lower:
                print(item)
                if item in str_lower:
                    category = "Personal"
                    if item in ['netfirms','godaddy']:
                        subCategory = "Business"
                        frequency = "Yearly"
                    elif item in ['vgi','529','kumon']:
                        subCategory = "Education"
                        frequency = "Monthly"
                    elif item in ['vangaurd buy','barclays']:
                        subCategory = "Investment"
                        frequency = "On Demand"
                    elif item in ['check']:
                        subCategory = "Kids"
                        frequency = "Monthly"


        data = {
            'category' : category,
            'subCategory' : subCategory,
            'frequency' : frequency
        }

    else:
        data = {
            'category' : 'Miscellaneous',
            'subCategory' : '',
            'frequency' : 'On Demand'
        }

    return data
        # return category

def processCitizensBank(fileLocation):
    expenses = []
    payments = []
    with open(fileLocation, newline='') as csvfile:
        
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        next(spamreader, None) 
        for row in spamreader:
            csvTransactionType = row[0].capitalize()#DEBIT, DEPOSIT, DIRECT DEPOSIT, CHECK
            csvDate            = row[1]
            csvAccountType     = row[2]
            csvDescription     = (" ".join(row[3].split())).capitalize()
            csvAmount          = row[4]
            csvReferenceNote   = row[5]
            csvCredits         = row[6]
            csvDebits          = row[7]
            
            
            if not csvDescription or csvDescription is None:
                if csvTransactionType in (['Check']): 
                    csvDescription = f'Check reference # - {csvReferenceNote}'
                else:
                    csvDescription = csvTransactionType
      
            
            data = transformCitizensBank(csvDescription)
            
            sale= {
                    "Transaction Date": csvDate,
                    "Description"     : csvDescription,
                    "Amount"          : csvAmount,
                    "Category"        : data['category'],
                    "Relation to Category" : data['category'],
                    "Sub Category"    : data['subCategory'],
                    "Month-Year"      : getMonthYear(csvDate),
                    "Type"            : csvTransactionType,
                    "Data Source"     : "Citizens Bank",
                    "Frequency"       : data['frequency']
                    }
            expenses.append(sale)
           
         
                


        print(json.dumps(expenses))
        return expenses


# chaseReport = 'C:\\Users\\punja\\Downloads\\Chase1611_ALL.csv'
# expenseChaseDict = processChaseCard(chaseReport)
# writeCsv(expenseChaseDict,'C:\\Users\\punja\\Downloads\\Chase1611_ALL_Tranformed.csv')


citizensBankReport = 'C:\\Users\\punja\\Downloads\\citizens_bank_2024-modified.csv'
expenseCitizenBankDict = processCitizensBank(citizensBankReport)
print(len(expenseCitizenBankDict))
writeCsv(expenseCitizenBankDict,'C:\\Users\\punja\\Downloads\\citizens_bank_2024_transformed.csv')


# print(determintCategory("PECOENERGY       UTIL_BIL"))