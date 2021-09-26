import random
import primecheck
import directBase64

class RSA:

    def __init__(self):

        self.p = 0
        self.q = 0
        self.n = 0 
        self.n_bytes = 0

        self.phi = 0

        self.e = 0  # PUBLIC KEY VALUE
        self.PUBLIC_KEY = (self.n, self.e)

        self.d = 0  # PRIVATE KEY VALUE
        self.PRIVATE_KEY = (self.n, self.d)

        self.c = b''  # CYPHERTEXT STORAGE
        self.m = b''  # DECRYPTED STORAGE

    # -----------------------INTERNAL KEY GENERATION ALGORITHMS -------------------------------------------

    def _generate_N(self, bits=1024):

        if bits % 2 != 0:
            return 0

        self.n_bytes = bits // 8

        #  Generally p and q which are prime factors of N vary by a few bit lengths for security
        #  An arbitrary bit variance of 10 - 15 is chosen.


        bit_variance = random.randrange(10, 16)  
        p_bits = (bits // 2) - bit_variance
        q_bits = (bits // 2) + bit_variance

        print(f'Generating p, q, and N with a length of {bits} bits...')

        #  p and q are two distinct prime numbers. Their product must be a number of length 'bits' but is not guaranteed
        #  given the sizes of p and q alone. iterate and ensure the proper size of N is reached.

        while True:
            self.p, self.q = self._generate_p_q(p_bits, q_bits)
            self.n = self.p * self.q
            if len(bin(self.n)) == bits + 2:
                break

        return self.n

    def _generate_p_q(self, p_bits, q_bits):

        self.p = primecheck.get_prime(p_bits)
        self.q = primecheck.get_prime(q_bits)
        return self.p, self.q

    def _generate_phi(self):

        print("Generating phi...")
        self.phi = (self.p - 1) * (self.q - 1)
        return self.phi

    def _generate_e(self, default=True):

        print("Generating public key e...")
        if default:
            self.e = 65537
        else:
            self.e = primecheck.get_relative_prime(self.phi)     
        return self.e

    def _generate_d(self):

        print("Generating private key d...")
        self.d = primecheck.modular_inverse(self.e, self.phi)
        return self.d

    # -----------------------end internal key generation algorithms -------------------------------------------

    # ------------------------INTERNAL ENCODING ALGORITHMS -----------------------------------------------------

    def _os2ip(self, X) -> int:
        #Reference RFC 8017 PKCS#1 v2.2 (4.2) (Convert a string into an integer representation)
        return int.from_bytes(X, 'big')

    def _i2osp(self, x) -> bytes:
        #Reference RFC 8017 PKCS#1 v2.2 (4.1) (Convert an integer into a representation of its bytes)
        return int.to_bytes(x, self.n_bytes, 'big')

    def _display_byte_string(self, bytestring, display_as='base64') -> str:
        #Converting bytes stored in memory to displayable format
        if display_as == 'base64':
            return directBase64.bytes_to_b64(bytestring)
        if display_as == 'hex':
            return hex(int.from_bytes(bytestring, 'big'))[2:]
        if display_as == 'ascii' or display_as == 'utf':
            return bytes.decode(bytestring, 'utf-8')

    # -------------------------end internal encoding algorithms --------------------------------------------------

    def write_private_key(self):

        with open('private.key', 'w') as private_key_file:

            private_key_file.write(('-' * 10) + 'BEGIN RSA PRIVATE KEY' + ('-' * 10))
            private_key_file.write('\n')

            private_key = self._i2osp(self.n) # converting int to bytes object
            private_key_file.write(self._display_byte_string(private_key))
            private_key_file.write('\n')

            private_key = self._i2osp(self.d)
            private_key_file.write(self._display_byte_string(private_key))
            private_key_file.write('\n')

            private_key_file.write(('-' * 10) + 'END RSA PRIVATE KEY' + ('-' * 10))
            private_key_file.write('\n')

    def write_public_key(self):

        with open('key.pub', 'w') as public_key_file:

            public_key_file.write(('-' * 10) + 'BEGIN RSA PUBLIC KEY' + ('-' * 10))
            public_key_file.write('\n')

            public_key = self._i2osp(self.n) # converting int to bytes object
            public_key_file.write(self._display_byte_string(public_key))
            public_key_file.write('\n')

            public_key = self._i2osp(self.e)
            public_key_file.write(self._display_byte_string(public_key))
            public_key_file.write('\n')

            public_key_file.write(('-' * 10) + 'END RSA PUBLIC KEY' + ('-' * 10))
            public_key_file.write('\n')

    def write_encrypted_message(self):

        with open('encrypted_message.txt', 'w') as output_file:
            
            output_file.write(('-' * 10) + 'BEGIN RSA ENCRYPTED MESSAGE' + ('-' * 10))
            output_file.write('\n')

            output_file.write(self._display_byte_string(self.c))
            output_file.write('\n')

            output_file.write(('-' * 10) + 'END RSA ENCRYPTED MESSAGE' + ('-' * 10))
            output_file.write('\n')

    def load_private_key_From_file(self):

        with open('private.key', 'r') as private_key_file:

            raw_content = private_key_file.readlines()
            empty = []

            if raw_content == empty:

                print('No private key found to load from file. Private keys are stored in private.key and are base64 encoded.')
                return

            # Remove newlines from content
            content = [token.rstrip('\n') for token in raw_content]

            # Check that first line of file is correct
            if content[0] != ('-' * 10) + 'BEGIN RSA PRIVATE KEY' + ('-' * 10): 
                print('Invalid key file format.')
                return
            
            # Check that last line of file is correct
            if content[3] != ('-' * 10) + 'END RSA PRIVATE KEY' + ('-' * 10):
                print('Invalid key file format.')
                return
            
            raw_key_n = content[1]
            raw_key_d = content[2]

            bytes_key_n = directBase64.b64_to_bytes(raw_key_n)
            bytes_key_d = directBase64.b64_to_bytes(raw_key_d)

            self.n = int.from_bytes(bytes_key_n, 'big')
            self.d = int.from_bytes(bytes_key_d, 'big')

        print('Private key file loaded successfully')

    def load_public_key_From_file(self):

        with open('key.pub', 'r') as public_key_file:

            raw_content = public_key_file.readlines()
            empty = []

            if raw_content == empty:

                print('No private key found to load from file. Private keys are stored in private.key and are base64 encoded.')
                return

            # Remove newlines from content
            content = [token.rstrip('\n') for token in raw_content]

            # Check that first line of file is correct
            if content[0] != ('-' * 10) + 'BEGIN RSA PUBLIC KEY' + ('-' * 10): 
                print('Invalid key file format.')
                return
            
            # Check that last line of file is correct
            if content[3] != ('-' * 10) + 'END RSA PUBLIC KEY' + ('-' * 10):
                print('Invalid key file format.')
                return
            
            raw_key_n = content[1]
            raw_key_e = content[2]

            bytes_key_n = directBase64.b64_to_bytes(raw_key_n)
            bytes_key_e = directBase64.b64_to_bytes(raw_key_e)

            self.n = int.from_bytes(bytes_key_n, 'big')
            self.e = int.from_bytes(bytes_key_e, 'big')

            self.n_bytes = 1024 # TODO this is a hack load the byte size of the key n instead
        
        print("Public key file loaded successfully.")

    def load_encrypted_message_from_file(self, filename='encrypted_message.txt'):

        with open(filename, 'r') as encrypted_msg:

            raw_content = encrypted_msg.readlines()

            empty = []
            if raw_content == empty:

                print('No private key found to load from file. Private keys are stored in private.key and are base64 encoded.')
                return

            # Remove newlines from content
            content = [token.rstrip('\n') for token in raw_content]

            # Check that first line of file is correct
            if content[0] != ('-' * 10) + 'BEGIN RSA ENCRYPTED MESSAGE' + ('-' * 10): 
                print('Invalid key file format.')
                return
            
            # Check that last line of file is correct
            if content[2] != ('-' * 10) + 'END RSA ENCRYPTED MESSAGE' + ('-' * 10):
                print('Invalid key file format.')
                return

            raw_cyphertext = content[1]

            self.c = directBase64.b64_to_bytes(raw_cyphertext)

        print('Encrypted message loaded from file successfully')


                
    def new_random_keys(self, bits=1024, default_e=True):
        """Generates new random n (bits = size of N, default is 1024) and new public key (n, e) along with new private key (n, d).
        n must be 1024, 2048, or 4096. Default value for the public key (e = 2^16 + 1) or a random 50 bit value is used. 
        These values are stored in memory within this class."""

        if not (bits == 1024 or bits == 2048 or bits == 4096):
            print('The size of n in bits must be 1024, 2048, or 4096 for this application.')
            return

        self.n = self._generate_N(bits)
        self.phi = self._generate_phi()
        self.e = self._generate_e(default_e)
        self.d = self._generate_d()

        self.PUBLIC_KEY = self.n, self.e
        self.PRIVATE_KEY = self.n, self.d

    def display_all(self):
        """Prints all values stored for the RSA encryption algorithm (N, p, q, phi, e, and d) as hex values"""

        print('\n')
        print(f"The value of N is:\n\n {hex(self.n)}\n\n")
        print(f"The value of p is:\n\n {hex(self.p)}\n\n")
        print(f"The value of q is:\n\n {hex(self.q)}\n\n")
        print(f"The value of phi is:\n\n {hex(self.phi)}\n\n")
        print(f"The value of e is:\n\n {hex(self.e)}\n\n")
        print(f"The value of d is:\n\n {hex(self.d)}\n\n")


    def encrypt(self, M, output_base64=True):
        '''Encrypt a message using the public key currently stored in this module.
        Input M is a string with or without encoded padding. Output is an encrypted string c which is the cyphertext.
        Reference PKCS#1 v2.2 (7.1.1 [3])'''

        if self.n == 0 or self.e == 0:
            print ('There is no public key (n, e) available in memory for encryption.')

        M = M.encode('utf-8')
        message_as_int = self._os2ip(M) # 1: convert message to a numeric representation

        if message_as_int >= self.n:
            print('Message is too large for encryption (encoding produced too many bytes).')

        encrypted_message_as_int = primecheck.a_exp_b_mod_c(message_as_int, self.e, self.n) # 2: Perform encryption
        encrypted_msg = self._i2osp(encrypted_message_as_int) # 3: convert encrypted number to a bytestring

        self.c = encrypted_msg # 4: bytestring stored in local memory
        print('Message successfully encrypted. Temporary copy has been stored in class memory') 

        if output_base64:
            return self._display_byte_string(encrypted_msg)
            
            
    def decrypt(self, c = b'', output_as_string=True) -> str:
        '''Decrypt a message using the private key currently stored in this module.
        If input c is a string, it must be a base64 encoded string. Alternatively, you can pass a bytes object.
        If no input is given, the encrypted message currently stored in memory is used.
        Output is a decrypted string in plaintext'''
        
        if self.n == 0 or self.d == 0:
            print ('There is no private key (n, d) available in memory for decryption.')

        if isinstance(c, str):
            c = directBase64.b64_to_bytes(c)

        #if the c parameter is empty, instead use c stored in memory
        if c == b'':
            c = self.c
        
        encrypted_msg_as_int = self._os2ip(c)

        if encrypted_msg_as_int >= self.n:
            print('Message is too large for decryption (encoding produced too many bytes).')

        decrypted_msg_int = primecheck.a_exp_b_mod_c(encrypted_msg_as_int, self.d, self.n)
        self.m = self._i2osp(decrypted_msg_int)

        if output_as_string:
            return self._display_byte_string(self.m, 'ascii')





    

