
from pyloan import pyloan
import csv
from datetime import date
import pandas as pd

# helpful links
#https://www.experts-exchange.com/articles/1948/A-Guide-to-the-PMT-FV-IPMT-and-PPMT-Functions.html
#https://money.stackexchange.com/questions/94140/what-is-the-math-used-to-calculate-the-impact-that-overpaying-a-mortgage-has-an

# import the loan guesses
print("Options: 'guesses_by_prin.tsv', 'guesses_by_rate.tsv'")
debt_file = input()
debt_owners = []
descrips = []
principles = []
original_principles = []
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
            original_principles.append(int(line[2]))
            int_rates.append(round(float(line[3]),4))
            payments_left.append(int(line[4]))
            iter +=1
        # print(line[0], line[1], line[2], line[3], line[4])

# make a list to retain the origianl principles in case you need that
# also just get some calculations out of the way

total_debts = sum(principles)
total_payments_remaining = sum(payments_left)
loan_count = len(debt_owners)
# current_date = str(date.today())

# import the incomes
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

# print everything out just to check
print(names)
print(incomes)
print('Total debts:', total_debts)
print('Total payments:', total_payments_remaining)
# print(current_date)

# Get the standard rates, their full term debt, and debt ratios
std_mnthly_rate = []
full_term_debts = []
debt_ratios = []
for each in range(0, loan_count):
    std_mnthly_rate.append(
        round(
            # (int_rates[each]/(1-(1+int_rates[each])**-payments_left[each]))*principles[each]
            (int_rates[each]/12*principles[each]/(
            1-(1+(int_rates[each]/12))**-payments_left[each])
        ),2))
    full_term_debts.append(round(std_mnthly_rate[each]*payments_left[each],2))
    debt_ratios.append(round((full_term_debts[each]/principles[each]),2))

# Make a list for ticking down the debt
# full_term_debts_ticker = full_term_debts
print(std_mnthly_rate)
print(full_term_debts)
print(debt_ratios)



# Now get all of them to tick down at the same time
principle_paid = []
current_period = [0] * loan_count
int_paid = [0]* loan_count

print('Total Incomes:', sum(incomes))
print("Enter percentage of net income, .015")
# net_inc_prcnt = float(input())
net_inc_prcnt = .015
group_extra_pay = net_inc_prcnt*sum(incomes)/12
print("Monthly contribution:", group_extra_pay)

# define a function to walk each loan down WITH the and print out where the loan is out
def loan_group_walkdown(loan_num):
    # If the standard monthly rate covers what's left of the loan
    if (std_mnthly_rate[loan_num]) > principles[loan_num]:
        int_paid[loan_num] += int_portion
        remaining_loan = int_portion+principles[loan_num]

        principles[loan_num] = 0
        print(descrips[loan_num]
        , current_period[loan_num], payments_left[loan_num]
        , round(remaining_loan,2), '0'
        , int_portion
        , round(principles[loan_num],2), int_paid[loan_num])
    # If the std plus group extra covers what's left of the loan
    elif (group_extra_pay+std_mnthly_rate[loan_num]) > principles[loan_num]:
        int_paid[loan_num] += int_portion
        remaining_loan = int_portion+principles[loan_num]
        group_finisher = (group_extra_pay+std_mnthly_rate[loan_num])-principles[loan_num]

        principles[loan_num] = 0
        print(descrips[loan_num]
        , current_period[loan_num], payments_left[loan_num]
        , round(remaining_loan,2), group_finisher
        , int_portion
        , round(principles[loan_num],2), int_paid[loan_num])
    # Standard payment plus group extra paying a normal payment off
    else:
        principles[loan_num] += -(prin_portion+group_extra_pay)
        int_paid[loan_num] += int_portion

        print(descrips[loan_num]
        , current_period[loan_num], payments_left[loan_num]
        , std_mnthly_rate[loan_num], group_extra_pay
        , int_portion
        , round(principles[loan_num],2), int_paid[loan_num])

# define a function to walk each loan down and print out where the loan is out
def loan_walkdown(loan_num):
    # If the standard monthly rate covers what's left of the loan
    if (std_mnthly_rate[loan_num]) > principles[loan_num]:
        int_paid[loan_num] += int_portion
        remaining_loan = int_portion+principles[loan_num]

        principles[loan_num] = 0
        print(descrips[loan_num]
        , current_period[loan_num], payments_left[loan_num]
        , round(remaining_loan,2), '0'
        , int_portion
        , round(principles[loan_num],2), int_paid[loan_num])
    else:
        principles[loan_num] += -(prin_portion)
        int_paid[loan_num] += int_portion

        print(descrips[loan_num]
        , current_period[loan_num], payments_left[loan_num]
        , std_mnthly_rate[loan_num], 'Grp: 0'
        , int_portion
        , round(principles[loan_num],2), int_paid[loan_num])

