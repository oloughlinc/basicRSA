import basicRSA
rsa2 = basicRSA.RSA()

#get an input
plaintext = input('Enter a message: ')

#convert this message to a ascii hex string

encoded = plaintext.encode('ascii')

out = []
for byte in encoded:
    out.append(hex(byte)[2:])

hex_string = ''.join(out)
print(hex_string)

# convert hex string to a number

integer = int(hex_string, 16)
print(integer)

#encode the number to the secret number:
encrypted = basicRSA.rsa.encrypt(integer)
print(f'encryped message is: {hex(encrypted)}')

input('Enter to continue')

#decode the number back again:

decrypted = basicRSA.rsa.decrypt(encrypted)
print(decrypted)

# convert the number to a hex string
back_to_hex = basicRSA.primecheck.int_to_hex(decrypted)
print(back_to_hex)


input('Enter')
input('Enter')
print('hi')
