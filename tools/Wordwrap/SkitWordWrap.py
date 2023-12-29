import pandas as pd
from PIL import Image, ImageDraw, ImageFont

def wordwrap_column(csv_file, english, linebreak, field, wrap_length, font_file, exceptions_file):
  # Load the font
  font = ImageFont.truetype(font_file, 10)
  

  # Read the CSV file into a pandas DataFrame
  df = pd.read_csv(csv_file, encoding='utf-8')

  # Load the exceptions file into a dictionary with the exception strings as keys and their lengths as values
  exceptions = {}
  with open(exceptions_file, 'r') as f:
    for line in f:
      exception, length = line.strip().split(';')
      exceptions[exception] = int(length)

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
        if row[field] == "line_addition":
            line_length = last_line
            text = " " + text
        else:
            line_length = 0
            last_line = 0
        
        for word in text.split(" "):
          # If the word is an exception, add its length to the line length
          if word in exceptions:
              line_length += (exceptions[word] + font.getlength(" "))
          else:
              line_length += font.getlength(word + " ")
              
        #if font.getlength(line + word) > wrap_length and word not in exceptions:
          if line_length > wrap_length:
            # If so, add the current line to the wrapped text and start a new line
            wrapped_text += line.rstrip(" ") + "\n" #removing trailing white space
            line = ""
            line_length = font.getlength(word + " ")
            
          # Add the word to the current line
          line += word + " "
        # Add the remaining line to the wrapped text
        wrapped_text += line
        df.at[index, english] = wrapped_text.rstrip(" ")
        last_line = line_length - font.getlength(" ") #for the skit line_addition scenario
        line_length = 0
        
        if len(wrapped_text.split("\n")) > 3:
            print(f"Cell in row {index +2} has more than 3 lines after wordwrapping" + '\n')
            print(wrapped_text + "\n====================\n")

  # Write the modified DataFrame back to the CSV file
  df.to_csv(csv_file, index=False, encoding='utf-8')
  
  # Example usage
wordwrap_column(r'../../2_translated/Skit.csv', 'English', 'LineBreak', 'Field', 257, 'arial.ttf', 'exceptions.txt')