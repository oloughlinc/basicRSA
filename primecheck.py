import random
import secrets
import math


def _valid_input(min_value, *argv):

    for i in argv:
        try:
            if i < min_value:
                return False 
        except TypeError:        
            return False
    return True

def isPrime_Fermat(num, k=20):

    '''Checks a given input for primality via Fermat's Little Theorem.
        Returns True if the number is a probable prime.
        Returns False if the number is composite

        k is the number of times to perform the check. Higher numbers reduce the chance
        of a false positive, lower numbers are faster.
    '''
    #TODO: check that num is an int
    
    # Check basic cases first
    if (num < 1) or (num % 2 == 0):
        return False

    # begin Fermat primality algorithm
    for i in range(k):

        a = random.randrange(1, num)
        if a_exp_b_mod_c(a, num - 1, num) == 1:
            continue
        else:
            return False

    #if the condition succeeds k times, return true.    
    else:
        return True

def a_exp_b_mod_c(a, b, c):

    '''Using properties of modular arithmetic, breaks a**b % c down
    into smaller components and solves without having to directly compute a**b which
    may result in overflow for large numbers. Mirrors built-in pow(a, b, c)'''
    
    # check for valid inputs
    if not _valid_input(1, a, b, c):
        return 0
        #TODO error printing??

    result = 1
    while b > 0:

        if b % 2 == 0:
            # If the exponent is even, a^b mod c = a*a mod c ^(b/2) mod c
            a = (a * a) % c
            b = b // 2

        else:
            # if the exponent is odd, a^b mod c = a * a^b-1 mod c
            result = (result * a) % c
            b -= 1
    
    return result

def get_prime(bits):
    """Generate a prime number of binary bit length 'bits'. Result is a
    probable prime number as verified by a Fermat primality test."""

    if bits < 2:
        return None

    min_bits = 1 << bits - 1
    candidate_prime = secrets.randbits(bits - 1) + min_bits

    while isPrime_Fermat(candidate_prime) == False:
        candidate_prime = secrets.randbits(bits - 1) + min_bits

    return candidate_prime

def get_relative_prime(N, max_bits=50):
    """Generate a new random number relatively prime to integer N. Define a maximum size in bits using max_bits"""

    candidate_prime = secrets.randbits(max_bits)
    while math.gcd(candidate_prime, N) != 1:
        candidate_prime = secrets.randbits(max_bits)
    return candidate_prime


def get_euclidean_sequence(a, b):
    """Returns the Euclidean Algorithm sequence in a list for two given integers a and b"""

    if a < 0 or b < 0:
        return 0

    euclidean_seq = []

    while b > 0:
        euclidean_seq.append(a // b)
        modb = a % b
        a = b
        b = modb

    return euclidean_seq

def modular_inverse(a, b):
    """Iterative function to calculate the inverse of integer a mod integer b"""

    if a < 0 or b < 0:
        return 0
        
    # receive the euclidean sequence and remove the last value as it is not needed for this algorithm.
    euclidean_seq = get_euclidean_sequence(b, a)
    euclidean_seq.pop()

    # Initialize p values of the algorithm
    p1 = 0
    p2 = 1

    for q in euclidean_seq:

        this_p = (p1 - (p2 * q)) % b

        # shift p values of the algorithm over one spot, updating p2 with the newest value
        p1 = p2
        p2 = this_p
    
    return p2

def int_to_hex(n):

    hex = {10: 'a', 11: 'b', 12: 'c', 13: 'd', 14: 'e', 15: 'f'}

    output = []
    while n > 0:

        modn = n % 16 # 16 base can be 0-16 var b
        if modn in hex:
            modn = hex[modn]
        output.append(str(modn))
        n = n // 16

    output.reverse()
    return ''.join(output)



if __name__ == '__main__':
    
    input('start')
    print(a_exp_b_mod_c(5, 11, 23567))
    


