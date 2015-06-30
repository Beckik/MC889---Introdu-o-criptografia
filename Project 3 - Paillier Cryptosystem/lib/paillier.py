import os
import random

from lib import utils

def generateKeys(prime_lenght=1536):
    """
    Generates Paillier Cryptosystem public and private keys. 
    The input is the bit size of the primes to be used.

    :return tuple: (n,g) the public key
                   (n_lambda, n_mu) the private key
    """
    p = utils.getPrime(prime_lenght)
    q = utils.getPrime(prime_lenght)

    n = p * q
    n_squared = n ** 2
    
    n_lambda = utils.computeLCM(p,q)

    g = utils.getRandomInZ_N2(n)
    n_mu = utils.inverseMod(utils.Lfunction(utils.powMod(g, n_lambda, n_squared), n), n)

    while n_mu == None:
        g = utils.getRandomInZ_N2(n)
        n_mu = utils.inverseMod(utils.Lfunction(utils.powMod(g, n_lambda, n_squared), n), n)

    public_key = PaillierPublicKey(n,g)
    private_key = PaillierPrivateKey(n_lambda, n_mu, p, q, public_key)

    return public_key, private_key  

def generateKeysSimple(prime_lenght=1536):
    """
    Simpler variant of the generateKeys procedure.
    This generator works only for primes p and q of equivalent lenght.

    :return tuple: (PaillierPublicKey, PaillierPrivateKey)
    """
    p = utils.getPrime(prime_lenght)
    q = utils.getPrime(prime_lenght)

    n = p * q
    n_lambda = (p-1) * (q-1)

    g = n + 1

    n_mu = utils.inverseMod(n_lambda, n)

    public_key = PaillierPublicKey(n,g)
    private_key = PaillierPrivateKey(n_lambda, n_mu, p, q, public_key)

    return public_key, private_key  

class PaillierPublicKey:

    def __init__(self, n, g):
        self.n = n
        self.g = g
        self.n_squared = self.n**2

    def encrypt(self, m):
        r = utils.getRandomInZ_N(self.n)

        g_m = utils.powMod(self.g, m, self.n_squared)
        r_n = utils.powMod(r, self.n, self.n_squared)

        cipher = (g_m * r_n) % self.n_squared

        return int(cipher)

class PaillierPrivateKey:

    def __init__(self, Lambda, mu, p, q, public_key):
        self.Lambda = Lambda
        self.mu = mu
        self.p = p
        self.q = q
        self.public_key = public_key
        self.h_p = utils.inverseMod(utils.Lfunction(utils.powMod(self.public_key.g, (self.p - 1), (self.p ** 2)), self.p), self.p)
        self.h_q = utils.inverseMod(utils.Lfunction(utils.powMod(self.public_key.g, (self.q - 1), (self.q ** 2)), self.q), self.q)
        self.n_squared = self.public_key.n**2

    def decrypt(self, c):
        c_lambda = utils.powMod(c, self.Lambda, self.n_squared)
        l = utils.Lfunction(c_lambda, self.public_key.n)

        message = (l * self.mu) % self.public_key.n

        return int(message)

    def decryptCRT(self, c):
        c_lambda1 = utils.powMod(c, self.p - 1, self.p ** 2)
        m_p = (utils.Lfunction(c_lambda1, self.p) * self.h_p) % self.p

        c_lambda2 = utils.powMod(c, self.q - 1, self.q ** 2)
        m_q = (utils.Lfunction(c_lambda2, self.q) * self.h_q) % self.q

        print('m_p: ' + str(m_p))
        print()
        print('m_q' + str(m_q))
        print()

        message = utils.crt([m_p],[m_q]) % (self.public_key.n)

        return int(message)
