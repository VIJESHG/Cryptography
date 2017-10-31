import random
#Euclid's algorithm for GCD
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a

#Euclid's extended algorithm for finding the multiplicative inverse
def multiplicative_inverse(e, phi):
    d = 0
    x1 = 0
    x2 = 1
    y1 = 1
    temp_phi = phi
    
    while e > 0:
        temp1 = temp_phi/e
        temp2 = temp_phi - temp1 * e
        temp_phi = e
        e = temp2
        
        x = x2- temp1* x1
        y = d - temp1 * y1
        
        x2 = x1
        x1 = x
        d = y1
        y1 = y
    
    if temp_phi == 1:
        return d + phi

#Prime Test.
def is_prime(num):
    if num == 2:
        return True
    if num < 2 or num % 2 == 0:
        return False
    for n in xrange(3, int(num**0.5)+2, 2):
        if num % n == 0:
            return False
    return True

def generate_keypair(p, q):
    if not (is_prime(p) and is_prime(q)):
        raise ValueError('Both numbers must be prime.')
    elif p == q:
        raise ValueError('p and q cannot be equal')
  
    n = p * q		

    #Phi is the totient of n
    phi = (p-1) * (q-1)

    #Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)
    
    #Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    #Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    
    #Return public and private keypair
    return ((e, n), (d, n))

def encrypt(pk, plaintext):
    key, n = pk
    cipher = (plaintext ** key) % n
    return cipher

def decrypt(pk, ciphertext):
    key, n = pk
    plain = (ciphertext ** key) % n
    return plain
    

if __name__ == '__main__':
    print "RSA Encrypter/ Decrypter"
    p = input("Enter a prime number: ")
    q = input("Enter another prime number (Not one you entered above): ")
    print "\nGenerating your public/private keypairs now . . ."
    public, private = generate_keypair(p, q)
    print "Your public key is (e,n): ", public 
    print "Your private key is (d,n): ", private
    message = input("\nEnter a message to encrypt with your private key: ")
    print "\nEncrypting message with public key ", public ," . . ."
    encrypted_msg = encrypt(public, message)
    print "Your encrypted message is: ",encrypted_msg
    print "\nDecrypting message with private key ", private ," . . ."
    print "Your message is:",decrypt(private, encrypted_msg)
