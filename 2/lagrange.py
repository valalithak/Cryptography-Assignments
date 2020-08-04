import os
import sys

def lagrange(x,i,xm):
    """ Evaluates  the i-th  Lagrange  polynomial  at x based on grid  data xm """
    n=len(xm)-1
    y=1
    for j in  range(n+1):
        if i!=j:
            y*=(x-xm[j])/(xm[i]-xm[j])
    return y

def interpolation(x,xm ,ym):
    n=len(xm)-1
    lagrpoly=array([lagrange(x,i,xm) for i in range(n+1)])
    y = dot(ym ,lagrpoly)
    return y


xm = array([1,2,3,4,5,6])
ym = array([-3,0,-1,2,1,4])
xplot = \
yplot = \
print(interpolation(xplot ,xm,ym))