/*
 * Image encryption tool.
 * 
 * Usage: encrypt_image [-e|-d] [-v|-a|-t] input_image output_image
 */

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>

#include "ppm.h"

/* Function prototypes. */
void vigenere(unsigned char *buf, int len);
void affine_enc(unsigned char *buf, int len);
void affine_dec(unsigned char *buf, int len);
void tea_enc(unsigned char *buf, int len);
void tea_dec(unsigned char *buf, int len);

/* Program arguments. */
FILE *input, *output;

/* Main program. */
int main(int argc, char *argv[]) {
	int encrypt = 0;
	pic image;

	/* Check number of arguments. */
	if (argc != 5) {
		fprintf(stderr,
				"\nUsage: encrypt_image [-e|-d] [-v|-a|-t] input_image output_image\n");
		exit(1);
	}
	/* Check mode. */
	if (argv[1][0] != '-' || strlen(argv[1]) != 2) {
		fprintf(stderr,
				"\nUse -e to encrypt and -d to decrypt..\n");
		exit(1);
	}
	encrypt = (argv[1][1] == 'e');
	/* Check algorithm. */
	if (argv[2][0] != '-' || strlen(argv[1]) != 2) {
		fprintf(stderr, "\nUnknown algorithm, use [-v|-a|-t].\n");
		exit(1);
	}
	/* Check files. */
	if ((input = fopen(argv[3], "rb")) == NULL) {
		fprintf(stderr, "\nNão é possível ler arquivo de entrada.\n");
		exit(1);
	}
	if ((output = fopen(argv[4], "wb")) == NULL) {
		fprintf(stderr, "\nNão é possível gravar em arquivo de saída.\n");
		exit(1);
	}

	if (ppm_read(input, &image) == 0) {
		fprintf(stderr, "\nNão é possível ler image de entrada.\n");
		exit(1);
	}

	/* Pass control to chosen algorithm. */
	switch (argv[2][1]) {
		case 'v':
			vigenere(image.pix, image.nx * image.ny * 3);
			break;
		case 'a':
			if (encrypt)
				affine_enc(image.pix, image.nx * image.ny * 3);
			else
				affine_dec(image.pix, image.nx * image.ny * 3);
			break;
		case 't':
                        if (encrypt)
                                tea_enc(image.pix, image.nx * image.ny * 3);
                        else
                                tea_dec(image.pix, image.nx * image.ny * 3);
                        break;
	}

	if (ppm_write(output, &image) == 0) {
		fprintf(stderr, "\nNão é possível gravar image de saída.\n");
		exit(1);
	}

	fclose(input);
	fclose(output);
}

/* Implements the Vigenere cipher. */
void vigenere(unsigned char *buf, int len) {
	int i, length;
	unsigned int byte;
	unsigned char *key;

	printf("Key size: ");
	if (scanf("%d", &length) != 1) {
		fprintf(stderr, "\nInvalid key size.\n");
		exit(1);
	}
	key = (char *)malloc((length + 1) * (sizeof(char)));
	getchar();

	printf("Encryption key: ");
	for (i = 0; i < length; i++) {
		if (scanf("%u", &byte) != 1) {
			fprintf(stderr, "\nError reading encryption key.\n");
			exit(1);
		}
		key[i] = byte % 256;
	}
	key[length] = '\0';

	for (i = 0; i < len; i++) {
		buf[i] = buf[i] ^ key[i % length];
	}
	free(key);
}

void affine_enc(unsigned char *buf, int len) {
}

void affine_dec(unsigned char *buf, int len) {
}

void tea_enc(unsigned char *buf, int len) {
}

void tea_dec(unsigned char *buf, int len) {
}
