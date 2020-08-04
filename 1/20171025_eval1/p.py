from hashlib import sha256
import random
import sympy

print("Input n - your choice for length of prime")
n=int(input())
# sympy.randprime(a,b) gives us a random prime between and b 
# So to get a random prime of length n, we use a as (10 power n-1) and (b as 10 power n )-1
x = sympy.randprime(pow(10, n-1), pow(10, n)-1)
print("The random prime is" ,x)

#this is using the inbuilt library for SHA hash function
def SHAHash(r, M):
    hash=sha256()
    hash.update(str(r).encode())
    hash.update(M.encode())
    return int(hash.hexdigest(),16)

#this is using my own hash function as described in the solution to Q.
def dlpHash(r,M, g, y, q):
    mm =''.join(format(i, 'b') for i in bytearray(M, encoding ='utf-8'))  #this gives us the binary representation of the message string
    print("Binary representation of message is: ", mm)
    m_dec = int(mm, 2) #Converting that binary to decimal
    print("Decimal representation of binary encoded message is: ", m_dec)
    print("\n")
    return ((pow(g, r)%q)*(pow(y, m_dec%q)%q))%q




# generator g
g = 2

# Prime q 
q = 2695139

## Key generation
#Private signing key is x as computed before
# calculate public verification key y
y = pow(g, x, q)

## Signing
M = "abcd"
k = random.randint(1, q - 1)
r = pow(g, k, q)
print("For Alice while signing")
e = SHAHash(r, M) % q # part 1 of signature
e2 = dlpHash(r,M, g, y, q)
s = (k - (x * e)) % (q-1) # part 2 of signature

## Verification

rv = (pow(g, s, q) * pow (y, e, q)) % q
print("For Bob while verifying")
ev = SHAHash(rv, M) % q
ev2 = dlpHash(rv, M, g,y,q)
print("Using SHA inbuilt hash function")
print("e is: ", e)
print("ev is: ", ev)
print("\n")
print("Using my own hash function")
print("e is: ", e2)
print("ev is: ", ev2)


if ev == e and ev2 == e2:
    print("\nev is equal to e in both cases. \nSignature Verified!\n")
else:
    print("ev is not equal to e. \n Signature not verified!\n")