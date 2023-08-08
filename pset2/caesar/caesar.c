#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

// Prototype of the functions
bool only_digits(string s);
char rotate(char c, int n);

int main(int argc, string argv[])
{
    // Check whether it accepts only a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1; // A non-zero exit status indicates some error to the system
    }

    // Check whether it contains only digits
    string str = argv[1];
    bool onlyNumbers = only_digits(str);
    if (onlyNumbers == false)
    {
        printf("Usage: ./caesar key\n");
        return 1; // A non-zero exit status indicates some error to the system
    }

    // Check whether the key is a non-negative integer
    int key = atoi(argv[1]);
    if (key < 0)
    {
        printf("Usage: ./caesar key\n");
        return 1; // A non-zero exit status indicates some error to the system
    }

    string plainText = get_string("plaintext:  ");

    // Rotate the character by that many positions
    printf("ciphertext: ");
    for (int i = 0, n = strlen(plainText); i < n; i++)
    {
        char rotatedChar = rotate(plainText[i], key);
        printf("%c", rotatedChar);
    }
    printf("\n");

    return 0; // A zero exit status indicates nothing went wrong to the system
}

bool only_digits(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isdigit(s[i]) == 0)
        {
            return false;
        }
    }
    return true;
}

char rotate(char c, int n)
{
    if (isupper(c))
    {
        c = (c - 65 + n) % 26;
        return c + 65;
    }
    else if (islower(c))
    {
        c = (c - 97 + n) % 26;
        return c + 97;
    }
    else
    {
        return c;
    }
}
