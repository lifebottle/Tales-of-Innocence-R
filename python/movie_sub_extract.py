import struct
import csv

def get_captions():
    subs = []
    f = open("C:/Users/pvnn/Desktop/MovieCaption_019.dat", "rb")

    # Check total number of lines in subtitles, in this case 60 lines (Long unsigned integer)
    lines = struct.unpack('<L', f.read(4))[0]

    # Move to 0x10
    f.seek(0x10)

    # Check the 60 lines for time and caption
    while line < lines

    # Read the next 4 bytes to get the time in float
    # read next 252 bytes convert to text
    # store in dictionary or something
    subs.append([struct.unpack('<f', f.read(4))[0], b"something".decode("utf-8")])
    line += 1

    # Write to a CSV file      
    f.close()
    
