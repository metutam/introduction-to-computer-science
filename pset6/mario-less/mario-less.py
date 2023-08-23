from cs50 import get_int

# Check whether the user input is valid
while True:
    # Prompt user for height of the pyramid
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

# Print the pyramid on the screen
for i in range(height):
    for j in range(height):
        if i + j < height - 1:
            print(" ", end="")
        else:
            print("#", end="")
    print()
