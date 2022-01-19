from math import ceil

loan = int(input('Enter the loan principal: '))

print('What do you want to calculate?')
print('type "m" - for number of monthly payments,')
print('type "p" - for the monthly payment: ')
action = input()

if action == 'p':
    months = int(input('Enter the number of months: '))
    month_payments = loan / months
    if not month_payments.is_integer():
        # Dealing with decimals and keeping last payment same or below fixed monthly payment
        rounded_up = ceil(loan / months)
        last_payment = rounded_up * (months - 1)
        payments = loan - last_payment
        print(f'Your monthly payment = {rounded_up} and the last payment = {payments}.')
    else:
        print(f'Your monthly payment = {int(month_payments)}')
elif action == 'm':
    monthly_payment = int(input('Enter the monthly payment: '))
    payment = round(loan / monthly_payment)
    periods = 'months' if payment > 1 else 'month'
    print(f'It will take {payment} {periods} to repay the loan')
