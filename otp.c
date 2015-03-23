/*
 * One-Time Pad (OTP) encryption.
 * 
 * Uso: otp input output
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

/* Function prototypes. */
void otp();

/* Program arguments. */
FILE *input, *output, *key;

/* Main program. */
int main(int argc, char *argv[]) {
	/* Checking number of arguments */
	if (argc != 4) {
		fprintf(stderr, "\nUssage: opt input output key_file.\n");
		exit(1);
	}

	/* Checking files. */
	if ((input = fopen(argv[1], "rb")) == NULL) {
		fprintf(stderr, "\nInput file cannot be read.\n");
		exit(1);
	}
	if ((output = fopen(argv[2], "wb")) == NULL) {
		fprintf(stderr, "\nOutput file cannot be written.\n");
		exit(1);
	}
	if ((key = fopen(argv[3], "rb")) == NULL) {
		fprintf(stderr, "\nKey file cannot be read.\n");
		exit(1);
	}

	otp();

	fclose(input);
	fclose(output);
}

void otp() {
	int c, k;

	while ((c = fgetc(input)) != EOF) {
		if ((k = fgetc(key)) != EOF) {
			printf("%c", c ^k);
			fputc(c ^ k, output);
		} else {
			fprintf(stderr, "\nInsufficient key material.\n");
			exit(1);
		}

	}
}