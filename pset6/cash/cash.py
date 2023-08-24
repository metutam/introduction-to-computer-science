from cs50 import get_float


def main():
    # Ask how many cents the customer is owed
    cents = get_cents()

    # Calculate the number of quarters to give the customer
    quarters = calculate_quarters(cents)
    cents = cents - quarters * 25

    # Calculate the number of dimes to give the customer
    dimes = calculate_dimes(cents)
    cents = cents - dimes * 10

    # Calculate the number of nickels to give the customer
    nickels = calculate_nickels(cents)
    cents = cents - nickels * 5

    # Calculate the number of pennies to give the customer
    pennies = calculate_pennies(cents)
    cents = cents - pennies * 1

    # Sum coins
    coins = quarters + dimes + nickels + pennies

    # Print total number of coins to give the customer
    print(coins)


def get_cents():
    while True:
        numberOfCents = get_float("Number of cents that a customer is owed: ")
        if numberOfCents >= 0:
            numberOfCents = int(numberOfCents * 100)
            break
    return numberOfCents


def calculate_quarters(cents):
    numberOfQuarters = cents // 25
    return numberOfQuarters


def calculate_dimes(cents):
    numberOfDimes = cents // 10
    return numberOfDimes


def calculate_nickels(cents):
    numberOfNickels = cents // 5
    return numberOfNickels


def calculate_pennies(cents):
    numberOfPennies = cents // 1
    return numberOfPennies


if __name__ == "__main__":
    main()
