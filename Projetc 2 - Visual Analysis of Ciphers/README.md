# Affine and TEA Encription Tool

## Installation

To use the tool, you need to have Python 3 installed and the Pillow module for image manipulation. 

To install Pillow, use the following command:

`pip install pillow`

## Usage

To execute the script, run the script as follows:

`python encryption_tool.py [image path] [output path] --cipher [affine/tea/none] [-e] [-d]`

Note that there is a `none` mode, in which the input image will simply be displayed.

If a cipher other than `none` is chosen, you need to use either the flag `-e` for encryption or `-d` for decryption.

## Affine

When using `affine`, you will be asked for a two-part key, `a` and `b`. These are integers, but `a` has the restraint thatit must be coprime with 256, while `b` can be any chosen integer.

## TEA

When using TEA, you will be asked for a 128-bit key, displayed as a four integers key. Each integer must be entered in hexadecimal notation.
After that you will be asked for the mode of operation of TEA, either `ECB` or `CFB`. When done with the inputs, the processing of the images will begin and the result saved in the given path.

