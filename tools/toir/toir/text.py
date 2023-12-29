import re
import struct

_ICONS_40 = {
    0x0406: 'left_analog',
    0x0706: 'start',
    0x0906: 'dpad_r',
    0x0a06: 'dpad_d',
    0x0b06: 'dpad_l',
    0x0c06: 'dpad_u',
    0x0d06: 'dpad_lr',
    0x0d06: 'dpad_du',
    0x0f06: 'dpad',
    0x0083: 'icon_fire',
    0x0183: 'icon_earth',
    0x0283: 'icon_wind',
    0x0383: 'icon_water',
    0x0483: 'icon_lightning',
    0x0583: 'icon_light',
    0x0683: 'icon_dark',
    0x0783: 'icon_poison',
    0x0883: 'icon_weak',
    0x0a83: 'icon_paralysis',
    0x0b83: 'icon_fear',
    0x0c83: 'icon_patk',
    0x0d83: 'icon_adef',
    0x0e83: 'icon_aatk',
    0x0f83: 'icon_pdef',
}

_BUTTONS_41 = {
    0x00: 'circle',
    0x01: 'cross',
    0x02: 'square',
    0x03: 'triangle',
    0x04: 'l1',
    0x05: 'l2'
}

_COLORS = {
    0x01: 'red',
    0x02: 'cyan',
    0x03: 'blue',
    0x04: 'white',
}

def decode_control_code(text, i):
    try:
        code = text[i + 1]
        if code == 0x01:
            arg = text[i + 3]
            if arg in _COLORS:
                return f'{{{_COLORS[arg]}}}', i + 4
            else:
                return '{x01}', i + 2        
        elif code == 0x02:
            index = text[i + 3] + (text[i + 4] << 8)
            return f'{{item:0x{index:04X}}}', i + 5
        elif code == 0x03:
            index = text[i + 3] + (text[i + 4] << 8)
            return f'{{unknown03:0x{index:04X}}}', i + 5
        elif code == 0x04:
            index = text[i + 3] + (text[i + 4] << 8)
            return f'{{number:0x{index:04X}}}', i + 5
        elif code == 0x05:
            arg = text[i + 3]
            if arg == 0x01:
                return '{variable}', i + 4
            elif arg == 0x02:
                return '{fixed}', i + 4
            else:
                return '{x05}', i + 2
        elif code == 0x40:
            index = text[i + 3] + ((text[i + 4]) << 8)
            if index in _ICONS_40:
                return _ICONS_40[index], i + 5
            else:
                return f'{{icon:0x{index:04X}}}', i + 5
        elif code == 0x41:
            index = text[i + 3]
            if index in _BUTTONS_41:
                return '{remap_' + _BUTTONS_41[index] + '}', i + 4
            else:
                return f'{{button:0x{index:02X}}}', i + 4
        elif code == 0x42:
            return '{triverse}', i + 2
        else:
            return f'{{x{code:02X}}}', i + 2
    except Exception as e:
        raise ValueError(str(e) + f' ("{text}")')

_PUNCTUATION = r'…\u3000、？！!《》○―＝\n♪【】「｢｣」』）～〜・々)'
_REDUNDANT_FIXED = re.compile(f'{{fixed}}(?P<chars>[{_PUNCTUATION}]+)({{variable}}|$)')
_REDUNDANT_VARIABLE = re.compile(f'^{{variable}}[^{_PUNCTUATION}]')

def _remove_spacing_cc(match):
    return match.group('chars')

def _remove_variable_cc(match):
    return match.group(0).replace('{variable}', '')

def remove_redundant_cc(text):
    removed = re.sub(_REDUNDANT_FIXED, _remove_spacing_cc, text)
    return re.sub(_REDUNDANT_VARIABLE, _remove_variable_cc, removed)

def get_next_end(buffer, offset, end):
    i = buffer.find(b'\x00', offset)
    if i == -1:
        return end
    else:
        return min(i + 1, end)

def decode_text_and_offset(buffer, offset, max_len=0):
    if not max_len:
        end = len(buffer)
    else:
        end = offset + max_len

    next_at = buffer.find(b'@', offset)
    next_end = get_next_end(buffer, offset, end)
    last = offset
    text = ''
    while next_at != -1 and next_at < next_end:
        text += buffer[last:next_at].decode('utf-8')
        cc, last = decode_control_code(buffer, next_at)
        text += cc
        next_at = buffer.find(b'@', last)
        next_end = get_next_end(buffer, last, end)
    text += buffer[last:next_end].decode('utf-8')
    return text.replace('\r', '').replace('\0', ''), next_end

def decode_text(buffer, offset, max_len=0):
    text = decode_text_and_offset(buffer, offset, max_len)[0]
    if text and text[-1] == '\0':
        return text[:-1]
    else:
        return text

def decode_text_fixed(buffer, offset, length):
    return decode_text(buffer, offset, length)

_FIXED_CC = {
    'variable': b'@\x05@\x01',
    'fixed': b'@\x05@\x02',
    'triverse': b'@B',
}
_FIXED_CC |= {
    key: b'@\x40@' + struct.pack('<H', index) for index, key in _ICONS_40.items()
}
_FIXED_CC |= {
    key: b'@\x41@' + struct.pack('<B', index) for index, key in _BUTTONS_41.items()
}
_FIXED_CC |= {
    key: b'@\x01@' + struct.pack('<B', index) for index, key in _COLORS.items()
}

def encode_control_code(text):
    if ':' in text:
        code, arg = text.split(':')
    else:
        code = text

    encoded = _FIXED_CC.get(code, None)
    if encoded:
        return encoded
    
    if code == 'item':
        return b'@\x02@' + struct.pack('<H', int(arg, 0))
    elif code == 'number':
        return b'@\x04@' + struct.pack('<H', int(arg, 0))
    elif code == 'icon':
        return b'@\x40@' + struct.pack('<H', int(arg, 0))
    elif code == 'button':
        return b'@\x41@' + struct.pack('<B', int(arg, 0))

    if code[0] == 'x' and len(code) == 3:
        return struct.pack('B', int(code[1:], 16))

    raise ValueError(f'unknown control code: {code}')

def encode_text(string):
    return encode_text_fixed(string) + b'\0'

def encode_text_fixed(string):
    string = string.replace('\r', '').replace('\n', '\r\n')
    buffer = bytes()
    next_cc = string.find('{')
    next_cc_end = 0
    while next_cc != -1:
        buffer += string[next_cc_end:next_cc].encode('utf-8')
        next_cc += 1
        next_cc_end = string.find('}', next_cc)
        buffer += encode_control_code(string[next_cc:next_cc_end]);
        next_cc = string.find('{', next_cc)
        next_cc_end += 1
    buffer += string[next_cc_end:].encode('utf-8')
    return buffer
