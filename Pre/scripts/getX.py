#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Dylan @ 2016-04-27 10:38:40

import os
import re
import sPickle
import numpy
from tools import GetFileFromRootDir,getArrayFromPattern
from config import *

numpy.random.seed(SEED)

pattern = 'p1^p2-p3+p4=p5/A:a1+a2+a3/B:b1-b2_b3/C:c1_c2+c3/D:d1+d2_d3/E:e1_e2!e3_e4-e5/F:f1_f2#f3_f4@f5_f6|f7_f8/G:g1_g2%g3_g4_g5/H:h1_h2/I:i1-i2@i3+i4&i5-i6|i7+i8/J:j1_j2/K:k1+k2-k3'

featdict = dict()
feattypedict=dict()
featnamearray=[]
X_train_N=[]
X_train_V=[]
X_test_N=[]
X_test_V=[]
fidx=0

if __name__ == '__main__':
#    featnamearray=getArrayFromPattern(pattern)
#    fp_feattype=open("feat.type","w")
#    for x in featnamearray:
#        fp_feattype.write("%s %d\n" % (x,1))
#    fp_feattype.close()

    with open("scripts/feat.type") as fp:
        for line in fp.readlines():
            if line == "":
                break
            featname,feattype=line.strip().split()
            featnamearray.append(featname)
            feattypedict[featname]=int(feattype)


    for featname in featnamearray:
        featdict[featname]=dict()

    labfiles=GetFileFromRootDir("./frame","lab")
    for file in labfiles:
        print file
        fidx+=1
        with open(file) as fp:
            for line in fp.readlines():
                lines=line.strip().split()
                if(len(lines)<3):
                    break
                label=lines[0]
                dataarray=getArrayFromPattern(label)
                if(fidx <= nTrain):
                    X_train_V.append(dataarray)
                    X_train_N.append(lines[1:])
                else:
                    X_test_V.append(dataarray)
                    X_test_N.append(lines[1:])
                for x in xrange(len(dataarray)):
                    featdict[featnamearray[x]][dataarray[x]]=1

    for featname,featvaluedict in featdict.items():
        i=0
        flag=0
        for key in sorted(featvaluedict.keys()):
            if key != 'xx':
                 featvaluedict[key]=i
                 i=i+1
            else:
                 flag=1
        if flag==1:
            featvaluedict['xx']=i;

    #pprint.pprint(featdict)
    """
    save the dictionary information
    """
    output=open('featdict.pkl','wb')
    sPickle.dump(featnamearray , output)
    sPickle.dump(feattypedict , output)
    sPickle.dump(featdict , output)
    output.close()

    

    X_train_N = numpy.array(X_train_N, dtype = numpy.float32)
    X_test_N = numpy.array(X_test_N, dtype = numpy.float32)
    X_mean_N = X_train_N.mean(axis = 0)
    X_std_N = X_train_N.std(axis = 0)
    X_train_N = (X_train_N - X_mean_N) / X_std_N
    X_test_N = (X_test_N - X_mean_N) / X_std_N

    X_train_V = numpy.array(X_train_V)
    X_test_V = numpy.array(X_test_V)

    numpy.random.shuffle(X_train_V)
    numpy.random.seed(SEED)#reset seeds
    numpy.random.shuffle(X_train_N)

    output =open('X.pkl','wb')
    sPickle.dump(X_mean_N , output)
    sPickle.dump(X_std_N , output)
    sPickle.dump(X_train_N , output)
    sPickle.dump(X_train_V , output)
    sPickle.dump(X_test_N , output)
    sPickle.dump(X_test_V , output)
    output.close()
    print "end"
