#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Dylan @ 2016-04-27 10:38:40

import sPickle
import numpy as np
from tools import GetFileFromRootDir, getArrayFromPattern
from config import nTrain, SEED, REMOVE_SIL

np.random.seed(SEED)
X_train_N = []
X_train_V = []
X_test_N = []
X_test_V = []
fidx = 0
idxarray = []  # used to remove 80% silence

if __name__ == '__main__':

    featnamearray, feattypedict, featdict = sPickle.load(
            open("featdict.pkl", "rb"))

    labfiles = GetFileFromRootDir("./frame", "lab")
    for file in labfiles:
        print file
        fidx += 1
        with open(file) as fp:
            for line in fp.readlines():
                lines = line.strip().split()
                if(len(lines) < 3):
                    break
                label = lines[0]
                dataarray = getArrayFromPattern(label)
                if(fidx <= nTrain):
                    if (dataarray[2] == 'sil' and
                            REMOVE_SIL is True and fidx < nTrain * 0.8):
                        idxarray.append(False)
                    else:
                        idxarray.append(True)
                        X_train_V.append(dataarray)
                        X_train_N.append(lines[1:])
                else:
                    X_test_V.append(dataarray)
                    X_test_N.append(lines[1:])

    if REMOVE_SIL is True:
        idxarray = np.array(idxarray)
        sPickle.dump(idxarray, open("idx.pkl", "wb"))

    X_train_N = np.array(X_train_N, dtype=np.float32)
    X_test_N = np.array(X_test_N, dtype=np.float32)
    X_train_V = np.array(X_train_V)
    X_test_V = np.array(X_test_V)

    X_mean_N = X_train_N.mean(axis=0)
    X_std_N = X_train_N.std(axis=0)
    X_train_N = (X_train_N - X_mean_N) / X_std_N
    X_test_N = (X_test_N - X_mean_N) / X_std_N
    np.random.shuffle(X_train_V)
    np.random.seed(SEED)  # reset seeds
    np.random.shuffle(X_train_N)

    print X_train_N.shape, X_train_V.shape, X_test_N.shape, X_test_V.shape

    output = open('X.pkl', 'wb')
    sPickle.dump(X_mean_N, output)
    sPickle.dump(X_std_N, output)
    sPickle.dump(X_train_N, output)
    sPickle.dump(X_train_V, output)
    sPickle.dump(X_test_N, output)
    sPickle.dump(X_test_V, output)
    output.close()
    print "end"
