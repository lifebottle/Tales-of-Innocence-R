#import sys
#import struct
#import os
## Get the input file and output directory from the command line arguments
#input_file = sys.argv[1]
#output_dir = sys.argv[2]
#file_name = sys.argv[3]
#
## Open the binary file in read-only mode
#with open(input_file, "rb") as f:
#    # Initialize a counter to keep track of the number of blocks
#    block_count = 0
#    
#    # Read the file in chunks of 4 bytes at a time
#    chunk = f.read(4)
#    
#    # Keep reading until we reach the end of the file
#    while chunk:
#        # Check if the chunk is the start of a new block (i.e. "RIFF")
#        if chunk == b"RIFF":
#            # Increment the block count
#            block_count += 1
#            
#            # Create a new file to store the current block
#            block_file = open(f"{output_dir}/{file_name}_{block_count}.at9", "wb")
#            
#            # Write the current chunk (i.e. "RIFF") to the new file
#            block_file.write(chunk)
#            
#            # Read the next chunk from the file
#            chunk = f.read(4)
#            
#            # Keep reading and writing until we reach the end of the current block
#            while chunk != b"RIFF":
#                block_file.write(chunk)
#                chunk = f.read(4)
#            
#            # Close the file for the current block
#            block_file.close()
#        else:
#            # If the current chunk is not the start of a new block, read the next chunk
#            chunk = f.read(4)
#
#print(f"Done! {block_count} blocks found and saved.")


import sys
import struct
import os

# Get the input file and output directory from the command line arguments
input_file = sys.argv[1]
output_dir = sys.argv[2]
file_name = sys.argv[3]

# Open the binary file in read-only mode
with open(input_file, "rb") as f:
    # Initialize a counter to keep track of the number of blocks
    block_count = 0
    
    # Read the file in chunks of 4 bytes at a time
    chunk = f.read(4)
    
    # Keep reading until we reach the end of the file
    while chunk:
        # Check if the chunk is the start of a new block (i.e. "RIFF")
        if chunk == b"RIFF":
            # Increment the block count
            block_count += 1
            
            # Create a new file to store the current block
            block_file = open(f"{output_dir}/{file_name}_{block_count}.at9", "wb")
            
            # Write the current chunk (i.e. "RIFF") to the new file
            block_file.write(chunk)
            
            # Read the next chunk from the file
            chunk = f.read(4)
            
            # Keep reading and writing until we reach the end of the current block
            while chunk != b"RIFF":
                block_file.write(chunk)
                chunk = f.read(4)
                
                # Check if we have reached the end of the file
                if not chunk:
                    # If the end of the file has been reached, save the current block and exit the loop
                    block_file.close()
                    break
            
            # Close the file for the current block
            block_file.close()
        else:
            # If the current chunk is not the start of a new block, read the next chunk
            chunk = f.read(4)

print(f"Done! {block_count} blocks found and saved.")