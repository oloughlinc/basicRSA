import primecheck

class RSA:

    def __init__(self):

        self.p = None
        self.q = None
        self.N = None 

        self.phi = None

        self.e = None  # PUBLIC KEY VALUE
        self.PUBLIC_KEY = self.e

        self.d = None  # PRIVATE KEY VALUE
        self.PRIVATE_KEY = self.d

    def gen_p_q(self):

        print("Generating p...")
        self.p = primecheck.gen_prime(1024)
        print("Generating q...")
        self.q = primecheck.gen_prime(1024)
        return self.p, self.q

    def gen_phi(self):

        self.phi = (self.p - 1) * (self.q - 1)
        return self.phi
    
rsa = RSA()
input('Enter to start')
p, q = rsa.gen_p_q()
print(f'p is: {bin(p)}')
print(f'q is: {bin(q)}') 
n = p * q
print(f'N is: {bin(n)}')
