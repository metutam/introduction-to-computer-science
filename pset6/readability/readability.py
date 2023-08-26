from cs50 import get_string

# Assume that a sentence will contain at least one word
# Assume that a sentence will not start or end with a space
# Assume that a sentence will not have multiple spaces in a row


def main():
    # Prompt user for a string
    text = get_string("Text: ")
    l = count_letters(text)
    w = count_words(text)
    s = count_sentences(text)

    # Calculate the average letters and sentences per 100 words
    L = l * 100 / w
    S = s * 100 / w

    # Compute the grade level by the Coleman-Liau formula
    index = 0.0588 * L - 0.296 * S - 15.8

    # Print the grade level
    if index < 1:
        print("Before Grade 1")
    elif index >= 1 and index < 16:
        print(f"Grade {round(index)}")
    else:
        print("Grade 16+")


# Count the number of letters in the text
def count_letters(text):
    counter = 0
    for char in text:
        if char.isalpha():
            counter += 1
    return counter


# Count the number of words in the text
def count_words(text):
    counter = 0
    for char in text:
        if char.isspace():
            counter += 1
    # Text will not end with a space (increment by 1)
    return counter + 1


# Count the number of sentences in the text
def count_sentences(text):
    counter = 0
    for char in text:
        if char == "." or char == "!" or char == "?":
            counter += 1
    return counter


if __name__ == "__main__":
    main()
