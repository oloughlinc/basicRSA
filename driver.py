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

plaintext = input('Enter a message: ')

out = _parse_encode(plaintext)
out2 = []
for piece in out:
    out2.append(int(piece, 16))

print(out)
print(out2)
# --------------decoding-------------
'''
print(out)
out2 = []
for piece in out:
    out2.append(chr(int(piece, 16)))

print(out2)
'''