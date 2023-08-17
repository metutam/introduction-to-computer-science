#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

typedef uint8_t BYTE;

int main(int argc, char *argv[])
{
    // Accept exactly one command-line argument
    if (argc != 2)
    {
        printf("Usage: ./recover IMAGE\n");
        return 1;
    }

    // Open the forensic image for reading
    FILE *file = fopen(argv[1], "r");
    if (file == NULL)
    {
        printf("Could not open %s.\n", argv[1]);
        return 1;
    }

    // Read every block from card.raw
    const int BLOCK_SIZE = 512;
    BYTE buffer[BLOCK_SIZE];
    int counter = 0;
    char fileName[8]; // ###.jpg\0 (\0 is NUL character)
    FILE *img;
    while (fread(buffer, 1, BLOCK_SIZE, file) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if (counter != 0)
            {
                fclose(img);
            }
            sprintf(fileName, "%03i.jpg", counter);
            img = fopen(fileName, "w");
            fwrite(buffer, 1, BLOCK_SIZE, img);
            counter++;
        }
        else if (counter != 0)
        {
            fwrite(buffer, 1, BLOCK_SIZE, img);
        }
    }
    fclose(img);
    fclose(file);
}
