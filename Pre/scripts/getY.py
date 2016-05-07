#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Dylan @ 2016-04-24 20:23:07

import os
import numpy as np
import sPickle
from config import nTrain, SEED, OUTPUT_DIM, REMOVE_SIL

np.random.seed(SEED)

Y_train = []
Y_test = []
fidx = 0
for file in [os.path.join("cmp1", f) for f in sorted(os.listdir("cmp1/"))]:
    fidx += 1
    labelarray = list(np.fromfile(file, dtype=np.float32))
    assert len(labelarray) % OUTPUT_DIM == 0
    nFrame = len(labelarray) / OUTPUT_DIM
    if fidx <= nTrain:
        Y_train += labelarray
    else:
        Y_test += labelarray

Y_train = np.array(Y_train, dtype=np.float32).reshape(-1, OUTPUT_DIM)
Y_test = np.array(Y_test, dtype=np.float32).reshape(-1, OUTPUT_DIM)

if REMOVE_SIL is True:
    idxarray = sPickle.load(open("idx.pkl", "rb"))
    Y_train = Y_train[idxarray]

print Y_train.shape, Y_test.shape
np.random.shuffle(Y_train)

Y_mean = Y_train.mean(axis=0)
Y_std = Y_train.std(axis=0)

Y_train = (Y_train - Y_mean) / Y_std
Y_test = (Y_test - Y_mean) / Y_std


with open("Y.pkl", "wb") as fp:
    sPickle.dump(Y_mean, fp)
    sPickle.dump(Y_std, fp)
    sPickle.dump(Y_train, fp)
    sPickle.dump(Y_test, fp)
