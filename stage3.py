from math import log
from math import pow
from math import ceil
from string import digits


def calculate_interest(i):
    return i / (12 * 100)


def calculate_loan(annuity, interest, no_of_payments):
    return annuity // ((interest * pow(1 + interest, no_of_payments)) / (pow(1 + interest, no_of_payments) - 1))


def calculate_payment(annuity, interest, loan):
    return log(annuity / (annuity - interest * loan), 1 + interest)


def calculate_annuity(loan, interest, no_of_payments):
    return loan * ((interest * pow(1 + interest, no_of_payments)) / (pow(1 + interest, no_of_payments) - 1))


def convert_numbers(num1, num2, num3):
    nums = [num1, num2, num3]
    fixed_nums = []

    for num in nums:
        isdigit = all([char in digits for char in num])

        if isdigit:
            num = int(num)
            fixed_nums.append(num)
        else:
            try:
                num = float(num)
                fixed_nums.append(num)
            except ValueError:
                return False
    return fixed_nums[0], fixed_nums[1], fixed_nums[2]


def manage_payment():
    p = input('Enter the loan principal: ')
    a = input('Enter the annuity payment: ')
    i = input('Enter the loan interest: ')

    if convert_numbers(p, a, i):
        p, a, i = convert_numbers(p, a, i)
    else:
        return False

    i = calculate_interest(i)
    result = calculate_payment(a, i, p)

    result = ceil(result)
    years = result // 12
    months = ceil(result % 12)

    if years == 0 and months > 0:
        periods = 'months' if months > 1 else 'month'
        return f'It will take {months} {periods} to repay this loan!'
    elif months == 0 and years > 0:
        return f'It will take {years} years to repay this loan!'
    elif years > 0 and months > 0:
        periods = 'months' if months > 1 else 'month'
        return f'It will take {years} years and {months} {periods} to repay this loan!'


def manage_annuity():
    p = input('Enter the loan principal: ')
    n = input('Enter the number of periods: ')
    i = input('Enter the loan interest: ')

    if convert_numbers(p, n, i):
        p, n, i = convert_numbers(p, n, i)
    else:
        return False

    i = calculate_interest(i)
    result = ceil(calculate_annuity(p, i, n))
    return f'Your monthly payment = {result}!'


def manage_loan():
    a = input('Enter the annuity payment: ')
    n = input('Enter the number of periods: ')
    i = input('Enter the loan interest: ')

    if convert_numbers(a, n, i):
        a, n, i = convert_numbers(a, n, i)
    else:
        return False

    i = calculate_interest(i)
    result = round(calculate_loan(a, i, n))
    return f'Your loan principal = {result}!'


print('What do you want to calculate?\ntype "n" for number of monthly payments,'
      '\ntype "a" for annuity monthly payment amount,\ntype "p" for loan principal:')
action = input()

if action == 'n':
    print(manage_payment())
elif action == 'a':
    print(manage_annuity())
elif action == 'p':
    print(manage_loan())
