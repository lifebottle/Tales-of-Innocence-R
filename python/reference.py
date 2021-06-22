with open('utf-8.tbl', 'w', encoding='utf-8') as f:
    for i in range(0x20, 0x10000):
        try:
            utf8 = chr(i).encode('utf-8')
            for b in utf8:
                f.write(f'{b:02X}')
            f.write(f'={chr(i)}\n')
        except:
            pass
