#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import json
import matplotlib.pyplot as plt
import pylab
import networkx as nx
import pydot
from scipy.interpolate import interp1d
from scipy.spatial import ConvexHull

k = 10

def gen_graph():
    global graph,labels,pos
    graph = nx.Graph()
    labels = {}
    for i in Words:
        graph.add_node(i)
    for i in corpus:
        for j in corpus[i]:
            graph.add_edge(i,j)
            #labels[(i,j)] = corpus[i][j]
    pos = nx.spring_layout(graph, k = 1.)
            
            

def draw_graph():
    #font_path = "/usr/share/fonts/japanese/TrueType/sazanami-gothic.ttf"
    #font_prop = font_manager.FontProperties(fname=font_path)
    nx.draw_networkx_nodes(graph, pos, node_size=100, node_color="w")
    nx.draw_networkx_edges(graph, pos, width=1)
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=labels)
    nx.draw_networkx_labels(graph, pos, font_size=20, font_color="r")

def draw_regs():
    for i in xrange(k):
        points = []
        for j in xrange(len(Words)):
            if mem_ship[j][i] > 0.1:
                points.append(pos[Words[j]])
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
    with open('c-means.json', 'r') as f:
        mem_ship = json.load(f)
    with open('c-means_words.json', 'r') as f:
        Words = json.load(f)
    with open('c-means_corpus.json', 'r') as f:
        corpus = json.load(f)
    gen_graph()
    draw_graph()
    draw_regs()
    plt.show()
    
'''
x = [-0.25, -0.625, -0.125, -1.25, -1.125, -1.25,
     0.875, 1.0, 1.0, 0.5, 1.0, 0.625, -0.25]
y = [1.25, 1.375, 1.5, 1.625, 1.75, 1.875, 1.875,
     1.75, 1.625, 1.5, 1.375, 1.25, 1.25]

# Pad the x and y series so it "wraps around".
# Note that if x and y are numpy arrays, you'll need to
# use np.r_ or np.concatenate instead of addition!
orig_len = len(x)
x = x[-3:-1] + x + x[1:3]
y = y[-3:-1] + y + y[1:3]

t = np.arange(len(x))
ti = np.linspace(2, orig_len + 1, 10 * orig_len)

xi = interp1d(t, x, kind='cubic')(ti)
yi = interp1d(t, y, kind='cubic')(ti)

fig, ax = plt.subplots()
ax.fill(xi, yi, alpha=0.2)
#ax.plot(x, y)
ax.margins(0.05)
plt.show()
'''
