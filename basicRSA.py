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

        self.c = b''  # CYPHERTEXT

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
        return int.from_bytes((X.encode('utf-8')), 'big')

    def _i2osp(self, x) -> bytes:
        #Reference RFC 8017 PKCS#1 v2.2 (4.1) (Convert an integer into a representation of its bytes)
        return int.to_bytes(x, self.n_bytes, 'big')

    def _display_byte_string(self, bytestring, display_as='base64') -> str:
        #Converting bytes stored in memory to displayable format
        if display_as == 'base64':
            return directBase64.bytes_to_b64(bytestring)
        if display_as == 'hex':
            return hex(int.from_bytes(bytestring, 'big'))[2:]

    # -------------------------end internal encoding algorithms --------------------------------------------------

                
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
            print ('There is no public key (N, e) available in memory for encryption.')

        message_as_int = self._os2ip(M) # 1: convert message to a numeric representation

        if message_as_int >= self.n:
            print('Message is too large for encryption (encoding produced too many bytes).')

        encrypted_message_as_int = primecheck.a_exp_b_mod_c(message_as_int, self.e, self.n) # 2: Perform encryption
        encrypted_msg = self._i2osp(encrypted_message_as_int) # 3: convert encrypted number to a bytestring

        self.c = encrypted_msg # 4: bytestring stored in local memory
        print('Message successfully encrypted. Temporary copy has been stored in class memory') 

        if output_base64:
            return self._display_byte_string(encrypted_msg)
            
            
    def decrypt(self, encrypted_msg):
        
        return primecheck.a_exp_b_mod_c(encrypted_msg, self.d, self.n)
    

