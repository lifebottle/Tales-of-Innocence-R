import pandas as pd

def load_letter_values(file_path):
    letter_values = {}

    try:
        with open(file_path, 'r',encoding='utf-8') as file:
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
            #add the 1 pixel of space between word
            word_sum += 2#story has +2 letter spacing
        else:
            # Handle the case where the letter is not in the dictionary
            print(f"Warning: Letter '{letter}' not found in the dictionary.")

    return word_sum


def wordwrap_column(csv_file, column, linebreak, wrap_length, font_file, letter_values_file):
  # Load the letter values from the file
  letter_values = load_letter_values(letter_values_file)
  
  # Read the CSV file into a pandas DataFrame
  df = pd.read_csv(csv_file, encoding='utf-8')


  # Wordwrap the text in the specified column of each row
  for index, row in df.iterrows():
    if row[linebreak] == True:
        text = row[column]
        # Remove trailing white space
        text = text.rstrip()
        # Remove double white spaces
        text = " ".join(text.split())
        # Remove existing line breaks
        text = text.replace("\n", " ")
        wrapped_text = ""
        line = ""
        line_length = 0
        
        for word in text.split(" "):
          line_length += calculate_word_sum(word, letter_values)-2 #-2 remove the last letter spacing
              
          if line_length > wrap_length:
            # If so, add the current line to the wrapped text and start a new line
            wrapped_text += line.rstrip(" ") + "\n" #removing trailing white space
            #line = ""
            line = word + ' '
            line_length = calculate_word_sum(word, letter_values)+18 #for white spaces
          else:  
            # Add the word to the current line
            line += word + " "
            #line_length += calculate_word_sum(word, letter_values)+17 #for white spaces
            line_length += 18 #for white spaces
        
        # Add the remaining line to the wrapped text
        wrapped_text += line
        df.at[index, column] = wrapped_text.rstrip(" ")
        line_length = 0
        
        
        if len(wrapped_text.split("\n")) > 3:
            print(f"In {csv_file}: Cell in row {index +2} has more than 3 lines after wordwrapping" + '\n')
            print(wrapped_text + "\n====================\n")

  # Write the modified DataFrame back to the CSV file
  df.to_csv(csv_file, index=False, encoding='utf-8')
  
# Example usage
wordwrap_column(r'../../2_translated/Story.csv', 'English', 'LineBreak', 658, 'DFGHSGothic-W5-03.ttf','letter_values.txt')
wordwrap_column(r'../../2_translated/MapData.csv', 'English', 'LineBreak', 658, 'DFGHSGothic-W5-03.ttf','letter_values.txt')

