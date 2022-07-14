import re
import argparse

class PyProtector:
    '''
    https://github.com/0xblobfish/PyProtector

    This one was a little bit trickier in the sense
    of programming the logic for the string reconstructor.
    In the end, I ended up going with RegEx instead of
    using tokenize or ast, as it's easier and gets the
    job done good enough.
    '''

    def __init__(self, file, output):
        self.file = file
        self.output = output

        self._chr = re.compile(r'[(](\d+)[)]')
        self._unichr = re.compile('unichr\((\d{0,3})\)')

        self.unpack()

    def string_reconstructor(self, code):
        for line in code.split('\n'):
            strings = self._chr.findall(line)

            if strings:
                string = '+'.join([f'unichr({_})' for _ in strings])
                decoded = ''.join([chr(int(_)) for _ in strings])

                code = code.replace(string, f'\'{decoded}\'')

        return code

    def unpack(self):
        with open(self.file) as code:
            code = code.read()

        code = self.string_reconstructor(
            ''.join(
                [
                    chr(
                        int(
                            char
                        )
                    )
                    for char in self._unichr.findall(code)
                ]
            ).split('#')[0].replace('True,False=False,True', '')
        )

        # Parsing ascii codes, converting them back into ascii, and then removing junk
        # Then running it through a very basic string reconstruction, doesn't work for
        # every case but gets most of them

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

    PyProtector(
        file=args.file,
        output=args.output
    )
