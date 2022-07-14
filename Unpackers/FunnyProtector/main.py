import ctypes
import argparse

import base64
import binascii

class FunnyProtector:
    '''
    https://github.com/EurosTeam/FunnyProtector

    To unpack the script we first use their dll to
    access the "unXoring" function with the cipher
    parsed from the script. Then all we have to do
    if run it through our decrypt function and then
    viola, we have the source.

    Note: there are other functions such as "StringEncrypt"
          that the dll contains, but god gave man a brain
          so you should be able to figure out how to reverse
          those :)
    '''

    def __init__(self, file, output):
        self.file = file
        self.output = output

        self.dll = ctypes.CDLL('./dlls/_protector.dll') if ctypes.sizeof(ctypes.c_voidp) == 8 else ctypes.CDLL('./dlls/_protector32.dll')
        self.dll.unXoring.restype = ctypes.c_wchar_p

        self.unpack()

    def decrypt(self, code, result=''):
        for char in code:
            result += chr(
                ord(char) - 10
            )

        return base64.b64decode(
            bytes.fromhex(
                result
            )
        )

    def unpack(self):
        with open(self.file) as code:
            code = code.read()

        code = self.decrypt(
            self.dll.unXoring(
                code.partition('returnCipher(\'')[2].partition('\'')[0]
            ).partition('(\'')[2].partition('\'')[0]
        ).decode()
        # Unpacking the script

        if self.output:
            with open(self.output, 'w') as file:
                file.write(code)
                file.close()

        else:
            print(code)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Unpack scripts protected with FunnyProtector'
    )
    parser.add_argument(
        '-o',
        dest='output',
        required=False,
        help='Output file, if null we will directly print the source'
    )
    parser.add_argument(
        '-f',
        dest='file',
        required=True,
        help='Code (*.py) that is packed with FunnyProtector'
    )

    args = parser.parse_args()

    # Parsing arguments passed into argparse

    FunnyProtector(
        file=args.file,
        output=args.output
    )
