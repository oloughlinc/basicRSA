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


def b64_to_bytes(m) -> bytes:
    '''Converts a base64 string message into a bytes representation.
    m is the string to convert.'''

    output = bytearray(b'')
    padding_found = 0

    encoded_value = 0
    for i in range(0, len(m), 4): 
        char_partition = m[i : i + 4] # Split input string 4 characters at a time

        
        if len(char_partition) == 4:

            for char in char_partition:
                
                encoded_value <<= 6 # each character is encoded to 6 bits, so before the next character value is loaded, shift 6 bits

                if char == pad:
                    padding_found += 1
                    continue

                encoded_value += base64_encoding_list.index(char) # add the characters encoding to the register

     # ----------------------------------------------------------------------------------------------------------------------------
    bytes_in_reverse = []
    while encoded_value > 0:
                
        next_byte = encoded_value & 255 # 8 bit mask
        bytes_in_reverse.append(next_byte)
        encoded_value >>= 8
            
    for number_of_times in range(padding_found):
        try:
            del(bytes_in_reverse[0]) # remove end bytes from the array equivalent to the amount of padding
        except IndexError:
            break # allows for cases where there are more padding characters than encoded characters in any partition. This should never actually happen.
                            # if it does though, it won't effect encoded output because that means entire partition is bad and would need to be
                            # deleted anyway.
            
    for byte in reversed(bytes_in_reverse):
                output.append(byte)

    return bytes(output)

