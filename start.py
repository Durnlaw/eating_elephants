
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
payments_left = []
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
            payments_left.append(int(line[4]))
            iter +=1
        # print(line[0], line[1], line[2], line[3], line[4])

total_debts = sum(principles)
total_payments_remaining = sum(payments_left)
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
print('Total debts:', total_debts)
print('Total payments:', total_payments_remaining)
print(current_date)

print('Total Incomes:', sum(incomes))
print("Enter percentage of net income, .015")
# net_inc_prcnt = float(input())
net_inc_prcnt = .015
monthly_contrib = net_inc_prcnt*sum(incomes)/12
print("Monthly contribution:", monthly_contrib)

# Get the standard rates and their full term debt
monthly_rates = []
full_term_debts = []
debt_ratios = []
for each in range(0, loan_count):
    monthly_rates.append(
        round(
            (int_rates[each]/100/12*principles[each])/(
            1-((1+(int_rates[each]/100/12))**-payments_left[each])
        ),2)
        )
    full_term_debts.append(round(monthly_rates[each]*payments_left[each],2))
    debt_ratios.append(round((full_term_debts[each]/principles[each]),2))

# Make a list for ticking down the debt
# full_term_debts_ticker = full_term_debts
print(monthly_rates)
print(full_term_debts)
print(debt_ratios)


principle_paid = []
interest_paid = []
current_payment = [0] * loam_count
# Now get all of them to tick down at the same time
while total_payments_remaining >0:
    for each in range(0, loan_count):
        if payments_left[each]>0:
            current_payment += 1
            total_payments_remaining += -1
            payments_left[each] += -1
            print("Payments left:", payments_left[each], monthly_rates[each])
            
print(current_payment)
            # print(principles[each], principles[each]-monthly_rates[each])











# # I'm going to try to do this without using pyloan
# # This processes each loan through the library calculator to find the worst repayment_to_principal ratio
# loan_summaries = pd.DataFrame({"loan_amount":[], "total_payment_amount":[], "total_principal_amount"
#                                :[], "total_interest_amount":[], "residual_loan_balance":[], "repayment_to_principal":[]})
# for each in range(0,loan_count):

#     # print('--------')
#     # print(names[each], descrips[each], int_rates[each])
#     loan = pyloan.Loan(loan_amount=principles[each]
#                 , interest_rate=int_rates[each]
#                 , loan_term=payments[each]
#                 , start_date=current_date
#                 # , payment_amount=1000
#                 )
#     individ_summary_df = pd.DataFrame.from_records([loan.get_loan_summary()],columns=pyloan.Loan_Summary._fields)
#     loan_summaries = loan_summaries._append(individ_summary_df, ignore_index=True)
#     # print(loan.get_loan_summary())
#     # print('------------------------------------------------')
# # set index
# loan_summaries.index = descrips

# print(loan_summaries)
