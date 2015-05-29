DELTA = 0x9e3779b9
SUMATION = 0xc6ef3720
ROUNDS = 32
IV = (0x086a271a, 0x6eec09ef)

from ctypes import *

##########################################################
# Tiny Encryption Algorithm
# 
# Author: Felipe Santos Oliveira
# State University of Campinas
# 2015
##########################################################

##########################################################
# Encryption/Decryption Functions
##########################################################

def encryptblock(block, keys):
    ''' Encrypts a 64-bit block with a 128-bit key '''
    y, z = block
    sumation = 0
    for _ in range(ROUNDS):
        sumation += DELTA
        sumation = c_uint32(sumation).value
        y += ((z << 4) + keys[0]) ^ (z + sumation) ^ ((z >> 5) + keys[1])
        y = c_uint32(y).value
        z += ((y << 4) + keys[2]) ^ (y + sumation) ^ ((y >> 5) + keys[3])
        z = c_uint32(z).value
    return (y, z)

def decryptblock(block,key):
    ''' Decrypts a 64-bit block with a 128-bit key '''
    y,z = block
    sumation = SUMATION
    delta = DELTA
    for _ in range(ROUNDS):
        z -= ((y << 4) + key[2]) ^ (y + sumation) ^ ((y >> 5) + key[3]);
        z = c_uint32(z).value
        y -= ((z << 4) + key[0]) ^ (z + sumation) ^ ((z >> 5) + key[1]);
        y = c_uint32(y).value
        sumation -= delta
        sumation = c_uint32(sumation).value
    return y,z

##########################################################
# ECB Mode
##########################################################

def encrypt_ECB(data, key):
    ''' 
    ECB mode of operation 
    Makes use of ciphertext stealing to handle incomplete blocks

    @param data: A list of integer lists with 3 elements each
    @param key: A list containing 4 32-bit integers

    @return A list of integer lists with 3 elements each 
    '''
    packed = packbytes(flatten(data))
    cipher = []
    doubleNumBlocks = len(packed)
    isCircular = len(packed) % 2
    if(isCircular == 0):
        for i in range(0, doubleNumBlocks - 4, 2):
            a, b = encryptblock((packed[i], packed[i+1]), key)
            cipher.append(a)
            cipher.append(b)
        a,b     = encryptblock((packed[doubleNumBlocks - 4], packed[doubleNumBlocks - 3]), key)
        (a,b),(c,d) = steal_even((a, b), (packed[doubleNumBlocks - 2], packed[doubleNumBlocks - 1]))
        a,b     = encryptblock((a,b), key)
        cipher.append(a)
        cipher.append(b)
        cipher.append(c)
        cipher.append(d)
    else:
        for i in range(0, doubleNumBlocks - 3, 2):
            a, b = encryptblock((packed[i], packed[i+1]), key)
            cipher.append(a)
            cipher.append(b)
        a,b   = encryptblock((packed[doubleNumBlocks - 3], packed[doubleNumBlocks - 2]), key)
        a,b,c = steal_odd(a,b,packed[doubleNumBlocks - 1])
        a,b   = encryptblock((a,b), key)
        cipher.append(a)
        cipher.append(b)
        cipher.append(c)
    cipher = totuple(unflatten(unpackbytes(cipher)))
    return cipher


def decrypt_ECB(data, key):
    packed = packbytes(flatten(data))
    message = []
    isCircular = len(packed) % 2
    doubleNumBlocks = len(packed)
    if(isCircular == 0):
        for i in range(0, doubleNumBlocks - 4, 2):
            a, b = decryptblock((packed[i], packed[i+1]), key)
            message.append(a)
            message.append(b)
        a,b     = decryptblock((packed[doubleNumBlocks - 4], packed[doubleNumBlocks - 3]), key)
        (a,b),(c,d) = receive_even((a, b), (packed[doubleNumBlocks - 2], packed[doubleNumBlocks - 1]))
        a,b     = decryptblock((a,b), key)
        message.append(a)
        message.append(b)
        message.append(c)
        message.append(d)
    else:
        for i in range(0, len(packed) - 3, 2):
            a, b = decryptblock((packed[i], packed[i+1]), key)
            message.append(a)
            message.append(b)
        a,b   = decryptblock((packed[len(packed) - 3], packed[len(packed) - 2]), key)
        a,b,c = receive_odd(a,b,packed[len(packed) - 1])
        a,b   = decryptblock((a,b), key)
        message.append(a)
        message.append(b)
        message.append(c)
    message = totuple(unflatten(unpackbytes(message)))
    return message

