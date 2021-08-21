import random
import secrets
import math

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
    may result in overflow for large numbers.'''
    
    # check for valid inputs
    try:
        if a < 1 or b < 0 or c < 1:
            return 0    
    except:
        print('Error')
        return 0
        #TODO handle if not int inputs..

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

def gen_prime(bits):
    """Generate a prime number of binary bit length 'bits'. Result is a
    probable prime number as verified by a Fermat primality test."""

    if bits < 2:
        return None

    min_bits = 1 << bits - 1
    candidate_prime = secrets.randbits(bits - 1) + min_bits

    while isPrime_Fermat(candidate_prime) == False:
        candidate_prime = secrets.randbits(bits - 1) + min_bits

    return candidate_prime


if __name__ == '__main__':
    '''
    x = int(input('num: '))
    y = int(input('num: '))
    z = int(input('num: '))
    print(a_exp_b_mod_c(x,y,z,))
    '''
    a = 1
    while input != 0:
        a = int(input('# of bits: '))
        b = gen_prime(a)
        print('prime is ' + str(b))
        i = -2
        for bit in bin(b):
            i += 1
        print(i)


