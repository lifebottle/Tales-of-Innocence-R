import pandas as pd
from PIL import ImageFont

def load_letter_values(file_path):
    letter_values = {}

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            for line in file:
                letter, value = line.strip().split()
                letter_values[letter] = int(value)
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
    except ValueError:
        print(f"Error: Invalid format in file '{file_path}'.")

    return letter_values

def calculate_word_sum(word, letter_values):
    word_sum = 0

    for letter in word:
        # Check if the letter is in the dictionary
        if letter in letter_values:
            # Add the value of the letter to the sum
            word_sum += letter_values[letter]
            print(word_sum)
            word_sum += 2#story letter spacing
            print(word_sum)
        else:
            # Handle the case where the letter is not in the dictionary
            print(f"Warning: Letter '{letter}' not found in the dictionary.")

    return word_sum

def calculate_word_sum_total(line, letter_values):
    words = line.split()
    total_sum = 0
    letter_counts = {}

    for word in words:
        word_count = calculate_word_sum(word, letter_values)-2 #last letter doesnt have final spacing
        total_sum += word_count 

        # Count each letter in the word
        for letter in word:
            if letter in letter_counts:
                letter_counts[letter] += 1
            else:
                letter_counts[letter] = 1

        print(f"Word: '{word}', Count: {word_count}")

    # Print letter counts
    print("\nLetter Counts:")
    for letter, count in letter_counts.items():
        print(f"Letter: '{letter}', Count: {count}")

    return total_sum

# Example usage
letter_values_file = 'letter_values.txt'
line_to_calculate = "[ -- Imperial City Regnum -- ]"

# Load the letter values from the file
letter_values = load_letter_values(letter_values_file)

# Calculate the word sum total for the specified line and print word and letter counts
total_sum = calculate_word_sum_total(line_to_calculate, letter_values)

# Print the total word sum
print(f"\nThe word sum total for the line is: {total_sum}")
