#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Dylan @ 2016-04-28 22:09:55

import os
import numpy as np
import sys
sys.path.append("../Pre/scripts/")
from config import *

Y_predict = np.fromfile("Y_predict", dtype=np.float32)
Y_predict = Y_predict.reshape(-1, OUTPUT_DIM)

print Y_predict.shape

Var_floor = np.fromfile("vFloors", sep=' ', dtype=np.float32)
Var_floor = np.tile(Var_floor, len(Y_predict))
Var_floor = Var_floor.reshape(-1, OUTPUT_DIM-1)
print Var_floor.shape

uv = Y_predict[:, OUTPUT_DIM-1]

mgc_pdf = np.hstack((Y_predict[:, 0:(MGC_DIM+1)*3], Var_floor[:, 0:(MGC_DIM+1)*3]))
lf0_pdf = np.hstack((Y_predict[:, (MGC_DIM+1)*3:OUTPUT_DIM-1], Var_floor[:, (MGC_DIM+1)*3:OUTPUT_DIM-1]))

mgc_pdf.tofile("mgc.pdf")
lf0_pdf.tofile("lf0.pdf")

os.system("mlpg -m %d -i 1 -d -0.5 0 0.5 -d 1.0 -2.0 1.0 mgc.pdf >tmp.mgc" % MGC_DIM)
os.system("mlpg -m %d -i 1 -d -0.5 0 0.5 -d 1.0 -2.0 1.0 lf0.pdf >tmp.lf0" % (LF0_DIM-1)) # need to be proved

lf0 = np.fromfile("tmp.lf0", dtype=np.float32)
for x in xrange(len(uv)):
    if uv[x] < 0.5:
        lf0[x] = -1e10

lf0.tofile("tmp.lf0")

os.system("perl scripts/syn.pl scripts/Config.pm tmp")
