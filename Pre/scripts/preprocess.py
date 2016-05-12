#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Dylan @ 2016-04-27 10:38:40

import sPickle
import numpy as np
import os
from tools import GetBasenameFromDir, getArrayFromPattern
from config import nTrain, SEED, REMOVE_SIL, OUTPUT_DIM

np.random.seed(SEED)
X_train_N = []
X_train_V = []
X_test_N = []
X_test_V = []
Y_train = []
Y_test = []
fidx = 0

if __name__ == '__main__':

    featnamearray, feattypedict, featdict = sPickle.load(
            open("featdict.pkl", "rb"))

    basenames = GetBasenameFromDir("./frame", ".lab")
    for basename in basenames:
        labfile = os.path.join("./frame", basename + ".lab")
        cmpfile = os.path.join("./cmp1", basename + ".cmp1")
        if not os.path.isfile(cmpfile):
            print "Warning: file %s do not exist, skip..." % cmpfile
            continue
        X_tmp_N = []
        X_tmp_V = []
        idxarray = []  # used to remove silence
        Y_tmp = np.fromfile(cmpfile, dtype='float32')
        Y_tmp = Y_tmp.reshape(-1, OUTPUT_DIM)
        print basename
        fidx += 1
        with open(labfile) as fp:
            for line in fp.readlines():
                lines = line.strip().split()
                if(len(lines) < 3):
                    break
                label = lines[0]
                dataarray = getArrayFromPattern(label)
                if (dataarray[2] == 'sil' and REMOVE_SIL is True):
                    idxarray.append(False)
                else:
                    idxarray.append(True)
                    X_tmp_V.append(dataarray)
                    X_tmp_N.append(lines[1:])

        if REMOVE_SIL is True:
            Y_tmp = Y_tmp[np.array(idxarray)]

        assert (len(Y_tmp) == len(X_tmp_V))

        if fidx <= nTrain:
            X_train_N += X_tmp_N
            X_train_V += X_tmp_V
            Y_train += list(Y_tmp)
        else:
            X_test_N += X_tmp_N
            X_test_V += X_tmp_V
            Y_test += list(Y_tmp)

    X_train_N = np.array(X_train_N, dtype=np.float32)
    X_test_N = np.array(X_test_N, dtype=np.float32)
    X_train_V = np.array(X_train_V)
    X_test_V = np.array(X_test_V)
    Y_train = np.array(Y_train, dtype='float32')
    Y_test = np.array(Y_test, dtype='float32')

    X_mean_N = X_train_N.mean(axis=0)
    X_std_N = X_train_N.std(axis=0)
    Y_mean = Y_train.mean(axis=0)
    Y_std = Y_train.std(axis=0)

    sPickle.dump((X_mean_N, X_std_N, Y_mean, Y_std),
                 open("normalize.pkl", "wb"))

    X_train_N = (X_train_N - X_mean_N) / X_std_N
    X_test_N = (X_test_N - X_mean_N) / X_std_N
    Y_train = (Y_train - Y_mean) / Y_std
    Y_test = (Y_test - Y_mean) / Y_std

    np.random.shuffle(X_train_V)
    np.random.seed(SEED)  # reset seeds
    np.random.shuffle(X_train_N)

    print(X_train_N.shape, X_train_V.shape, X_test_N.shape,
          X_test_V.shape, Y_train.shape, Y_test.shape)

    output = open('data.pkl', 'wb')
    sPickle.dump(X_train_N, output)
    sPickle.dump(X_train_V, output)
    sPickle.dump(X_test_N, output)
    sPickle.dump(X_test_V, output)
    sPickle.dump(Y_train, output)
    sPickle.dump(Y_test, output)
    output.close()
    print "end"
