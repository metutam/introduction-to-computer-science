#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt the user for a credit card number
    long cardNumber = get_long("Number: ");

    // Find the number of digits and first two digits in the credit card number
    int firstTwoDigits;
    int numberOfDigits = 0;
    long creditCard = cardNumber;
    while (creditCard > 0)
    {
        if (creditCard >= 10 && creditCard <= 99)
        {
            firstTwoDigits = creditCard;
        }

        creditCard /= 10;
        numberOfDigits++;
    }

    // Luhn's Algorithm
    creditCard = cardNumber; // Store the credit card number
    int digitSum = 0;
    for (int i = 0; i < numberOfDigits; i++)
    {
        int digit = creditCard % 10; // Get the last digit
        if (i % 2 == 0) // Add the digits that weren't multiplied by 2
        {
            digitSum += digit;
        }
        else // Multiply each of the second-to-last digit by 2 and add those products' digits together
        {
            digit *= 2;
            if (digit >= 10)
            {
                int n = digit;
                while (n > 0)
                {
                    digitSum += n % 10;
                    n /= 10;
                }
            }
            else
            {
                digitSum += digit;
            }
        }
        creditCard /= 10;
    }

    if (digitSum % 10 == 0) // Checksum
    {
        if (firstTwoDigits == 34 || firstTwoDigits == 37) // Check whether it starts with 34 or 37
        {
            if (numberOfDigits == 15) // Check whether it uses 15-digit numbers
            {
                printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (firstTwoDigits >= 51 && firstTwoDigits <= 55) // Check whether it starts with 51, 52, 53, 54, or 55
        {
            if (numberOfDigits == 16) // Check whether it uses 16-digit numbers
            {
                printf("MASTERCARD\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else if (firstTwoDigits >= 40 && firstTwoDigits <= 49) // Check whether it starts with 4
        {
            if (numberOfDigits == 13 || numberOfDigits == 16) // Check whether it uses 13- and 16-digit numbers
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}
