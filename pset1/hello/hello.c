#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Prompt user for their name
    string answer = get_string("What's your name? ");

    // Print greeting using the user's input
    printf("Hello, %s\n", answer);
}
