#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Dylan @ 2016-04-29 22:54:44

STATENUM=5
MGC_DIM = 34
LF0_DIM = 1

FRAME_LEN = 50000 # ns
INPUT_DIM = 911
OUTPUT_DIM = (MGC_DIM + 1 + LF0_DIM) * 3 +1

nTrain = 493 #first 493 files for training, 10 for testing
SEED = 1337

REMOVE_SIL = True 
