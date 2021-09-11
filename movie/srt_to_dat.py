from collections import namedtuple
from itertools import groupby, zip_longest
import re, struct, os, sys

rTIME_STAMP = r"(\d+):(\d+):(\d+),(\d+)"
subtitle = namedtuple('Subtitle', 'number start end content')
MAX_SUB_SIZE = 0x100
MAX_LINE_SIZE = 0xFB
HEADER_SIZE = 0x10

def get_file_name_noext(path):
    return os.path.splitext(os.path.basename(path))[0]

def srt_time_to_seconds(time_stamp:str):
    times = [int(s) for s in re.findall(rTIME_STAMP, time_stamp)[0]]
    seconds = float(times[0] * 60) #hours
    seconds += times[1] * 60       #minutes
    seconds += times[2]            #seconds
    seconds += times[3] / 1000     #miliseconds
    return seconds

def get_sub_pos(sub:int):
    return sub * MAX_SUB_SIZE + HEADER_SIZE

def insert_sub_into(buf:bytearray,sub:subtitle,index:int):
    assert len(sub.content) <= MAX_LINE_SIZE, "Subtitle line %02d is too long!" % sub.number
    struct.pack_into("<f%ds" % len(sub.content),buf,get_sub_pos(index),sub.start,sub.content)

def get_subs(filename:str):
# simple srt parser from: https://stackoverflow.com/a/23620587
# "chunk" our input file, delimited by blank lines
    with open(filename, encoding="utf8") as f:
        res = [list(g) for b,g in groupby(f, lambda x: bool(x.strip())) if b]

    subs = []

    for sub,sub_n in zip_longest(res, res[1:]):
        assert len(sub) >= 3, "Invalid subtitle entry in file: %s" % filename
        sub = [x.strip() for x in sub]
        number = sub[0]
        start, end = [srt_time_to_seconds(t) for t in sub[1].split(' --> ')]
        content = str.encode("\r\n".join(sub[2:]))
        subs.append(subtitle(number, start, end, content))
        
        if sub_n != None:
            assert len(sub_n) >= 3, "Invalid subtitle entry in file: %s" % filename
            sub_n = [x.strip() for x in sub_n]
            start_n, _ = [srt_time_to_seconds(t) for t in sub_n[1].split(' --> ')]
            if end != start_n:
                subs.append(subtitle(-1, end, start_n, b"\x00"))
        else:
            subs.append(subtitle(-1, end, end, b"\x00"))
    
    return subs


srt_files = []
for file in os.listdir(os.getcwd()):
    if file.endswith(".srt"):
        srt_files.append(file)

print("Found %02d srt files in path: %s" % (len(srt_files), os.getcwd()))
for p_files, file in zip(range(1,len(srt_files)+1),srt_files):
    print("Converting file %02d/%02d..." % (p_files, len(srt_files)), end="\r")
    subs = get_subs(file)

    dat_file = bytearray(len(subs) * MAX_SUB_SIZE + HEADER_SIZE)
    struct.pack_into("<i",dat_file,0,len(subs))

    for i, sub in zip(range(len(subs)),subs):
        insert_sub_into(dat_file,sub,i)

    out_name = get_file_name_noext(file) + ".dat"
    with open(out_name, mode="wb+") as f:
        f.write(bytes(dat_file))

print("Converted %02d/%02d files." % (p_files, len(srt_files)))
print("Done!")


