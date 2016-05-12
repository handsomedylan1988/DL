#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Dylan @ 2016-04-27 10:38:40

import sPickle
import numpy as np
import os
from tools import GetBasenameFromDir
from config import nTrain, REMOVE_SIL, OUTPUT_DIM

X_train_N = []
Y_train = []
fidx = 0
idxarray = []  # used to remove silence

if __name__ == '__main__':

    basenames = GetBasenameFromDir("./frame", ".lab")
    for basename in basenames:
        print basename
        fidx += 1
        if fidx <= nTrain:
            labfile = os.path.join("./frame", basename + ".lab")
            cmpfile = os.path.join("./cmp1", basename + ".cmp1")
            if not os.path.isfile(cmpfile):
                print "Warning: file %s do not exist, skip..." % cmpfile
                continue
            X_tmp = []
            Y_tmp = np.fromfile(cmpfile, dtype='float32')
            Y_tmp = Y_tmp.reshape(-1, OUTPUT_DIM)
            with open(labfile) as fp:
                for line in fp.readlines():
                    lines = line.strip().split()
                    if(len(lines) < 3):
                        break
                    if (lines[0].find("-sil+")!=-1 and REMOVE_SIL is True):
                        idxarray.append(False)
                        pass
                    else:
                        idxarray.append(True)
                        X_tmp.append(lines[1:])
                        
            assert(len(idxarray) == len(Y_tmp))
            Y_tmp = ( 
            Y_train += Y_tmp
            X_train += X_tmp
   
    X_mean = X_train.mean(axis=0)
    X_std = X_train.std(axis=0)
    
    Y_mean = Y_train.mean(axis=0)
    Y_std = Y_train.std(axis=0)

    output = open('Normalize.pkl', 'wb')
    sPickle.dump((X_mean, X_std, Y_mean, Y_std), output)
    output.close()
    print "end"
