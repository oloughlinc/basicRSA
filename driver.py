def _parse_encode(text):

    #  set partition to number of 8 bit ascii characters that can fit inside the size of N bits

    # partition = 1024 // 8
    partition = 128
    print(len(text))
    print(len(bin(2**24)))
    output = []
    for i in range(0, len(text), partition):
        partitioned_txt = text[i : i + partition]
        output_segment = []
        for char in partitioned_txt:
            encoded_char = ord(char)
            encoded_char = str(hex(encoded_char)[2:])
            output_segment.append(encoded_char)
        output.append(''.join(output_segment))

    return output

# --------------decoding-------------
'''
print(out)
out2 = []
for piece in out:
    out2.append(chr(int(piece, 16)))

print(out2)
'''

import basicRSA
import base64

rsa = basicRSA.RSA()

message = "in the time of chimpanzees I was a monkey. butane: in my vaines''' like my name was sarach connor population was none in the desertous sun"

bytee = rsa._encode_to_bytes(message)
asciid = str(message).encode('ascii')
print(bytee)
for byte in bytee:
    print(byte)

parts = []
for i in range(0, len(bytee) - 2, 4):
    parts.append(bytee[i : i + 4])

print(parts)
what = [(8 % (len(bin(y))-2)) *'0' + str(bin(y))[2:] for x in parts for y in x]
print(what)
e_val = eval('0b' + ''.join(what))
print(e_val)
#all that for a drop of blood......(can do in one line)
encoded_bytee = int.from_bytes(bytee, 'big')
encoded = int.from_bytes(asciid, 'big')
print(encoded)
decoded = int.to_bytes(encoded, 128, 'big')
print(decoded)
#this is fun but need to equate the letters to their 6 bit counterparts in base64 instead of their ascii so ... probably need a dictionary of some sort..
#note that the encoded ascii is the same number of bits and should be the same overall value as the encoded base64 message. so why use base64?? besides as display..
rsa.new_random_keys()
encrypted_bytee = rsa.encrypt(encoded_bytee)
decrypted_bytee = rsa.decrypt(encrypted_bytee)
print(base64.b64decode(int.to_bytes(decrypted_bytee, 1024, 'big')))
print((int.to_bytes(decrypted_bytee, 1024, 'big')))
print(encrypted_bytee)