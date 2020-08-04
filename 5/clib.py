from random import randint, getrandbits
# import sympy as sp
from textwrap import wrap

def p(t):
    return t.ljust(30)

def miillerTest(d, n):       
    a = 2 + randint(1, n - 4); 
    x = pow(a, d, n); 
    if (x == 1 or x == n - 1): 
        return True; 

    while (d != n - 1): 
        x = (x * x) % n; 
        d *= 2; 
        if (x == 1): 
            return False; 
        if (x == n - 1): 
            return True; 
  
    return False;

def isPrime( n, k=20): 
    # Corner cases
    # return sp.isprime(n) 
    if (n <= 1 or n == 4): 
        return False; 
    if (n <= 3): 
        return True; 
  
    # Find r such that n =  
    # 2^d * r + 1 for some r >= 1 
    d = n - 1; 
    while (d % 2 == 0): 
        d //= 2; 
  
    # Iterate given nber of 'k' times 
    for i in range(k): 
        if (miillerTest(d, n) == False): 
            return False; 
  
    return True


def mod_exp(a, b, n):
    # print(a,b,n)
    a,b,n = int(a), int(b), int(n)
    return pow(a,b,n)

def gcd(a,b):
    if a==0: return b
    else: return gcd(b%a, a)

def get_gen(n):
    for i in range(2,n):
        if gcd(i,n) == 1:
            return i

def generate_big_prime(n):
    found_prime = False
    while not found_prime:
        p = randint(2**(n-1), 2**n)
        # if sp.isprime(p):
        if isPrime(p):
            return p

def gen_safe_prime(n):
    while True:
        q = generate_big_prime(n-1)
        if isPrime(2*q+1):
            return 2*q+1
    return None


def is_gen(h, q, prime_factors):
    for f in prime_factors:
        # print(f, q/f)
        if mod_exp(h, q/f, q+1) == 1:
            return False
    return True 

def find_gen(q, prime_factors):
    for i in range(100):
        h = randint(2,q)
        # print('ch', h)
        if is_gen(h, q, prime_factors):
            return h
    return None

def check_gen(gen,p):
    print('Checking generator: ',end='')
    if mod_exp(gen, p-1, p) == 1:
        print(True)
    else:
        print(False)
        exit(1)


def get_bits(x):
    mask = (1 << (nbits//2)) - 1
    rt = x & mask
    lt = x >> (nbits//2)
    return lt, rt


def hash(pks, x, y):
    k = 123142124
    g = pks['prime']
    p = pks['gen']

    z = mod_exp(g, k, p)
 
    return (mod_exp(g, x, p) * mod_exp(z,y,p)) % p

def hash_md(pks, msg, t=100):
    p = pks['prime']
    n = pks['n']
    b = bin(msg)[2:]
    mk = wrap(b, n)
    # t= rd.randint(2,p-1)
    for m in mk:
        t = hash(pks, m, t)
#         print(t)
    return t

def sign(pks, msg, x,md=True):
    p = pks['prime']
    g = pks['gen']
    r = randint(2, p-1)

    t = mod_exp(g, r, p)
    if md:
        c =hash_md(pks,msg,t)
    else:
        c = hash(pks, msg, t)

    z = c*x +r
    signature = {'t': t, 'z': z}
    return signature

def verifier(pks, signature, msg):
    t = signature['t']
    z = signature['z']
    c = hash(pks, msg, t)
    p = pks['prime']
    g = pks['gen']
    y = pks['y']
    c = hash_md(pks, msg, t)
    return mod_exp(g,z,p) == (mod_exp(y, c, p) * t)%p

if __name__ == '__main__':
    nbits = int(input("Enter n(no of bits)".ljust(30)+': ' ))
    k = getrandbits(nbits)
    p = gen_safe_prime(nbits)


    print('Found safe prime'.ljust(30)+':', p)
    print('Group Zp* of order'.ljust(30)+':',p-1)
    prime_factors = [2, (p-1)/2]
    gen = find_gen(p-1, prime_factors)
    print('Found generator'.ljust(30)+':', gen)


    x = getrandbits(nbits)
    print('Secret key'.ljust(30)+':',x)
    public_keys = {'n': nbits, 'prime': p, 'gen': gen, 'y': mod_exp(gen,x,p)}

    msg = getrandbits(nbits)
    print('Message'.ljust(30)+':', msg)
    # msg = int(input('Enter msg: '))
    signature = sign(public_keys, msg, x)
    # signature = {'t': t, 'z': z}
    print('Signature'.ljust(30)+':', 't =',t,'\n'.ljust(32),'z =',z)

    print('Verifier'.ljust(30)+':',verifier(public_keys, signature, msg))