########################################################
# CFB Mode
########################################################

def encrypt_CFB(data, key):
    '''
    CFB mode of operation for TEA
    An attempt to compensate for incomplete blocks was made, but there is a bug that 
    breaks the last pixel in some pictures.

    @param data: A list of integer lists with 3 elements each
    @param key: A list containing 4 32-bit integers

    @return A list of integer lists with 3 elements each 
    '''
    flat = flatten(data)
    packed = packbytes(flat)
    cipher = []
    isCircular = int(len(packed)/2) % 2
    doubleNumBlocks = len(packed)
    if(isCircular == 0):
        a,b = encryptblock(IV, key)
        a = a ^ packed[0]
        b = b ^ packed[1]
        cipher.append(a)
        cipher.append(b)
        for i in range(2, doubleNumBlocks-2, 2):
            a,b = encryptblock((a,b), key)
            a = a ^ packed[i]
            b = b ^ packed[i+1]
            cipher.append(a)
            cipher.append(b)
        if((packed[doubleNumBlocks-1] & 255) == 0):
            a,b = encryptblock((a,b), key)
            a = a ^ packed[doubleNumBlocks-2]
            b = b ^ packed[doubleNumBlocks-1]
            b = b ^ packed[doubleNumBlocks-1]
        else:
            a,b = encryptblock((a,b), key)
            a = a ^ packed[doubleNumBlocks-2]
            b = b ^ packed[doubleNumBlocks-1]
        cipher.append(a)
        cipher.append(b)
    else:
        a,b = encryptblock(IV, key)
        a = a ^ packed[0]
        b = b ^ packed[1]
        cipher.append(a)
        cipher.append(b)
        for i in range(2, doubleNumBlocks - 2, 2):
            a,b = encryptblock((a,b), key)
            a = a ^ packed[i]
            b = b ^ packed[i+1]
            cipher.append(a)
            cipher.append(b)
        a,b = encryptblock((a,b), key)
        while((packed[doubleNumBlocks-1] & 255) == 0):
            packed[doubleNumBlocks-1] = packed[doubleNumBlocks-1] >> 8
        a = a ^ packed[doubleNumBlocks-1]
        cipher.append(a)    
    cipher = totuple(unflatten(unpackbytes(cipher)))
    return cipher

def decrypt_CFB(data, key):
    packed = packbytes(flatten(data))
    cipher = []
    isCircular = int(len(packed)/2) % 2
    doubleNumBlocks = len(packed)
    if(isCircular == 0):
        a,b = encryptblock(IV, key)
        a = a ^ packed[0]
        b = b ^ packed[1]
        cipher.append(a)
        cipher.append(b)
        for i in range(2, doubleNumBlocks - 2, 2):
            a,b = encryptblock((packed[i-2],packed[i-1]), key)
            a = a ^ packed[i]
            b = b ^ packed[i+1]
            cipher.append(a)
            cipher.append(b)
        if((packed[doubleNumBlocks-1] & 255) == 0):
            a,b = encryptblock((packed[doubleNumBlocks-4],packed[doubleNumBlocks-3]), key)
            a = a ^ packed[doubleNumBlocks-2]
            b = b ^ packed[doubleNumBlocks-1]
            b = b & packed[doubleNumBlocks-1]
        else:
            a,b = encryptblock((packed[doubleNumBlocks-4],packed[doubleNumBlocks-3]), key)
            a = a ^ packed[doubleNumBlocks-2]
            b = b ^ packed[doubleNumBlocks-1]
        cipher.append(a)
        cipher.append(b)
    else:
        a,b = encryptblock(IV, key)
        a = a ^ packed[0]
        b = b ^ packed[1]
        cipher.append(a)
        cipher.append(b)
        for i in range(2, doubleNumBlocks - 2, 2):
            a,b = encryptblock((packed[i-2],packed[i-1]), key)
            a = a ^ packed[i]
            b = b ^ packed[i+1]
            cipher.append(a)
            cipher.append(b)
        a,b = encryptblock((packed[doubleNumBlocks-3],packed[doubleNumBlocks-2]), key)
        a = a ^ packed[doubleNumBlocks-1]
        while((a & (255 << 24)) == 0):
            a = a << 8
        cipher.append(a)    
    cipher = totuple(unflatten(unpackbytes(cipher)))
    return cipher

