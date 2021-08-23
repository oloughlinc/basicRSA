import random
import primecheck

class RSA:

    def __init__(self):

        self.p = 0
        self.q = 0
        self.N = 0 

        self.phi = 0

        self.e = 0  # PUBLIC KEY VALUE
        self.PUBLIC_KEY = (self.e, self.N)

        self.d = 0  # PRIVATE KEY VALUE
        self.PRIVATE_KEY = (self.d, self.N)

    # -----------------------INTERNAL KEY GENERATION ALGORITHMS -------------------------------------------

    def _generate_N(self, bits=1024):

        if bits % 2 != 0:
            return 0

        #  Generally p and q which are prime factors of N vary by a few bit lengths for security
        #  An arbitrary bit variance of 10 - 15 is chosen.


        bit_variance = random.randrange(10, 16)
        
        p_bits = (bits // 2) - bit_variance
        print('p bits' + str(p_bits))
        q_bits = (bits // 2) + bit_variance
        print('q bits' + str(q_bits))

        print(f'Generating p, q, and N with a length of {bits} bits...')

        #  p and q are two distinct prime numbers. Their product must be a number of length 'bits' but is not guaranteed
        #  given the sizes of p and q alone. iterate and ensure the proper size of N is reached.

        while True:
            self.p, self.q = self._generate_p_q(p_bits, q_bits)
            self.N = self.p * self.q
            if len(bin(self.N)) == bits + 2:
                break

        return self.N

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

        print("Generating secret key d...")
        self.d = primecheck.modular_inverse(self.e, self.phi)
        return self.d

    # -----------------------/end internal key generation algorithms -------------------------------------------

    # ------------------------INTERNAL ENCODING ALGORITHMS -----------------------------------------------------

    def _parse_encode(self, text):
        #TODO not working see result in driver.py
        #  set partition to number of 8 bit ascii characters that can fit inside the size of N bits
        partition = ((len(bin(self.N))) - 2) // 8

        output = []
        for i in range(0, len(text), partition):
            partitioned_txt = text[partition : i + partition]
            output_segment = []
            for char in partitioned_txt:
                encoded_char = str(hex(char)[2:])
                output_segment.append(encoded_char)
            output.append(''.join(output_segment))

        return output
                


    def new_random_keys(self, bits=1024, default_e=True):
        """Generates new random N (bits = size of N, default is 1024) and new public key (e, N) along with new private key (d, N).
        N must be an even number and is typically 2^x. Default value for the public key (e = 2^16 + 1) or a random 50 bit value is used. 
        These values are stored in memory within this class."""

        if bits % 2 != 0:
            print('The size of N must be an even number for this implementation. Typically a value 2^x is used.')
            return

        self.N = self._generate_N(bits)
        self.phi = self._generate_phi()
        self.e = self._generate_e(default_e)
        self.d = self._generate_d()

        self.PUBLIC_KEY = self.e, self.N
        self.PRIVATE_KEY = self.d, self.N

    def display_all(self):
        """Prints all values stored for the RSA encryption algorithm (N, p, q, phi, e, and d) as hex values"""

        print('\n')
        print(f"The value of N is:\n\n {hex(self.N)}\n\n")
        print(f"The value of p is:\n\n {hex(self.p)}\n\n")
        print(f"The value of q is:\n\n {hex(self.q)}\n\n")
        print(f"The value of phi is:\n\n {hex(self.phi)}\n\n")
        print(f"The value of e is:\n\n {hex(self.e)}\n\n")
        print(f"The value of d is:\n\n {hex(self.d)}\n\n")


    def encrypt(self, encoded_msg):

        return primecheck.a_exp_b_mod_c(encoded_msg, self.e, self.N)

    def decrypt(self, encrypted_msg):

        return primecheck.a_exp_b_mod_c(encrypted_msg, self.d, self.N)
    

