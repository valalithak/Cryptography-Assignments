import os
import sys
import random as rnd
import sympy

q = 99991 #2695139 #order of field

print("Input k:")
k = int(input())
print("Input n:")
n = int(input())

#For the purpose of this assignment, I will consider that I have the file contents as a list of K integers
#Right now, I'm creating a list of k random integers
file_contents = []
for i in range(0, k):
    file_contents.append(rnd.randint(1, 1000))

#Now that we have k numbers, we will define a polynomial f(x) as summation of file_contents[i]*(x**(k-i)) and finally mod q
#Since i ranges from 0 to k, we get f(x) to be a k-1 degree polynomial

def compute_f(x):
    val = 0
    for i in range(0, k):
        val += file_contents[i]*(pow(x, k-i))
    return val%q

#Now we select n points of the form (x, f(x))
n_points = {}
for i in range(1, n+1):
    n_points[i] = compute_f(i)

#Using digital signatures to identify and recover corrupted blocks

#Step1 : Signing each of the n blocks with digital signature
# I will use the hash function created in Evaluation 1 and XOR the x and y coordinates to get hash value for a point

x = sympy.randprime(1000, 9999) # private key = prime number of length 4
g = 2 #generator
y = pow(g, x, q) #public verification key
c = rnd.randint(1, q - 1)
r = pow(g, c, q)

def dlpHash(r,m):
    return ((pow(g, r)%q)*(pow(y, m%q)%q))%q


#signing
point_hash = {}
for i in n_points.keys():
    m1 = i
    m2 = n_points[i]
    e = dlpHash(r, m1) ^ dlpHash(r, m2) #part 1 of signature
    s = (c - (x * e)) % (q-1) # part 2 of signature
    signature = []
    signature.append(e)
    signature.append(s)
    point_hash[i] = signature

# Step 2: Verification
print("Verifying...\n")
corr_block = 0
index = 0
for i in n_points.keys():
    index+=1
    m1 = i
    m2 = n_points[i]
    e = point_hash[i][0]
    s = point_hash[i][1]
    rv = (pow(g, s, q) * pow (y, e, q)) % q
    ev = dlpHash(rv, m1) ^ dlpHash(rv, m2)

    if e==ev:
        print("Block "+ str(index) + " uncorrputed")
    else:
        print("Block "+ str(index) + " corrupted")
        corr_block+=1

#Atleast e blocks are corrputed => atmost n-e blocks are available.
#Since we need atleast k points to find out the equation of the polynomial, => this idea works if (n-e) >= k
print("\n")
print("n = " + str(n))
print("e = " + str(corr_block))
print("k = "+ str(k))
    
if n - corr_block >= k:
    print("(n-e)>=k => We can recover the lost data")
else:
    print("(n-e)<k => We cannot recover the lost data")
