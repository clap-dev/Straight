import re
import base64
import argparse

class SimpleObfuscator():
    '''
    https://github.com/wodxgod/Simple-Obfuscator

    Firstly, we have to get all of the obfuscated strings
    which we can just use regex for. Then we convert them
    from hex to string and lastly base64 decode the strings.
    '''

    def __init__(self, code):
        self.code = code

    def unpack(self, output=None):
        code = base64.b64decode(
            bytearray.fromhex(
                ''.join(
                    re.findall(
                        '\+= \"(.*)\"',
                        self.code
                    )
                ).replace('\\x', '')
            ).decode()
        ).decode()

        if output:
            with open(output, 'w') as file:
                file.write(code)
                file.close()

        else:
            print(code)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='PyCompile will detect, unpack and decompile files packed with either Py2Exe or Pyinstaller'
    )
    parser.add_argument(
        '-o',
        dest='output',
        required=False,
        help='Output file, if None we will directly print the source'
    )
    parser.add_argument(
        '-f',
        dest='file',
        required=True,
        help='Code (*.py) that is packed with SimpleObfuscator'
    )

    # Creating argparse instance

    args = parser.parse_args()

    file = args.file
    output = args.output

    # Parsing arguments passed into argparse

    SimpleObfuscator = SimpleObfuscator(
        code=open(file).read()
    )
    SimpleObfuscator.unpack(output)

    # Deobfuscating the script
