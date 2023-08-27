import csv
import sys

#  Assume that the first argument is indeed the filename of a valid CSV file
#  Assume that the second argument is the filename of a valid text file


def main():

    # Check for command-line usage
    if len(sys.argv) != 3:
        print("Missing command-line argument.")

    # Read database file into a variable
    people = []
    with open(sys.argv[1], "r") as file:
        reader = csv.reader(file)
        for row in reader:
            people.append(row)

    # Read DNA sequence file into a variable
    with open(sys.argv[2], "r") as file:
        dna = file.read()

    # Find longest match of each STR in DNA sequence
    longestMatches = []
    for firstRow in people[0:1]:
        for strs in firstRow[1:]:
            longestMatch = longest_match(dna, strs)
            longestMatches.append(longestMatch)

    # Check database for matching profiles
    length = len(longestMatches)
    for person in people[1:]:
        counter = 0
        for i in range(length):
            if int(person[i + 1]) == int(longestMatches[i]):
                counter += 1
        if counter == length:
            print(person[0])
            return
    print("No match")


def longest_match(sequence, subsequence):
    """Returns length of longest run of subsequence in sequence."""

    # Initialize variables
    longest_run = 0
    subsequence_length = len(subsequence)
    sequence_length = len(sequence)

    # Check each character in sequence for most consecutive runs of subsequence
    for i in range(sequence_length):

        # Initialize count of consecutive runs
        count = 0

        # Check for a subsequence match in a "substring" (a subset of characters) within sequence
        # If a match, move substring to next potential match in sequence
        # Continue moving substring and checking for matches until out of consecutive matches
        while True:

            # Adjust substring start and end
            start = i + count * subsequence_length
            end = start + subsequence_length

            # If there is a match in the substring
            if sequence[start:end] == subsequence:
                count += 1

            # If there is no match in the substring
            else:
                break

        # Update most consecutive matches found
        longest_run = max(longest_run, count)

    # After checking for runs at each character in seqeuence, return longest run found
    return longest_run


main()
