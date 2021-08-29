base64_encoding_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',
                        'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                        '0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '+', '/']

pad = '='



message = 'VISA ---- BOB P SAGET ---- 4479 4426 4439 9999 ---- EXP: 12.12.2021 ---- CVV: 123'
print(f'{len(message)} chars long')

#---------------------------------base 64 encoding manually (def encode_message)---------------------------------------------------
out_list = []
out_num = 0 #  encoded numerical value of the message. This is the number to be encrypted. 
padding = 0
for i in range(0, len(message), 3):

    partition = message[i : i + 3]

    if len(partition) == 1:
        padding = 2
    elif len(partition) == 2:
        padding = 1

    string = ''
    for character in partition: # can list comprehension: ''.join([f'{(ord(character)):08b}' for character in partition])

        num = ord(character) # ascii encoding each character
        string += f'{num:08b}'


    for j in range(0, len(string), 6):

        six_bits = string[j : j + 6]

        if len(six_bits) < 6:
            six_bits = six_bits.ljust(6, '0')

        num = int(six_bits, 2)
        out_list.append(base64_encoding_list[num])

        out_num <<= 6 #  running count of the numerical value of the encoding (for encryption)
        out_num |= num # this would be one large number who's binary representation is equivalent to the base64 encoding
        #for academic purposes: you can do something similar to the whole string at once if you pack it as a struct of bytes

    while padding > 0:
        out_list.append(pad)
        padding -= 1
        out_num <<= 6 # NEW CODE!!!!

print(''.join(out_list))
print(out_num)
#---------------------------------------------------------------------------------------------------------------

# for academics note that four lines accomplish the same thing:
import base64
enc = message.encode('ascii')
b64 = base64.b64encode(enc)
out = b64.decode('ascii')
print(out)


# ------------------------------------decode an ascii.. (base64) encoded number to an ascii string-----------------------------
print('\ndecoding a string from this number...\n')
number = out_num
output = []
while number > 0:

    new_num = number & 255 #  8 bit mask
    output.append(chr(new_num)) # note that ascii 8 bit zero = NULL
    number >>= 8

output.reverse()
print(''.join(output)) # i like this, but it involves equating padding to zero which isnt really right
                        #TODO another thing we can do is take it 6 bits at a time and decode a number to base64 instead. then decode to ascii. 
#-----------------------------------------------------------------------------------------------------------------------------

#------------------------------------turn base64 ascii encoded text into a base64 numerical representation---------------------------
#                                      (this would be used for decryption)

base64message = ''.join(out_list)
output = []
for char in base64message: 

    if char == pad:
        output.append('0' * 6)

    else:

        base64value = base64_encoding_list.index(char)
        output.append(f'{base64value:06b}')

string_o_bits = ''.join(output)
final_num = int(string_o_bits, 2)
print(final_num) # yee ha

# note there is essentially no difference in the bit structure between ascci encoding and base64 encoding. The difference is in how the bits are
# displayed as output...and padding

#THIS MEANS THAT ALL CONVERSIONS AND MATH CAN BE DONE IN ASCII AND THEN THE ENCRYPTED RESULTS ARE CONVERTED TO ASCII AND
# DISPLAYED BASE64. DECRYPTING WILL FIRST CONVERT BASE64 TO ASCII NUMBER

# and thats all for today i think

import basicRSA

rsa = basicRSA.RSA()
rsa.n_bytes = 1024 // 8

nummy = rsa._os2ip('VISA ---- BOB P SAGET ---- 4479 4426 4439 9999 ---- EXP: 12.12.2021 ---- CVV: 123')
print()
print(nummy)

stringy = rsa._i2osp(nummy)

print(stringy) 

rsa.new_random_keys()
stringy = 'VISA ---- BOB P SAGET ---- 4479 4426 4439 9999 ---- EXP: 12.12.2021 ---- CVV: 123'
print('encrypted stringy:')
encrypted_stringy = rsa.encrypt(stringy)
print(encrypted_stringy)


number = int.from_bytes(encrypted_stringy, 'big')
print(number)

decrypt = basicRSA.primecheck.a_exp_b_mod_c(number, rsa.d, rsa.N)
print(decrypt)

decrypted_bytes = int.to_bytes(decrypt, 1024, 'big')
decrypted = decrypted_bytes.decode('utf-8')
print(decrypted)

hi = 'Þ↑bL*xMJAÛSÙs♫N>§ð¯q→☼­◄Ü¢G¬♀S°á8ê¶å1N­'