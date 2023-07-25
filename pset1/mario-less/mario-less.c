#include <cs50.h>
#include <stdio.h>

int main(void)
{
    // Check whether the user input is valid
    int height;
    do
    {
        // Prompt user for height of the pyramid
        height = get_int("Height: ");
    }
    while (height < 1 || 8 < height);

    // Print the pyramid on the screen
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < height; j++)
        {
            if (i + j < height - 1)
            {
                printf(" ");
            }
            else if (i + j >= height - 1)
            {
                printf("#");
            }
        }
        printf("\n");
    }

}
