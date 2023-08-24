from cs50 import get_int
from re import search


# Prompt the user for a credit card number
cardNumber = get_int("Number: ")

# Find the number of digits and first two digits in the credit card number
card = str(cardNumber)
numberOfDigits = len(card)
firstTwoDigits = card[0:2]

# Luhn's Algorithm

digitSum = 0
# Multiply each of the second-to-last digit by 2 and add those products' digits together
for digit in card[-2::-2]:
    digit = int(digit)
    digit *= 2
    if digit >= 10:
        digit = str(digit)
        for d in digit[:]:
            digitSum += int(d)
    else:
        digitSum += int(digit)

# Add the digits that weren't multiplied by 2
for digit in card[-1::-2]:
    digitSum += int(digit)

# Checksum
if digitSum % 10 == 0:
    # Check whether it starts with 34 or 37
    if int(firstTwoDigits) == 34 or int(firstTwoDigits) == 37:
        # Check whether it uses 15-digit numbers
        pattern = r"^[0-9]{15}$"
        if search(pattern, card):
            print("AMEX")
        else:
            print("INVALID")
    # Check whether it starts with 51, 52, 53, 54, or 55
    elif int(firstTwoDigits) >= 51 and int(firstTwoDigits) <= 55:
        # Check whether it uses 16-digit numbers
        pattern = r"^[0-9]{16}$"
        if search(pattern, card):
            print("MASTERCARD")
        else:
            print("INVALID")
    # Check whether it starts with 4
    elif int(firstTwoDigits) >= 40 and int(firstTwoDigits) <= 49:
        # Check whether it uses 13- and 16-digit numbers
        pattern = r"^[0-9]{13,16}$"
        if search(pattern, card):
            print("VISA")
        else:
            print("INVALID")
    else:
        print("INVALID")
else:
    print("INVALID")
