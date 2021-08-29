# basicRSA

A straighforward implementation of RSA cryptography built in Python.
The purpose of this build is a programming exercise. Although some consideration was given to best encryption practice where applicable, the focus was to 
implement something that first and foremost works and that was built by myself. Most functions were built from 'scratch' even though in most cases
either standard libraries exist or open libraries can be imported.

The RSA class handles public and private key generation in 1024, 2048, or 4096 bit integer n modulus. Its handles encoding and encryption of a given string in
one function .encrypt(M) and decryption using .decrypt(). Output can keys can be written to a file.

<b>Some design choices:</b>

-Prime generation using Python 'secrets' library which is a cryptographically sound random number generator.

-Large prime numbers are verified using an implementation of Fermat's Little Theorem, which ensures 'probable primes'. 
Although more comprehensive methods exist for verifying prime numbers, I chose this method based on its simplicity vs effectiveness for this application.

-Private key d value, which is the modular inverse of public key value e, is calculated using an iterative implementation of the Extended Euclidean Algorithm.

-Modular exponentiation involving very large numbers, which is the backbone of RSA encryption scheme, is written as an iterative function 
[Although Python pow(a, b, c) performs the same task].

-Output is stored in memory as a bytes object.

-Output can be displayed in base64 representation. I have chosen per the idea of this project to implement the base64 encoding/decoding manually.

<b>Some things that are left out:</b>

-Padding of the input message. Typically an input message is padded to add randomness to an input, so if the same input is sent twice the encryption
will appear different.

-Digital signature. Typically an outgoing message is signed using the senders private key to verify message origination.

-AES encryption. AES encryption is used on the actual message in most real use cases, and only the AES key is encrypted using RSA. This is because
RSA encryption can only work on messages smaller than the size of n in bits which amounts to only a few hundered bytes at most.

-Probably many others that keep this from being an actually secure solution.
