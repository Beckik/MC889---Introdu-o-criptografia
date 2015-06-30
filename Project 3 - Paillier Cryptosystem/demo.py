"""
   Usage: demo.py (--generate) [-c]
          demo.py (--encrypt | --decrypt) (<key>) (<file>) [--crt]
          demo.py -h | --help

   Arguments:
      <key>             File containing either the public 
                        or the private key.
      <file>            File to be encrypted/decrypted

   Options:
      -h --help         Displays help
      --generate        Sets key generation mode
      -c --complex      Sets complex key generation mode (default simple mode)
      --encrypt         Sets encryption mode
      --decrypt         Sets decryption mode
      --crt             Sets fast decryption mode (only on decryption)

"""

from lib import paillier
from lib import utils
import json
from docopt import docopt
import binascii
import codecs

def generate(args):
    if args['--complex']: 
        public_key, private_key = paillier.generateKeys()
    else: 
        public_key, private_key = paillier.generateKeysSimple()

    f = open('output/public_key.json', 'w')
    public_content = json.dumps({"n": public_key.n, "g": public_key.g})
    f.write(public_content)
    f.close()

    f = open('output/private_key.json', 'w')
    private_content = json.dumps({"Lambda": private_key.Lambda, "mu": private_key.mu, "p": private_key.p, "q": private_key.q, 'public_key': json.loads(public_content)})
    f.write(private_content)
    f.close()

def encrypt(args):
    f = open(args['<key>'], 'r')
    file_content = f.read()
    f.close()

    content = json.loads(file_content)
    public_key = paillier.PaillierPublicKey(content['n'], content['g'])

    f = open(args['<file>'], 'rb')
    a = binascii.hexlify(f.read())
    #print(str(a))
    file_content = int(a, 16)
    f.close()

    ciphertext = public_key.encrypt(file_content)

    f = open('output/ciphertext.txt', 'w')
    f.write(str(ciphertext))
    f.close()

def decrypt(args):
    f = open(args['<key>'], 'r')
    file_content = f.read()
    f.close()

    content = json.loads(file_content)

    public_key = paillier.PaillierPublicKey(content['public_key']['n'], content['public_key']['n'])
    private_key = paillier.PaillierPrivateKey(content['Lambda'], content['mu'], content['p'], content['q'], public_key)

    f = open(args['<file>'], 'r')
    file_content = int(f.read(), 0)
    f.close()

    if args['--crt']:
        plaintext = private_key.decryptCRT(file_content)
    else:
        plaintext = private_key.decrypt(file_content)



    plaintext = codecs.encode(hex(plaintext)[2:])
    plaintext = binascii.unhexlify(plaintext)

    print(str(plaintext))

    plaintext = codecs.decode(plaintext)

    f = open('output/plaintext.txt', 'w')
    f.write(plaintext)
    f.close()



if __name__ == '__main__':
    args = docopt(__doc__)

    # if args['-h']:
    #     print(args)
    if args['--generate']:
        generate(args)

    elif args['--encrypt']:
        encrypt(args)

    elif args['--decrypt']:
        decrypt(args)



    