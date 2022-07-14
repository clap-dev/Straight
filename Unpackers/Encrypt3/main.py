import sys
import argparse

import io
import dis

import zlib
import base64
import marshal

class Encrypt3:
    '''
    https://github.com/caturmahdialfurqon/encrypt-python3

    This one was very straight-forward as they use the
    exact same encoding scheme layered on top of eachother,
    the output file will be a pyc file as it's compiled with
    python beforehand, but you can use Uncompyle6/Decompyle3
    to get the source code.
    '''

    def __init__(self, file, output):
        self.file = file
        self.output = output

        self.unpack()

    def get_bytecode(self, code):
        value = io.StringIO()

        sys.stdout = value

        dis.dis(code)

        sys.stdout = sys.__stdout__
        # Getting the data printed to the console

        return value.getvalue()

    def unpack(self):
        with open(self.file) as code:
            code = code.read()

        exec(
            'string = b\'{string}\''.format(
                string=code.partition('(b\'')[2].partition('\')')[0]
            ),
            locals(),
            globals()
        )
        # Computing the string like this as if we encode it with latin-1, it corrupts the header

        code = dis.Bytecode(
            marshal.loads(
                zlib.decompress(
                    string
                )
            )
        ).dis()
        # Dissasembling the bytecode and returning the value as a string (not perfect so we use dis.dis as well)

        exec(
            'string = b\'{string}\''.format(
                string=code.partition('(b\'')[2].partition('\')')[0]
            ),
            locals(),
            globals()
        )
        # Getting compressed code

        code = self.get_bytecode(marshal.loads(zlib.decompress(string)))
        # Getting the bytecode using dis.dis

        exec(
            'string = b\'{string}\''.format(
                string=code.partition('(b\'')[2].partition('\')')[0]
            ),
            locals(),
            globals()
        )

        exec(
            'string = b\'{string}\''.format(
                string=string.decode('utf-32').partition('(b\'')[2].partition('\',')[0]
            ),
            locals(),
            globals()
        )

        # Getting final base64 string

        code = zlib.decompress(
            base64.b64decode(
                base64.b64decode(
                    base64.b64decode(
                        string.decode('utf-32').partition('(b\'')[2].partition('\',')[0].encode()
                    ).partition(b'(b\'')[2].partition(b'\',')[0]
                ).partition(b'(b\'')[2].partition(b'\',')[0]
            )
        )

        # Sifting through the layers of obfuscation, it's the same thing just multiple times

        for i in range(2):
            code = zlib.decompress(
                base64.b64decode(
                    self.get_bytecode(
                        marshal.loads(
                            code
                        )
                    ).partition('(b\'')[2].partition('\')')[0]
                )
            )

        # If you don't get the source code with 2 loops, try messing around with it

        if self.output:
            with open(self.output, 'wb') as file:
                file.write(code)
                file.close()

        else:
            dis.dis(
                marshal.loads(
                    code
                )
            )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Unpack scripts protected with Encrypt-Python3'
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

    Encrypt3(
        file=args.file,
        output=args.output
    )
