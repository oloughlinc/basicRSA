import basicRSA

rsa = basicRSA.RSA()

rsa.new_random_keys(2048)
rsa.display_all()

message = input('Enter a message to decrypt: ')

rsa.encrypt(message)

print(rsa.c)
print(rsa._display_byte_string(rsa.c))