########################################################
# Help functions
########################################################

########################################################
# Ciphertext stealing functions
########################################################

def steal_odd(first32, last32, halfLastBlock):
    bytesToSteal = 0
    last = halfLastBlock
    while ((last & 255) == 0):
        last = last >> 8
        bytesToSteal += 8
    head = first32 >> (bytesToSteal)
    tail = first32 & (255 << 8 * int(bytesToSteal / 8))
    return (halfLastBlock + tail, last32, head)

def steal_even(block1, block2):
    bytesToSteal = 0
    last = block2[1]
    while ((last & 255) == 0):
        last = last >> 8
        bytesToSteal += 8
    if bytesToSteal != 0:
        cnTail = block1[1] >> bytesToSteal
        cnHead = block1[0]
        en1Head = block2[0]
        en1Tail = block2[1] + (block1[1] & (255 << 8 * int(bytesToSteal / 8)))
        return ((en1Head, en1Tail), (cnHead, cnTail))
    else:
        return (block1, block2)

def receive_even(block1, block2):
    bytesToReceive = 0
    last = block2[1]
    while (last & (255 << 24) == 0):
        last = last << 8
        bytesToReceive += 8
    if bytesToReceive != 0:
        cnTail = (block1[1] >> bytesToReceive) << bytesToReceive
        cnHead = block1[0]
        en1Head = block2[0]
        en1Tail = block2[1] + (block1[1] & (255 << 8 * int(bytesToReceive / 8)))
        return ((en1Head, en1Tail), (cnHead, cnTail))
    else:
        return (block1, block2)

def receive_odd(first32, last32, halfLastBlock):
    bytesToReceive = 0;
    last = halfLastBlock
    while (last & (255 << 24) == 0):
        last = last << 8
        bytesToReceive += 8
    tail = first32 >> (bytesToReceive)
    head = first32 & (255 << 8  * int(bytesToReceive / 8))
    return (last + tail, last32, head)

########################################################
# Data manipulation functions
########################################################

def totuple(data):
    output = []
    for element in data:
        output.append(tuple(element))
    return output

def flatten(data):
    output = []
    for element in data:
        for value in element:
            output.append(value)
    return output

def unflatten(data):
    output = []
    block = []
    for element in data:
        block.append(element)
        if(len(block) == 3):
            output.append(block)
            block = []
    return output

def packbytes(data):
    output = []
    numInts = len(data) / 4
    lastInt = len(data) % 4
    for i in range(0, len(data) - lastInt, 4):
        newInt = (data[i] << 24) + (data[i+1] << 16) + (data[i+2] << 8) + data[i+3]
        output.append(newInt)
    if lastInt:
        newInt = 0
        for i in range(0, lastInt):
            newInt += data[len(data) - lastInt + i] << (24 - 8*i)
        output.append(newInt)
    return output

def unpackbytes(data):
    output = []
    numElements = len(data)
    for element in data[:numElements - 1]:
        output.append((element         & (255 << 24)) >> 24)
        output.append(((element <<  8) & (255 << 24)) >> 24)
        output.append(((element << 16) & (255 << 24)) >> 24)
        output.append(((element << 24) & (255 << 24)) >> 24)
    lastbytes = data[numElements - 1]
    count = 1
    while ((lastbytes & 255) == 0):
        lastbytes = lastbytes >> 8
        count += 1
    lastbytes = lastbytes << (count-1) * 8
    for i in range(4-count, -1, -1):
        if (((lastbytes << (8 * i)) & (255 << 24)) >> 24) != 0:
            output.append(((lastbytes << (8 * i)) & (255 << 24)) >> 24)
    return output

########################################################