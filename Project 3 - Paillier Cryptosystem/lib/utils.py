import os
import random

try:
    import gmpy2
    GMPY = True
except ImportError:
    GMPY = False

try:
    from Crypto.Util import number
    PYCRYPTO = True
except ImportError:
    PYCRYPTO = False


def powMod(a,b,c):
    """
    Computes a^b mod c
    """
    if GMPY:
        return(gmpy2.powmod(a,b,c))
    else:
        return pow(a,b,c)

def computeGCD(a, b):
    """
    Computes the GCD between a and b
    """
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    result = b
    return result, x, y


def inverseMod(a,b):
    """
    Computes modular multiplicative inverse of a mod b
    """
    if GMPY:
        return int(gmpy2.invert(a,b))
    else:
        gcd, x, y = computeGCD(a, m)
        if gcd != 1:
            None # there is no inverse of a mod b
        else:
            return x % m

def getPrime(N):
    """
    Returns a random N-bit prime number usign either GMP or PyCrypto.
    """
    if GMPY:
        randomFunction = random.SystemRandom()
        rand = gmpy2.mpz(randomFunction.getrandbits(N))
        rand = gmpy2.bit_set(rand, N - 1)
        return int(gmpy2.next_prime(rand))
    elif PYCRYPTO:
        return number.getPrime(N, os.urandom)
    else:
        raise NotImplementedError("Couldn't find GMP or PyCrypto. No futher method implemented. Please install one of these two.")

def computeLCM(a,b):
    a, b = abs(a), abs(b)
    m = a * b
    if not m:
        return 0
    while True:
        a %= b
        if not a:
            return m // a
        b %= a
        if not b:
            return m // b

def getRandomInZ_N2(N):
    """
    Returns an integer in the group Z^*_{n^2}
    """
    n_squared = n**2
    n_length = n_squared.bit_length()
    if PYCRYPTO:
        rand = number.getRandomInteger(n_length, os.urandom)
        while(rand > n_squared):
            rand = number.getRandomInteger(n_length, os.urandom)
        return rand
    else:
        raise NotImplementedError("Couldn't find PyCrypto. No futher method implemented. Please install PyCrypto.")

def getRandomInZ_N(N):
    """
    Returns an integer in the group Z^*_n
    """
    n_length = N.bit_length()
    if PYCRYPTO:
        rand = number.getRandomInteger(n_length, os.urandom)
        while(rand > N):
            rand = number.getRandomInteger(n_length, os.urandom)
        return rand
    else:
        raise NotImplementedError("Couldn't find PyCrypto. No futher method implemented. Please install PyCrypto.")

def Lfunction(u, n):
    return (u - 1) // n

def crt(a, n):
    p = i = prod = 1
    sm = 0

    print(str(len(a)))

    for i in range(len(a)): prod *= n[i]
    for i in range(len(a)): 
        p = prod // n[i]
        sm += a[i] * inverseMod(p, n[i]) * p
    return sm % prod