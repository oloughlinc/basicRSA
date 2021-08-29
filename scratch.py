'''
bytes = int.to_bytes(42034982103482109482130498120349812309482109481203948201394821039482103948312091243, 128, 'big')
print(bytes)
print(len(bytes))
'''

bytey = b'\x80#\x8b\xed\x1f\xab9Nb\x0e\x1c%\x10#l\xadm'
import directBase64
from base64 import b64encode, b64decode

b64 = b64encode(bytey)
print(b64.decode())

print(directBase64.bytes_to_b64(bytey))

print()

b64_string = 'gCOL7R+rOU5iDhw=lECNsrW1======'
a = b64decode(b64_string)

b = directBase64.b64_to_bytes(b64_string)

print(a)
print(b)



