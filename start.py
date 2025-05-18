
from pyloan import pyloan
import csv
from datetime import date
import pandas as pd

# setup the loan guesses
debt_file = 'guesses.tsv'
debt_owners = []
descrips = []
principles = []
int_rates = []
payments = []
iter = 0
with open(debt_file,'r') as data:
   for line in csv.reader(data, delimiter='\t'):
        if iter == 0:
            iter +=1
        else:
            debt_owners.append(line[0])
            descrips.append(line[1])
            principles.append(int(line[2]))
            int_rates.append(round(float(line[3])*100,4))
            payments.append(int(line[4]))
            iter +=1
        # print(line[0], line[1], line[2], line[3], line[4])

total_debts = sum(principles)
total_payments_remaining = sum(payments)*12
loan_count = len(debt_owners)
current_date = str(date.today())

# setup the incomes
income_file = 'incomes.tsv'
names = []
incomes = []
iter2 = 0
with open(income_file,'r') as data:
   for line in csv.reader(data, delimiter='\t'):
        if iter2 == 0:
            iter2 +=1
        else:
            names.append(line[0])
            incomes.append(int(line[1]))
            iter2 +=1

print(names)
print(incomes)
print(sum(incomes))


# This processes each loan through the library calculator to find the worst repayment_to_principal ratio
loan_summaries = pd.DataFrame({"loan_amount":[], "total_payment_amount":[], "total_principal_amount"
                               :[], "total_interest_amount":[], "residual_loan_balance":[], "repayment_to_principal":[]})
for each in range(0,loan_count):

    # print('--------')
    # print(names[each], descrips[each], int_rates[each])
    loan = pyloan.Loan(loan_amount=principles[each]
                , interest_rate=int_rates[each]
                , loan_term=payments[each]
                , start_date=current_date
                # , payment_amount=1000
                )
    individ_summary_df = pd.DataFrame.from_records([loan.get_loan_summary()],columns=pyloan.Loan_Summary._fields)
    loan_summaries = loan_summaries._append(individ_summary_df, ignore_index=True)
    # print(loan.get_loan_summary())
    # print('------------------------------------------------')
# set index
loan_summaries.index = descrips

print(loan_summaries)



print(total_debts)
print(total_payments_remaining)
print(current_date)
# print(current_lowest)