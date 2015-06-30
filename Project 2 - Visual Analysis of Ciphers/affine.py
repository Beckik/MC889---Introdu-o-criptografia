import fractions

KEYSPACE = 256

def checkKeys(a, b):
    if (fractions.gcd(a,KEYSPACE) != 1):
        return False
    else:
        return True

def encrypt(data, keyA, keyB):
    cipher = []
    for element in data:
        newPixel = []
        for color in element:
            newPixel.append((keyA * color + keyB) % KEYSPACE)
        cipher.append(tuple(newPixel))
    return cipher

def decrypt(data, keyA, keyB):
    message = []
    invA = modinv(keyA,KEYSPACE)
    for element in data:
        newPixel = []
        for color in element:
            newPixel.append((invA * (color - keyB)) % KEYSPACE)
        message.append(tuple(newPixel))
    return message


def egcd(a, b):
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b%a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y

def modinv(a, m):
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m