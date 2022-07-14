from ctypes import *
import sys,ctypes
if sys.platform == 'win32':
    if ctypes.sizeof(ctypes.c_voidp)==4:
        mydll=ctypes.CDLL('FunnyProtector\\_protector32.dll')
    elif ctypes.sizeof(ctypes.c_voidp)==8:
        mydll=ctypes.CDLL('FunnyProtector\\_protector.dll')
def returnCipher(code,file):
    mydll.unXoring.restype = c_wchar_p
    result = mydll.unXoring(code,file)
    return result
