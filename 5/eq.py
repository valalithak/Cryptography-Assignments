import random as rd
import sympy as sp
import numpy as np
import clib as cl
from textwrap import wrap


k = 5
n = 7


def calc(poly, x, p):
    val = 0
    for i, a in enumerate(poly):
        val += (a * (x**i)) % p 
    
    return val %p



def solve_poly(points,d, p):
    x = points[:d, 0]
    x = np.tile(x, (d,1)).T
    te = np.tile(np.arange(d), (d,1))
    A = np.power(x,te)
    return sp.Matrix(A).inv_mod(p) @ points[:d, 1]
    

if __name__ == '__main__':
	ml = 2000
	message = rd.getrandbits(ml-1) + 2**(ml-1)
	message_bin = bin(message)[2:]
	pl = ml // k + 1
	data = list(map(lambda x: int('1'+x,2), wrap(message_bin, pl)))
	# data = [rd.randint(2**150,2**200) for i in range(k)]
	print(message)
	print(data)



	lg = max(max(data), n)
	# p = sp.nextprime(lg)
	nbits = lg.bit_length()+1
	p = cl.gen_safe_prime(nbits)
	pf = [2, (p-1)//2]
	x = rd.getrandbits(nbits)
	g = cl.find_gen(p-1,pf)
	pks = {'n': nbits, 'prime': p, 'gen': g, 'y': pow(g,x,p)}
	print(pks)



	points = []
	for i in range(1,n+1):
	    points.append((i, calc(data, i,p)))
	points = np.array(points)
	print(points)


	signs = []
	for y in points[:, 1]:
	    signs.append(cl.sign(pks, y, x,True))

	store_n = []
	for m, sn in zip(points[:,1],signs):
	    dt = {'msg': m, 'sign': sn}
	    store_n.append(dt)


	for bl in store_n:
	    print(cl.verifier(pks,bl['sign'],bl['msg']))


	store_n[2]['msg'] = 123
	store_n[4]['msg'] = 141412
	valid = []
	ncp_dt = []
	for i, bl in enumerate(store_n):
	    valid.append(cl.verifier(pks,bl['sign'],bl['msg']))
	    if valid[-1]:
	        ncp_dt.append((i+1, bl['msg']))
	ncp_dt = np.array(ncp_dt)
	print(valid)


	values = solve_poly(ncp_dt[:k], k, p) % p
	values == data



	v_bin = ''.join(list(map(lambda x: bin(x)[3:], values)))


	print(int(v_bin,2))
	print(message)
	print(message == int(v_bin, 2))

