#!/usr/bin/env python
# -*- coding: utf-8 -*-

import k_means as km
import fuzzy_c_means as cm
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.spatial import ConvexHull

k = 5 #クラスタ数
m = 1.7 #ファジィさの度合

def plot(ps):
    x = [i[0] for i in ps]
    y = [i[1] for i in ps]
    plt.plot(x, y, "o")

def draw_regs(ps,mem_ship,mode):
    for i in xrange(k):
        P = []
        if mode == 0:
            for j in xrange(len(ps)):
                if i == mem_ship[j]:
                    P.append(ps[j])
        else:
            for j in xrange(len(ps)):
                if mem_ship[j][i] > 0.1:
                    P.append(ps[j])
        if P != []:
            hull = ConvexHull(P)
            x = [P[l][0] for l in hull.vertices]
            y = [P[l][1] for l in hull.vertices]
            orig_len = len(x)
            x = x[-3:-1] + x + x[1:3]
            y = y[-3:-1] + y + y[1:3]
            t = np.arange(len(x))
            ti = np.linspace(2, orig_len + 1, 10 * orig_len)
            xi = interp1d(t, x, kind='cubic')(ti)
            yi = interp1d(t, y, kind='cubic')(ti)
            plt.fill(xi, yi, alpha=0.2)
        
if __name__ == '__main__':
    ps = np.random.rand(300,2)
    plt.subplot(211)
    plot(ps)
    draw_regs(ps,km.k_means(ps,k),0)
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)

    plt.subplot(212)
    plot(ps)
    draw_regs(ps,cm.c_means(ps,k,m),1)
    plt.xlim(-0.1, 1.1)
    plt.ylim(-0.1, 1.1)
    
    plt.show()
    
