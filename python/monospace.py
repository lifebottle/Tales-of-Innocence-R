import sys

def monospace1():
    eboot = open('patched/eboot.bin', 'r+b')
    eboot.seek(0x7B5E)
    eboot.write(b'\x00\x23')
    eboot.close()

def monospace2():
    eboot = open('patched/eboot.bin', 'r+b')
    eboot.seek(0x8630)
    eboot.write(b'\x40\x18')
    eboot.close()

if __name__ == '__main__':
    if sys.argv[1] == '1':
        monospace1()
        monospace2()
