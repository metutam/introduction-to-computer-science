#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

// Prototype of the functions
bool only_alphabetical(string s);
bool exactly_once(string s);
char rotate(char c, string s);

int main(int argc, string argv[])
{
    // Check whether it accepts only a single command-line argument
    if (argc != 2)
    {
        printf("Usage: ./substitution key\n");
        return 1; // A non-zero exit status indicates some error to the system
    }

    // Check whether the key contains 26 characters
    if (strlen(argv[1]) != 26)
    {
        printf("Key must contain 26 characters.\n");
        return 1; // A non-zero exit status indicates some error to the system
    }

    // Check whether the key contains only alphabetic characters
    string str = argv[1];
    bool onlyAlpha = only_alphabetical(str);
    if (onlyAlpha == false)
    {
        printf("Key must contain only alphabetic characters.\n");
        return 1; // A non-zero exit status indicates some error to the system
    }

    // Check whether the key contains each letter exactly once
    bool justOnce = exactly_once(str);
    if (justOnce == false)
    {
        printf("Key must contain each letter exactly once.\n");
        return 1; // A non-zero exit status indicates some error to the system
    }

    string plainText = get_string("plaintext:  ");

    // Rotate the character by that corresponding key
    printf("ciphertext: ");
    for (int i = 0, n = strlen(plainText); i < n; i++)
    {
        char rotatedChar = rotate(plainText[i], str);
        printf("%c", rotatedChar);
    }
    printf("\n");

    return 0; // A zero exit status indicates nothing went wrong to the system
}

bool only_alphabetical(string s)
{
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        if (isalpha(s[i]) == 0)
        {
            return false;
        }
    }
    return true;
}

bool exactly_once(string s)
{
    int n = strlen(s);
    for (int i = 0; i < n; i++)
    {
        s[i] = tolower(s[i]);
    }
    for (int i = 0; i < n; i++)
    {
        for (int j = 0; j < n - i; j++)
        {
            if (s[i] == s[i + j + 1])
            {
                return false;
            }
        }
    }
    return true;
}

char rotate(char c, string s)
{
    if (isupper(c))
    {
        c = s[c - 65];
        return toupper(c);
    }
    else if (islower(c))
    {
        c = s[c - 97];
        return tolower(c);
    }
    else
    {
        return c;
    }
}
