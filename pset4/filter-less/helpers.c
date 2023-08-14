#include <math.h>

#include "helpers.h"

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            // Divide the sum of these integers by 3.0 and not 3
            int average = round((image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue) / 3.0);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int sepiaRed = round(.393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue);
            int sepiaGreen = round(.349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue);
            int sepiaBlue = round(.272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue);

            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }

            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }

            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            int tmpRed = image[i][j].rgbtRed;
            image[i][j].rgbtRed = image[i][(width - 1) - j].rgbtRed;
            image[i][(width - 1) - j].rgbtRed = tmpRed;

            int tmpGreen = image[i][j].rgbtGreen;
            image[i][j].rgbtGreen = image[i][(width - 1) - j].rgbtGreen;
            image[i][(width - 1) - j].rgbtGreen = tmpGreen;

            int tmpBlue = image[i][j].rgbtBlue;
            image[i][j].rgbtBlue = image[i][(width - 1) - j].rgbtBlue;
            image[i][(width - 1) - j].rgbtBlue = tmpBlue;
        }
    }
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    // Create a copy of image and surround it with 0s
    RGBTRIPLE copy[height + 2][width + 2];
    for (int i = 0; i < height + 2; i++)
    {
        for (int j = 0; j < width + 2; j++)
        {
            if (i == 0 || j == 0 || i == width + 1 || j == width + 1)
            {
                copy[i][j].rgbtRed = 0;
                copy[i][j].rgbtGreen = 0;
                copy[i][j].rgbtBlue = 0;
            }
            else
            {
                copy[i][j].rgbtRed = image[i - 1][j - 1].rgbtRed;
                copy[i][j].rgbtGreen = image[i - 1][j - 1].rgbtGreen;
                copy[i][j].rgbtBlue = image[i - 1][j - 1].rgbtBlue;
            }
        }
    }

    // Change the pixels’ colors in the image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            int averageRed = 0;
            int averageGreen = 0;
            int averageBlue = 0;

            for (int k = 0; k < 3; k++)
            {
                for (int l = 0; l < 3; l++)
                {
                    averageRed = averageRed + copy[i + k][j + l].rgbtRed;
                    averageGreen = averageGreen + copy[i + k][j + l].rgbtGreen;
                    averageBlue = averageBlue + copy[i + k][j + l].rgbtBlue;
                }
            }

            if (i + j == 0 || (i == 0 && j == width - 1) || (i == height - 1 && j == 0) || (i == height - 1 && j == width - 1))
            {
                averageRed = round(averageRed / 4.0);
                averageGreen = round(averageGreen / 4.0);
                averageBlue = round(averageBlue / 4.0);
            }
            else if (i == 0 || j == 0 || i == width - 1 || j == width - 1)
            {
                averageRed = round(averageRed / 6.0);
                averageGreen = round(averageGreen / 6.0);
                averageBlue = round(averageBlue / 6.0);
            }
            else
            {
                averageRed = round(averageRed / 9.0);
                averageGreen = round(averageGreen / 9.0);
                averageBlue = round(averageBlue / 9.0);
            }

            image[i][j].rgbtRed = averageRed;
            image[i][j].rgbtGreen = averageGreen;
            image[i][j].rgbtBlue = averageBlue;
        }
    }
}