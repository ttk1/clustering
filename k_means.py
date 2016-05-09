#! /bin/env python
# coding:utf-8

import numpy as np

def centroid(mem_ship,ps):
    V = [np.array([0.]*len(ps[0])) for i in xrange(k)]
    count = [0]*k
    for i in xrange(len(ps)):
        count[mem_ship[i]] += 1
        V[mem_ship[i]] += ps[i]
    V = [V[i]/count[i] for i in xrange(k)]
    return V

def argmin(i,V,ps,k):
    min_i = 0
    min = sum((V[0]-np.array(ps[i]))**2)
    for j in xrange(1,k):
        tmp = sum((V[j]-np.array(ps[i]))**2)
        if tmp < min:
            min_i = j
            min = tmp
    return min_i

def update(V,ps,k):
    new_mem_ship  = [None]*len(ps)
    for i in xrange(len(ps)):
        new_mem_ship[i] = argmin(i,V,ps,k)
    return new_mem_ship
            
def k_means(ps,k):
    while True:
        mem_ship = list(np.random.randint(0,k,len(ps)))
        if len(set(mem_ship)) == k:
            break
    while True:
        V = centroid(mem_ship,ps,k)
        new_mem_ship = update(V,ps,k)
        if mem_ship == new_mem_ship:
            break
        else:
            mem_ship = new_mem_ship
    return mem_ship
