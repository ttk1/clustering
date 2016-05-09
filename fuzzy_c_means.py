#! /bin/env python
# coding:utf-8

import numpy as np

def update(V,ps,k,m):
    new_mem_ship  = [np.array([None]*k) for i in xrange(len(ps))]
    for i in xrange(len(ps)):
        for j in xrange(k):
            new_mem_ship[i][j] = 1.0/sum((np.linalg.norm(np.array(ps[i])-V[j])/np.linalg.norm(np.array(ps[i])-V[l]))**(2.0/(m-1)) for l in xrange(k))
    return new_mem_ship
            
def centroid(mem_ship,ps,k,m):
    V = [np.array([0.]*len(ps)) for i in xrange(k)]
    for i in xrange(k):
        V[i] = sum([mem_ship[j][i]**m*np.array(ps[j]) for j in xrange(len(ps))])/sum([mem_ship[j][i]**m for j in xrange(len(ps))])
    return V
            
def c_means(ps,k,m):
    mem_ship = [np.random.random(k) for i in xrange(len(ps))]
    mem_ship = [mem_ship[i]/sum(mem_ship[i]) for i in xrange(len(ps))]
    while True:
        V = centroid(mem_ship,ps,k,m)
        new_mem_ship = update(V,ps,k,m)
        diff = sum([np.linalg.norm(mem_ship[i]-new_mem_ship[i]) for i in xrange(len(ps))])
        if diff < 0.0001:
            break
        else:
            mem_ship = new_mem_ship
    return mem_ship
    

