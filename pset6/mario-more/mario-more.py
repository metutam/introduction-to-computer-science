from cs50 import get_int

# Check whether the user input is valid
while True:
    # Prompt user for height of the pyramid
    height = get_int("Height: ")
    if height >= 1 and height <= 8:
        break

for i in range(height):
    # Print the left-side of the pyramid on the screen
    for j in range(height):
        if i + j < height - 1:
            print(" ", end="")
        else:
            print("#", end="")
    # Print two spaces between two pyramids
    print("  ", end="")
    # Print the right-side of the pyramid on the screen
    for k in range(height):
        if i >= k:
            print("#", end="")
    # Print a new line
    print()