while total_payments_remaining > 0:
    total_payments_remaining += -1
    # cycle through each loan
    for each in range(0, loan_count):
        # if there is principle left on the loan
        if principles[each]>0:
            total_payments_remaining += -1
            # if there are still payments left on THIS loan
            if payments_left[each]>0:
                current_period[each] += 1
                payments_left[each] += -1
                # now determine how much of the payment is interest and principle
                int_portion = round(principles[each]*(int_rates[each]/12), 2)
                prin_portion = round(std_mnthly_rate[each] - int_portion, 2)
                
                # next big thing. 
                # If it's the first loan, process that loan with group_pay
                if each == 0:
                    loan_group_walkdown(each)
                    print(current_period)
                    print(principles[each])
                # If it's NOT the first loan, but the first loan is still being paid
                # process that loan without the group_pay
                elif current_period[each] == current_period[each-1]:
                    loan_walkdown(each)
                    print(current_period)
                    print(principles[each])
                # If the first loan is done, then process the next loan with group_pay
                elif current_period[each] > current_period[each-1]:
                    loan_group_walkdown(each)
                    print(current_period)
                    print(principles[each])
            else:
                pass
        else:
            pass

# let's handle how much was saved and how long it took to get here
loan_savings = []

for each in range(0, loan_count):
    loan_savings.append(
        round(full_term_debts[each]-original_principles[each]-int_paid[each],2))

print(loan_savings)
print(sum(loan_savings))
print(current_period)






















# # IN ORDER TO MAKE THIS WORK I THINK
# # you need to move the while statement inside the first for loop. 
# # Also, record what period the loan is paid off, so you can have an if statement or something
# # move to the next loan and apply the new group_extra_pay


# # cycle through all potential payments
# while total_payments_remaining >0:
#     total_payments_remaining += -1
#     # cycle through each loan
#     for each in range(0, loan_count):
#         # if there is principle left on the loan
#         if principles[each]>0:
#             # if there are still payments left on THIS loan
#             if payments_left[each]>0:
#                 current_period[each] += 1
#                 payments_left[each] += -1

#                 # now determine how much of the payment is interest and principle
#                 int_portion = round(principles[each]*(int_rates[each]/12), 2)
#                 prin_portion = round(std_mnthly_rate[each] - int_portion, 2)

#                 # If the standard monthly rate covers what's left of the loan
#                 if (std_mnthly_rate[each]) > principles[each]:
#                     int_paid[each] += int_portion
#                     remaining_loan = int_portion+principles[each]

#                     principles[each] = 0
#                     print(descrips[each]
#                     , current_period[each], payments_left[each]
#                     , round(remaining_loan,2), '0'
#                     , int_portion
#                     , round(principles[each],2), int_paid[each])
                
#                 # If the std plus group extra covers what's left of the loan
#                 elif (group_extra_pay+std_mnthly_rate[each]) > principles[each]:
#                     int_paid[each] += int_portion
#                     remaining_loan = int_portion+principles[each]
#                     group_finisher = (group_extra_pay+std_mnthly_rate[each])-principles[each]

#                     principles[each] = 0
#                     print(descrips[each]
#                     , current_period[each], payments_left[each]
#                     , round(remaining_loan,2), group_finisher
#                     , int_portion
#                     , round(principles[each],2), int_paid[each])
                
#                 # Standard payment plus group extra paying a normal payment off
#                 else:
#                     principles[each] += -(prin_portion+group_extra_pay)
#                     int_paid[each] += int_portion

#                     print(descrips[each]
#                     , current_period[each], payments_left[each]
#                     , std_mnthly_rate[each], group_extra_pay
#                     , int_portion
#                     , round(principles[each],2), int_paid[each])
#             else:
#                 pass
#         else:
#             pass

# # let's handle how much was saved and how long it took to get here
# loan_savings = []

# for each in range(0, loan_count):
#     loan_savings.append(
#         round(full_term_debts[each]-original_principles[each]-int_paid[each],2))

# print(loan_savings)
# print(current_period)









# # # I'm going to try to do this without using pyloan
# # # This processes each loan through the library calculator to find the worst repayment_to_principal ratio
# # loan_summaries = pd.DataFrame({"loan_amount":[], "total_payment_amount":[], "total_principal_amount"
# #                                :[], "total_interest_amount":[], "residual_loan_balance":[], "repayment_to_principal":[]})
# # for each in range(0,loan_count):

# #     # print('--------')
# #     # print(names[each], descrips[each], int_rates[each])
# #     loan = pyloan.Loan(loan_amount=principles[each]
# #                 , interest_rate=int_rates[each]
# #                 , loan_term=payments[each]
# #                 , start_date=current_date
# #                 # , payment_amount=1000
# #                 )
# #     individ_summary_df = pd.DataFrame.from_records([loan.get_loan_summary()],columns=pyloan.Loan_Summary._fields)
# #     loan_summaries = loan_summaries._append(individ_summary_df, ignore_index=True)
# #     # print(loan.get_loan_summary())
# #     # print('------------------------------------------------')
# # # set index
# # loan_summaries.index = descrips

# # print(loan_summaries)
