import os

def search_byte_sequence(directory, byte_sequence):
    """
    Search for a specific byte sequence in all files within the given directory and its subdirectories.
    
    Args:
        directory (str): The directory to start the search from.
        byte_sequence (bytes): The byte sequence to search for.
    """
    for root, _, files in os.walk(directory):
        for file_name in files:
            file_path = os.path.join(root, file_name)
            try:
                with open(file_path, 'rb') as file:
                    data = file.read()
                    if byte_sequence in data:
                        print(f"Found byte sequence in file: {file_path}")
            except Exception as e:
                print(f"Could not read file {file_path}: {e}")

if __name__ == "__main__":
    # Define the directory to search and the byte sequence
    search_directory = "0_gamefiles"
    byte_sequence = b'\x07\x77\x77\x77\x77'

    # Run the search
    search_byte_sequence(search_directory, byte_sequence)