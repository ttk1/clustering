#!/usr/bin/env python
# -*- coding: utf-8 -*-

import k_means as km
import fuzzy_c_means as mc
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
from scipy.spatial import ConvexHull

k = 10 #クラスタ数
m = 1.7 #ファジィさの度合

def draw_regs(ps,mem_ship):
    for i in xrange(k):
        hull = ConvexHull(points)
        x = [points[i][0] for i in hull.vertices]
        y = [points[i][1] for i in hull.vertices]
        orig_len = len(x)
        x = x[-3:-1] + x + x[1:3]
        y = y[-3:-1] + y + y[1:3]
        t = np.arange(len(x))
        ti = np.linspace(2, orig_len + 1, 10 * orig_len)
        xi = interp1d(t, x, kind='cubic')(ti)
        yi = interp1d(t, y, kind='cubic')(ti)
        plt.fill(xi, yi, alpha=0.2)
        


if __name__ == '__main__':
    ps = np.random.rand(100,2)
    mem_ship = c_means(ps)
    
    draw_regs()
    plt.show()
    
