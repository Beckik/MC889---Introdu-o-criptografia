from lib import paillier
from lib import utils

def main():
	public, private = paillier.generateKeysSimple()

	a = input("Enter the first integer: ")

	cipher_a = public.encrypt(int(a, 0))

	print("ciphertext 'a': " + str(cipher_a))
	print()

	b = input("Enter the second integer: ")

	cipher_b = public.encrypt(int(b, 0))

	print("ciphertext 'b': " + str(cipher_b))
	print()

	summation = private.decrypt(cipher_a * cipher_b)

	print("ciphertext 'a' * 'b' = " + str(cipher_a * cipher_b))
	print()

	print("The summation of 'a' and  'b' can be obtained by the decryptation of enc(a)*enc(b): " + str(summation))

if __name__ == '__main__':
	main()