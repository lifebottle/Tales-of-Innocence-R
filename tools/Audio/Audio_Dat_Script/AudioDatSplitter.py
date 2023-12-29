import sys
import struct
import os

# Constants for the header
HEADER_SIZE = 0x30
CHUNK_POINTER_OFFSETS = [0x10, 0x18, 0x20]
CHUNK_SIZE_OFFSETS = [0x14, 0x1C, 0x24]
CHUNK_EXTENTION = "RIFF", "PPEF", "EPHD"

# Get the input file and output directory from the command line arguments
input_file = sys.argv[1]
output_dir = sys.argv[2]
file_name = sys.argv[3]

# Open the input file in binary mode
with open(input_file, 'rb') as f:
  # Read the header
  header = f.read(HEADER_SIZE)
  
  # Get the number of chunks from the header
  num_chunks = struct.unpack('<i', header[:4])[0]
  
  # Create the output directory if it doesn't exist
  if not os.path.exists(output_dir):
    os.makedirs(output_dir)
  
  # Iterate over the chunks
  for i in range(num_chunks):
    # Get the chunk pointer and size from the header
    chunk_pointer = struct.unpack('<i', header[CHUNK_POINTER_OFFSETS[i]:CHUNK_POINTER_OFFSETS[i]+4])[0]
    chunk_size = struct.unpack('<i', header[CHUNK_SIZE_OFFSETS[i]:CHUNK_SIZE_OFFSETS[i]+4])[0]
    chunk_extension = CHUNK_EXTENTION[i]
    
    
    # Seek to the chunk pointer in the input file
    f.seek(chunk_pointer)
    
    # Read the chunk data
    chunk_data = f.read(chunk_size)
    
    # Save the chunk data to the output directory
    with open(f'{output_dir}/{file_name}.{chunk_extension}', 'wb') as chunk_file:
      chunk_file.write(chunk_data)
      
print(f"Done!{file_name}")