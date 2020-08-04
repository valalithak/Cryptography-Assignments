# -*- coding: utf-8 -*-
import random as rd
import sympy as sp
import numpy as np
import clib as cl
import eq
from textwrap import wrap

n = 7
k = 5

def encode(msg):
    x = 0
    for i,m in enumerate(msg):
        x += (ord(m)-97) * (26**i)
    print("Actual Message:", msg)
    print("Encoded Message:", x)
    return x

def decode(x):
    msg = ''
    while(x > 0):
        msg += chr((x % 26) +97)
        x //= 26
    return msg

class TransferProtocol:
    def __init__(self):
        self.data_z = None
        self.data_c = None
        pass
    
    @staticmethod
    def get_points(blocks, p):
        points = []
        for i in range(1,n+1):
            points.append((i, eq.calc(blocks, i, p)))
        points = np.array(points,dtype=object)
        return points
    
    def transfern(self, k_blocks, pks, sk):
        p = pks['prime']
        points = self.get_points(k_blocks, p)
        
        signs = []
        for y in points[:, 1]:
            signs.append(cl.sign(pks, y, sk, True))
        
        self.data = []
        for m, sn in zip(points[:,1],signs):
            dt = {'msg': m, 'sign': sn}
            self.data.append(dt)
        
        
        
        
    def transfer(self,k_blocks, pks, sk):
        p = pks['prime']
        # print(p)
        blocks_z = [bl['z'] for bl in k_blocks]
        blocks_c = [bl['c'] for bl in k_blocks]
        
        points_z = self.get_points(blocks_z, p)
        points_c = self.get_points(blocks_c, p)
        
        
        signs_z = []
        signs_c = []
        
        for y,y1 in zip(points_z[:, 1], points_c[:, 1]):
            signs_z.append(cl.sign(pks, y, sk,True))
            signs_c.append(cl.sign(pks, y1, sk, True))
        
        self.data_z = []
        self.data_c = []
        for m, sn in zip(points_z[:,1],signs_z):
            dt = {'msg': m, 'sign': sn}
            self.data_z.append(dt) 
        
        for m, sn in zip(points_c[:,1],signs_c):
            dt = {'msg': m, 'sign': sn}
            self.data_c.append(dt) 
    
    @staticmethod
    def get_data(data, pks):
        p = pks['prime']
        valid = []
        ncp_dt = []
        
        for i, bl in enumerate(data):
            valid.append(cl.verifier(pks,bl['sign'],bl['msg']))
            if valid[-1]:
                ncp_dt.append((i+1, bl['msg']))
      
        print("Checking true or false for validity of each block")
        print(valid)
        
        ncp_dt = np.array(ncp_dt,dtype=object)
        values = eq.solve_poly(ncp_dt[:k], k, p) % p
        return values
    
    def get(self, pks):
        vals_z = self.get_data(self.data_z, pks)
        vals_c = self.get_data(self.data_c, pks)
        
        vals = []
        for vz, vc in zip(vals_z, vals_c):
            vals.append({'z': vz, 'c': vc})

        return vals

def get_keys(nbits):
    p = cl.gen_safe_prime(nbits)
    pf = [2, (p-1)//2]
    x = rd.getrandbits(nbits)
    g = cl.find_gen(p-1,pf)
    pks = {'n': nbits, 'prime': p, 'gen': g, 'y': pow(g,x,p)}
    sk = x
    return pks, sk

def encrypt(message, pks):
    p = pks['prime']
    g = pks['gen']
    r = rd.randint(2,p-1)
    z = pow(g,r,p)
    s = pow(pks['y'], r, p)
    c = (message * s)
    print('s value in encryption step: ', s)
    return z, c

def decrypt(cipher, pks, sk):
    p = pks['prime']
    s = pow(cipher['z'], sk, p)
    print('s value in decryption step: ',s)
    message = cipher['c'] // s
    return message

message = ["Message1","Message2", "Message3", "Message4", "Message5"]
data_blocks = [encode(word) for word in message]

nbits = 128

pks_en_A, sk_en_A = get_keys(nbits)
print("For A")
print(pks_en_A, sk_en_A)

pks_en_B, sk_en_B = get_keys(nbits)
print("For B")
print(pks_en_B, sk_en_B)

nbits = 300

pks_tp_A, sk_tp_A = get_keys(nbits)
print("For A")
print(pks_tp_A, sk_tp_A)

pks_tp_B, sk_tp_B = get_keys(nbits)
print("For B")
print(pks_tp_B, sk_tp_B)

tp = TransferProtocol()

index = 4
length = 54
l_2 = 2 * length

rd_array = []
for _ in range(k):
    z = rd.getrandbits(length-1) + 2**(length-1)
    c = rd.getrandbits(l_2-1) + 2**(l_2-1)
    rd_array.append({'z': z, 'c': c})
    
rd_store = rd_array[index]
print(rd_array)

z, c = encrypt(rd_array[index]['z'], pks_en_B)
rd_array[index] = {'z': z, 'c': c}
print(rd_array)


tp.transfer(rd_array, pks_tp_A, sk_tp_A)

# print(rd_array[1]['c'].bit_length())
# print(sk_tp_A.bit_length())

sent_data = tp.get(pks_tp_A)

# print(sent_data)

rd_array == sent_data

# print(sent_data[index]['c'])

dec_data = [int(decrypt(dt, pks_en_B, sk_en_B)) for dt in sent_data]

# print(rd_store, dec_data[index])

xor_data = [ddt ^ ddb  for ddt, ddb in zip(dec_data, data_blocks)]

tp.transfern(xor_data, pks_tp_B, sk_tp_B)

data_recv = tp.get_data(tp.data, pks_tp_B)

decode(rd_store['z'] ^ int(data_recv[index]))



