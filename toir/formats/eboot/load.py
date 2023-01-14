import hashlib

def address_to_offset(address):
    return address - 0x80FFE000

def offset_to_address(offset):
    return offset + 0x80FFE000

_EBOOT_ELF_HASH = ("93ce22efa901de4a7013aa7dee99aad4"
                   "60226ad5705f5f90098c875d8ac92aa7"
                   "5517c5c11a8b9e4d78bf164644b8a942"
                   "f6da123db62667df5825e29ae4221a98")

_EBOOT_BIN_HASH = ('b4894e29fb37ddcc5ef5c9daa65499a6'
                   '977396b7c4ad021eae0a72b7c962b023'
                   '5236275f583094d2e51c59a4c0695c47'
                   '37e835b03094ad313e849c6e3941b94f')

_EBOOT_BIN_ENCRYPTED_HASH = ('3b64bec6656bcacd5ea03bad96c6f9be'
                             '4bc065cef10a285775d4f44359b4b2de'
                             'c0f9663dd1b4fe4b51d79479077db5b5'
                             'cc896977f5ab96de813934a838459c06')

def load_eboot(ebootpath, elf_okay=True):
    with open(ebootpath, 'rb') as f:
        eboot = f.read()
        return eboot
    hash = hashlib.blake2b(eboot).hexdigest()

    if hash == _EBOOT_BIN_HASH:
        return eboot
    elif hash == _EBOOT_BIN_ENCRYPTED_HASH:
        raise ValueError('Provided eboot.bin is still encrypted!')
    elif hash == _EBOOT_ELF_HASH:
        if elf_okay:
            return bytes(0x1000) + eboot
        raise ValueError('eboot.bin with fSELF header must be provided!')
    else:
        raise ValueError('Hash for eboot.bin does not match any supported hashes.')
