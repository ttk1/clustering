#! /bin/env python
# coding:utf-8

#
# fuzzy c means from, http://ibisforest.org/index.php?ファジィc-means法
#

#import create_corpus as cc
import mecab_inc as mi

import numpy as np
import random
import json
import sys
reload(sys)
sys.setdefaultencoding("utf-8")

file_name = 'tweets/new.txt'
#file_name = 'tweets/test_data.txt'
k = 10 #number of clusters
m = 1.7 #fuzzy param
th = 0.1

def create_corpus(file_name):
    global W,C
    W = {}
    C = {}
    for line in open(file_name,'r'):
        text = mi.clean_text(line)
        WL = mi.create_word_list(text)
        WL = sorted(set(WL))
        for i in xrange(len(WL)):
            if WL[i] in W:
                W[WL[i]] += 1
            else:
                W[WL[i]] = 1
            for j in xrange(i+1,len(WL)):
                if WL[i] in C:
                    if WL[j] in C[WL[i]]:
                        C[WL[i]][WL[j]] += 1
                    else:
                        C[WL[i]][WL[j]] = 1
                else:
                    C[WL[i]] = {WL[j]:1}

def f(i,j):
    try:
        a = C[Words[i]][Words[j]]
        return a*1.0/(W[Words[i]]+W[Words[j]]-a)
    except:
        return 0

def create_table():
    #単語Word[i]とWord[j]の共起度table[i][j]=table[j][i]を生成
    global table
    table = [[None]*len(Words) for i in xrange(len(Words))]
    for i in xrange(len(Words)):
        table[i][i] = 1
        for j  in xrange(i+1,len(Words)):
            table[i][j] = f(i,j)
            table[j][i] = table[i][j]

def update(V):
    new_mem_ship  = [np.array([None]*k) for i in xrange(len(Words))]
    for i in xrange(len(Words)):
        for j in xrange(k):
            new_mem_ship[i][j] = 1.0/sum((np.linalg.norm(np.array(table[i])-V[j])/np.linalg.norm(np.array(table[i])-V[l]))**(2.0/(m-1)) for l in xrange(k))
    return new_mem_ship
            
def centroid(mem_ship):
    V = [np.array([0]*len(Words)) for i in xrange(k)]
    for i in xrange(k):
        V[i] = sum([mem_ship[j][i]**m*np.array(table[j]) for j in xrange(len(Words))])/sum([mem_ship[j][i]**m for j in xrange(len(Words))])
    return V
            
def c_means():
    mem_ship = [np.random.random(k) for i in xrange(len(Words))]
    mem_ship = [mem_ship[i]/sum(mem_ship[i]) for i in xrange(len(Words))]
    r = 0
    while True:
        r+=1
        V = centroid(mem_ship)
        new_mem_ship = update(V)
        diff = sum([np.linalg.norm(mem_ship[i]-new_mem_ship[i]) for i in xrange(len(Words))])
        print diff
        if diff < 0.0001:
            break
        else:
            mem_ship = new_mem_ship
            
    print '単語数:',len(Words)
    print 'クラスタ数:',k
    print 'ファジィさm:',m
    print '繰り返し回数:',r
    print '閾値:',th
    
    return mem_ship

if __name__ == '__main__':
    create_corpus(file_name)
    Words = sorted(W) #dict W -> list Words
    create_table()
    mem_ship = c_means()

    for i in xrange(k):
        print 'cluster num =',i
        for j in xrange(len(Words)):
            if mem_ship[j][i] > th and W[Words[j]] > 2:
                print Words[j]+':',W[Words[j]],
        print ''

    
    mem_ship = [list(mem_ship[i]) for i in xrange(len(Words))]
    for i in mem_ship:
        print i
    with open('c-means.json', 'w') as f:
        json.dump(mem_ship,f)
    with open('c-means_words.json', 'w') as f:
        json.dump(Words,f)
    with open('c-means_corpus.json', 'w') as f:
        json.dump(C,f)
    

