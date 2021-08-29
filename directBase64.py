'''Manual module for converting a string directly to a base64 encoded string.
Reference RFC 1421 "PEM for Electronic Mail" sec. 4.3.2.4 

This is created mostly as a programming exercise, the same output can be 
produced in 3 lines of code with built in Python functions:

import base64
b64 = base64.b64encode(message)
out = b64.decode()

'''

base64_encoding_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']

pad = '='

def bytes_to_b64(M) -> str:
    '''Converts bytes directly to a string representation of the bytes input encoded in base64 per PEM methodology.
    M is the bytestring to convert. Output is a string representing the base64 encoding.'''

    output = [] 
    padding = 0

    # ------------- Looking at the input bytestring 3 bytes at a time and partitioning to 3 x 8 = 24 bit pieces ----------------------

    for i in range(0, len(M), 3):
        byte_partition = M[i : i + 3]

        # padding requirements per PEM. If there is less than 3 characters padding will be added at the end of algorithm.
        if len(byte_partition) == 1:
            padding = 2
        elif len(byte_partition) == 2:
            padding = 1

        # creating binary string representations of the  bytes and combining into a 24 bit piece
        piece_24_bit = ''.join([f'{byte:08b}' for byte in byte_partition]) 

    # -------------- splitting 24 bit pieces into 6 bit segments and encoding to base64 --------------------------------------------

        for j in range(0, len(piece_24_bit), 6):

            six_bits = piece_24_bit[j : j + 6]

            if len(six_bits) < 6:  # which can occur in some cases where the input piece was less than 3 characters
                six_bits = six_bits.ljust(6, '0')
            
            index = int(six_bits, 2)
            output.append(base64_encoding_list[index])

        while padding > 0:
            output.append(pad)
            padding -= 1

    return ''.join(output)
