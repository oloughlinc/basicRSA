import basicRSA

# Create Basic RSA object
rsa = basicRSA.RSA()

# Initialize RSA with random keys
rsa.new_random_keys()

# Write keys to file
rsa.write_private_key()
rsa.write_public_key()

# Encrypt a message
message = input("Enter message to encrypt: ")
rsa.encrypt(message)
rsa.write_encrypted_message()

# Clear RSA memory
rsa = basicRSA.RSA()

# Load keys and message from the last session
rsa.load_public_key_From_file()
rsa.load_private_key_From_file()
rsa.load_encrypted_message_from_file()

# Decrypt a message
message = rsa.decrypt()
print(f'The message decrypted again is: {message}')




