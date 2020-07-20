from random import choice, randint
import math

def main():
    
    keys = generateKeys(150)                                                                   # 150 *2 on site
    n1 = int('8721BA49F6FD8C4614EB792FA7A0B393306944A857B1DC2032B93E810E9E711FDE1A9378A87',16) # modulus site
    e1 = int('10001', 16)                                                                      # public exponent site
    k1, s1 = sendKey(randomNumberGenerator(250), e1, n1, keys[2], keys[1])
    print('Receive key: ')    # on site
    print('Key:             ' + str(hex(k1))[2:])   # hex - 16 b
    print('Signature:       ' + str(hex(s1))[2:])
    print('Modulus:         ' + str(hex(keys[1]))[2:])
    print('Public exponent: ' + str(hex(keys[0]))[2:])

def randomNumberGenerator(len):
    number = str()
    for i in range(len-2):
        number += str(choice([0, 1]))
    number = ''.join(('1', number, '1'))
    return int(number,2)

def randomPrimeNumber(len):
    num = randomNumberGenerator(len)
    while not testMillerRabin(num):
        num+=2
    return num

def oilerFunction(p, q):
    return (p-1)*(q-1)

def generateKeys(len):  # RSA
    p = randomPrimeNumber(len)
    q = randomPrimeNumber(len)
    n = p*q
    oiler = oilerFunction(p, q)
    e = randint(2, oiler-1)
    while  advancedEuclideanAlgorithm(e,oiler)[0] != 1:
        e = randint(2, oiler-1)
    d = advancedEuclideanAlgorithm(e,oiler)[1]%oiler
    return(e, n, d)                                       ### (e, n) -откр (d, n) - закр   n-модуль из p q

def encrypt(message, e, n):
    c = pow(message, e, n)
    return c

def decrypt(c, d ,n ):
    m = pow(c, d, n)
    return m

def sign(m, d, n):    #подпись
    s = pow(m, d, n)
    return s

def verify(s, e, n):    # проверка подписи
    m = pow(s, e, n)
    return m

def sendKey(k, e1, n1, d, n):                                       ### 
    return (encrypt(k, e1, n1), encrypt(sign(k, d, n), e1, n1))

def ReceiveKey(k1, s1, d1, n1, e, n):                               ### 
    if verify(decrypt(s1, d1, n1), e, n) == decrypt(k1, d1, n1):
        return k
    else:
        return ''

def testMillerRabin(p):    # k = 20
    temp_p = p-1           
    s=0
    while temp_p%2 == 0:
        temp_p //= 2
        s += 1
    d = temp_p
    x = 0
    for i in range(20):
        x = randint(2, p-1)
        if advancedEuclideanAlgorithm(x, p)[0] == 1:
            if pow(x, d, p) == 1 or pow(x, d, p) == (-1)%p:
                continue
            else:
                for r in range (1, s):
                    xr = pow(x, d*pow(2,r), p)
                    if xr == (-1)%p:
                        return True
                    elif xr == 1:
                        return False
                    else:
                        continue
                return False
        elif advancedEuclideanAlgorithm(x, p)[0] > 1:
            return False
    return True

def advancedEuclideanAlgorithm(num1, num2):   # u*num1 + v*num2 = gcd(num1, num2)
    if(num2==0):
        return (num1, 1, 0)
    else:
        (greatestCommonDivisior, u, v) = advancedEuclideanAlgorithm(num2, num1 % num2)
        return (greatestCommonDivisior, v, u - num1//num2*v)   # gcd, u - reverced, v

main()

