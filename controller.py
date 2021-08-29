import basicRSA

rsa = basicRSA.RSA()

rsa.new_random_keys(1024)

message = input('Enter a message to encrypt: ')

rsa.encrypt(message)
encrypted = rsa._display_byte_string(rsa.c)
print(encrypted)

input('Press enter to decrypt')

decrypted = rsa.decrypt(encrypted)
print(decrypted)