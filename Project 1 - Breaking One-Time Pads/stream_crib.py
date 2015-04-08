import sys
import re
import argparse
import codecs
import time
import difflib as diff
from collections import Counter

parser = argparse.ArgumentParser(description='')
parser.add_argument('cipher1', help='First encripted message file path.')
parser.add_argument('cipher2', help='Second encripted message file path.')
parser.add_argument('dictionary', help='Dictionary, encoded in ASCII format')
parser.add_argument('-v', '--verbose', action="count", help='Set to True to enable verbose mode.')
args = parser.parse_args()


# ----------------------------------------------------------------
# Auxiliary functions
# ----------------------------------------------------------------

def string_sxor(text1,text2):
    len_text1 = len(text1)
    len_text2 = len(text2)

    if len_text1 > len_text2:
        ctext = text1
        crib = text2
    else:
        ctext = text2
        crib = text1

    results = ""
    single_result = ''
    crib_len = len(crib)
    positions = len(ctext)-crib_len+1

    for index in range(positions):
        single_result = ''
        for a,b in zip(ctext[index:index+crib_len],crib):
            single_result += chr(ord(a) ^ ord(b))
        results += single_result
    return results

def binary_sxor(text1,text2):
    len_text1 = len(text1)
    len_text2 = len(text2)

    if len_text1 > len_text2:
        ctext = text1
        crib = text2
    else:
        ctext = text2
        crib = text1

    results = ""
    single_result = ''
    crib_len = len(crib)
    positions = len(ctext)-crib_len+1

    for index in range(positions):
        single_result = ''
        for a,b in zip(ctext[index:index+crib_len],crib):
            single_result += chr( a ^ b )
        results += single_result
    return results


def testCrib(crib, cipher, cursor):
    result = ""
    for index in range(len(crib)):
        # print('index: ' + str(index))
        result += chr(ord(cipher[index]) ^ ord(crib[index]))
    return result



def hasWordStartingWith(prefix, frequencyDictionary):
    if(prefix == ' \n'):
        return 1
    if (not re.search('^[a-zA-Z., :\']+$',prefix)):
        return 0
    matches = 0
    prefixes = prefix.split()
    count = 0
    for entry in prefixes:
        for word in frequencyDictionary:
            if word[0:len(entry)] == entry:
                count += 1
                matches += 1
                break
        if count == len(frequencyDictionary):
            return 0
    return matches



def WordStartingWith(prefix, frequencyDictionary):
    for word in frequencyDictionary:
        if word[0:len(prefix)] == prefix:
            return True
    return False


# ----------------------------------------------------------
# Main Routine
# ----------------------------------------------------------

def findMessages(plaintext1, plaintext2, cursor, cipher_xor, currentPart, frequencyDictionary, wordDictionary, lastCursor):

    if(args.verbose != None):
        print('\n-----')

        print("1: '" + plaintext1 + "'")
        print("2: '" + plaintext2 + "'")
        print('Cursor: ' + str(cursor))

        print('-----\n')


    textToXor = ''
    theOther = ''
    if cursor == 201:
        if plaintext2[cursor-2:] == '. ':
            textToXor = plaintext2
            theOther =  plaintext1
        else:
            textToXor = plaintext1
            theOther =  plaintext2


    if cursor == 201 and string_sxor(textToXor, cipher_xor[:201]) == theOther: #cursor == 201:
        return (plaintext1 + 'g. ', plaintext2 + '\n')
    else:
        if currentPart == '':
            for word in frequencyDictionary:
                result = testCrib(plaintext1 + word + ' ', cipher_xor, cursor)
                if result != '' and hasWordStartingWith(result[len(plaintext2):], frequencyDictionary):
                    ans = findMessages(plaintext2 + result, plaintext1 + word + ' ', cursor + len(plaintext1 + word + ' '), cipher_xor, result, frequencyDictionary, wordDictionary, cursor)
                    if ans[0] != plaintext1:
                        return ans
        else:
            for word in frequencyDictionary:
                if word[0:len(currentPart)] == currentPart:
                    result = testCrib(plaintext1 + word[len(currentPart):] + ' ', cipher_xor, cursor)
                    matches = hasWordStartingWith(result[len(plaintext2):], frequencyDictionary)

                    if matches > 0:
                        if matches == 1:
                            ans =  findMessages(plaintext2 + result[cursor:], plaintext1 + word[len(currentPart):] + ' ', cursor + len(word[len(currentPart):] + ' '), cipher_xor, result[len(plaintext2):], frequencyDictionary, wordDictionary, cursor)       
                            if ans[1] != plaintext1:
                                return ans
                        elif matches == len(result[len(plaintext2):].split()):
                            ans =  findMessages(plaintext2 + result[cursor:], plaintext1 + word[len(currentPart):] + ' ', cursor + len(word[len(currentPart):] + ' '), cipher_xor, result.split()[len(result.split())-1], frequencyDictionary, wordDictionary, cursor)
                            if ans[1] != plaintext1:
                                return ans

    return(plaintext1[:lastCursor], plaintext2[:lastCursor])
    

# -------------------------------------------------------------------------------
# Initialization of variables and dictionaries
# -------------------------------------------------------------------------------

cipherfile = open(args.cipher1, 'rb+')
ciphertext1 = cipherfile.read()
cipherfile.close()

cipherfile = open(args.cipher2, 'rb+')
ciphertext2 = cipherfile.read()
cipherfile.close()

frequencyDictionary = list()
wordDictionary = Counter()
f = open(args.dictionary, 'r')

for line in f:
    line = line.rstrip('\n')
    frequencyDictionary.append(line)
    wordDictionary[line] = True

f.close()

frequencyDictionary.append(" \n")
wordDictionary[" \n"] = True

plaintext1 = ''
plaintext2 = ''

ctext = binary_sxor(ciphertext1, ciphertext2)[0:202]

# -------------------------------------------------------------------------------
# Main Routine call
# -------------------------------------------------------------------------------

(plaintext1, plaintext2) = findMessages(plaintext1, plaintext2, 0, ctext, '', frequencyDictionary, wordDictionary, 0)



print('\n-----\n')

if(len(plaintext1) == len(ctext) or len(plaintext2) == len(ctext)):

    key = string_sxor(plaintext1, plaintext2)[0:202]

    f1 = open('plaintext1.txt', 'w')
    f2 = open('plaintext2.txt', 'w')
    f3 = open('key.txt', 'w')

    f1.write(plaintext1)
    f2.write(plaintext2)
    f3.write(key)

    f1.close()
    f2.close()
    f3.close()


    print("Text 1: '" + plaintext1 + "'")
    print()
    print("Text 2: '" + plaintext2 + "'")
    print()

    if(args.verbose):

        print('Key size: ' + str(len(key)))
        print("Key: '" + key + "'")
        print()

else:
    print('Your dictionary is incomplete!')
    