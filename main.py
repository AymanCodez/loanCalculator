import argparse
from math import log, pow, ceil
from string import digits


def calculate_interest(i):
    return i / (12 * 100)


def calculate_loan(annuity, interest, no_of_payments):
    return annuity // ((interest * pow(1 + interest, no_of_payments)) / (pow(1 + interest, no_of_payments) - 1))


def calculate_payment(annuity, interest, loan):
    return log(annuity / (annuity - interest * loan), 1 + interest)


def calculate_annuity(loan, interest, no_of_payments):
    return loan * ((interest * pow(1 + interest, no_of_payments)) / (pow(1 + interest, no_of_payments) - 1))


def calculate_differentiated(loan, interest, no_of_payments):
    payments = []
    for i in range(no_of_payments):
        payments.append((loan / no_of_payments) + interest * (loan - ((loan * ((i + 1) - 1)) / no_of_payments)))

    return payments


def calculate_overpayment(loan, periods, amount):
    if type(amount) == list:
        amount_paid = sum(amount)
        overpayment = amount_paid - loan
        print(f'Overpayment = {ceil(overpayment)}')
    else:
        amount_paid = periods * amount
        overpayment = amount_paid - loan
        print(f'Overpayment = {ceil(overpayment)}')


def check_negative(num1, num2, num3):
    nums = [num1, num2, num3]
    return any([num.startswith('-') for num in nums])


def convert_numbers(num1, num2, num3):
    # convert string input into the appropriate number: int or float
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


def manage_payment(p, a, i):
    if not check_negative(p, a, i):
        if convert_numbers(p, a, i):
            p, a, i = convert_numbers(p, a, i)
        else:
            return False
    else:
        return False

    i = calculate_interest(i)
    result = calculate_payment(a, i, p)

    result = ceil(result)
    years = result // 12
    months = ceil(result % 12)

    if years == 0 and months > 0:
        periods = 'months' if months > 1 else 'month'
        print(f'It will take {months} {periods} to repay this loan!')
    elif months == 0 and years > 0:
        print(f'It will take {years} years to repay this loan!')
    elif years > 0 and months > 0:
        periods = 'months' if months > 1 else 'month'
        print(f'It will take {years} years and {months} {periods} to repay this loan!')

    return p, years, months, a


def manage_loan(a, n, i):
    if not check_negative(a, n, i):
        if convert_numbers(a, n, i):
            a, n, i = convert_numbers(a, n, i)
        else:
            return False
    else:
        return False

    i = calculate_interest(i)
    result = round(calculate_loan(a, i, n))
    print(f'Your loan principal = {result}!')

    return result, n, a


def manage_annuity(p, n, i):
    if not check_negative(p, n, i):
        if convert_numbers(p, n, i):
            p, n, i = convert_numbers(p, n, i)
        else:
            return False
    else:
        return False

    i = calculate_interest(i)
    result = ceil(calculate_annuity(p, i, n))
    print(f'Your monthly payment = {result}!')
    return p, n, result


def manage_differentiated(p, n, i):
    if not check_negative(p, n, i):
        if convert_numbers(p, n, i):
            p, n, i = convert_numbers(p, n, i)
        else:
            return False
    else:
        return False

    i = calculate_interest(i)
    result = calculate_differentiated(p, i, n)
    # round up all values
    result = [ceil(item) for item in result]

    for i in range(len(result)):
        print(f'Month {i + 1}: payment is {result[i]}')

    return p, n, result


def period_conversion(years, months):
    return (years * 12) + months


def check_args(args):
    unknown = None

    if args.type not in ['diff', 'annuity'] or (args.type == 'diff' and args.payment is not None):
        return False
    if args.interest is None:
        return False
    if args.type == 'diff':
        if args.principal is None or args.periods is None:
            return False
    if args.type == 'annuity':
        if args.periods is None:
            unknown = 'periods'
        elif args.principal is None:
            unknown = 'principal'
        elif args.payment is None:
            unknown = 'payment'

    return args.type, args.interest, args.payment, args.principal, args.periods, unknown


def manage_args(args):
    loan_type, interest, payment, principal, periods, unknown = check_args(args)

    if loan_type == 'diff':
        loan, period, answer = manage_differentiated(principal, periods, interest)
        print()
        calculate_overpayment(loan, period, answer)
    if loan_type == 'annuity':
        if unknown == 'periods':
            loan, year, month, a = manage_payment(principal, payment, interest)
            period = period_conversion(year, month)
            calculate_overpayment(loan, period, a)
        elif unknown == 'payment':
            loan, period, answer = manage_annuity(principal, periods, interest)
            calculate_overpayment(loan, period, answer)
        elif unknown == 'principal':
            p, n, a = manage_loan(payment, periods, interest)
            calculate_overpayment(p, n, a)


parser = argparse.ArgumentParser(description="A simply loan calculator built in Python!")
parser.add_argument('--type', choices=['diff', 'annuity'])
parser.add_argument('--interest')
parser.add_argument('--payment')
parser.add_argument('--principal')
parser.add_argument('--periods')

arguments = parser.parse_args()
if check_args(arguments):
    try:
        manage_args(arguments)
    except TypeError:
        print('Incorrect parameters')
else:
    print('Incorrect parameters')
