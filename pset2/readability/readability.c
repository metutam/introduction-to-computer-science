#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

// Assume that a sentence will contain at least one word
// Assume that a sentence will not start or end with a space
// Assume that a sentence will not have multiple spaces in a row

// Prototype of the functions
int count_letters(string text);
int count_words(string text);
int count_sentences(string text);

int main(void)
{
    // Prompt user for a string
    string text = get_string("Text: ");
    float l = count_letters(text);
    float w = count_words(text);
    float s = count_sentences(text);

    // Calculate the average letters and sentences per 100 words
    float L = l * 100 / w;
    float S = s * 100 / w;

    // Compute the grade level by the Coleman-Liau formula
    float index = 0.0588 * L - 0.296 * S - 15.8;

    // Print the grade level
    if (index < 1)
    {
        printf("Before Grade 1\n");
    }
    else if (index >= 1 && index < 16)
    {
        printf("Grade %i\n", (int) round(index));
    }
    else
    {
        printf("Grade 16+\n");
    }
}

// Count the number of letters in the text
int count_letters(string text)
{
    int counter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isalpha(text[i]))
        {
            counter++;
        }
    }
    return counter;
}

// Count the number of words in the text
int count_words(string text)
{
    int counter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (isspace(text[i]))
        {
            counter++;
        }
    }
    return counter + 1; // Text will not end with a space (increment by 1)
}

// Count the number of sentences in the text
int count_sentences(string text)
{
    int counter = 0;
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '.' || text[i] == '!' || text[i] == '?')
        {
            counter++;
        }
    }
    return counter;
}
