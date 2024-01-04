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
        else:
            # Handle the case where the letter is not in the dictionary
            print(f"Warning: Letter '{letter}' not found in the dictionary.")

    return word_sum

def wordwrap_column(csv_file, english, linebreak, field, wrap_length, letter_values_file):
  # Load the letter values from the file
  letter_values = load_letter_values(letter_values_file)
  # Read the CSV file into a pandas DataFrame
  df = pd.read_csv(csv_file, encoding='utf-8')


  # Wordwrap the text in the specified column of each row
  for index, row in df.iterrows():
    if row[linebreak] == True:
        text = row[english]
        # Remove trailing white space
        text = text.rstrip()
        # Remove double white spaces
        text = " ".join(text.split())
        # Remove existing line breaks
        text = text.replace("\n", " ")
        wrapped_text = ""
        line = ""
        
        #Logic for line addition
        if row[field] == "line_addition":
            line_length = last_line
            text = " " + text
        else:
            line_length = 0
            last_line = 0
        
        for word in text.split(" "):
          line_length += calculate_word_sum(word, letter_values)
              
          if line_length > wrap_length:
            # If so, add the current line to the wrapped text and start a new line
            wrapped_text += line.rstrip(" ") + "\n" #removing trailing white space
            #line = ""
            line = word + ' '
            line_length = calculate_word_sum(word, letter_values)+14 #for white spaces
          else:  
            # Add the word to the current line
            line += word + " "
            #line_length += calculate_word_sum(word, letter_values)+17 #for white spaces
            line_length += 14 #for white spaces
        
        # Add the remaining line to the wrapped text
        wrapped_text += line
        df.at[index, english] = wrapped_text.rstrip(" ")
        last_line = line_length - 14 #for the skit line_addition scenario
        line_length = 0
        
        if len(wrapped_text.split("\n")) > 3:
            print(f"Cell in row {index +2} has more than 3 lines after wordwrapping" + '\n')
            print(wrapped_text + "\n====================\n")

  # Write the modified DataFrame back to the CSV file
  df.to_csv(csv_file, index=False, encoding='utf-8')
  
  # Example usage
wordwrap_column(r'../../2_translated/Skit.csv', 'English', 'LineBreak', 'Field', 600, 'letter_values_skit.txt')