#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Dylan @ 2016-04-27 10:38:40

import sPickle
import numpy
from tools import GetFileFromRootDir, getArrayFromPattern
from config import *
import pprint

numpy.random.seed(SEED)
pattern = 'p1^p2-p3+p4=p5/A:a1+a2+a3/B:b1-b2_b3/C:c1_c2+c3/D:d1+d2_d3/E:e1_e2!e3_e4-e5/F:f1_f2#f3_f4@f5_f6|f7_f8/G:g1_g2%g3_g4_g5/H:h1_h2/I:i1-i2@i3+i4&i5-i6|i7+i8/J:j1_j2/K:k1+k2-k3'


featdict = dict()
feattypedict = dict()
featnamearray = []
if __name__ == '__main__':

    """
    featnamearray=getArrayFromPattern(pattern)
    fp_feattype=open("feat.type","w")
    for x in featnamearray:
        fp_feattype.write("%s %d\n" % (x,1))
    fp_feattype.close()
    """
    with open("scripts/feat.type") as fp:
        for line in fp.readlines():
            if line == "":
                break
            featname, feattype = line.strip().split()
            featnamearray.append(featname)
            feattypedict[featname] = int(feattype)

    for featname in featnamearray:
        featdict[featname] = dict()

    labfiles = GetFileFromRootDir("./frame", "lab")
    for file in labfiles:
        print file
        with open(file) as fp:
            for line in fp.readlines():
                lines = line.strip().split()
                if(len(lines) < 3):
                    break
                label = lines[0]
                dataarray = getArrayFromPattern(label)

                for x in xrange(len(dataarray)):
                    featdict[featnamearray[x]][dataarray[x]] = 1

    input_dim_v = 0
    for featname, featvaluedict in featdict.items():
        i = 0
        flag = 0
        if feattypedict[featname] != 1:
            continue
        for key in sorted(featvaluedict.keys()):
            if key != 'xx':
                featvaluedict[key] = i
                i += 1
            else:
                flag = 1
        if flag == 1:
            featvaluedict['xx'] = i
            i += 1
        input_dim_v += i 

    print "input vector dimension: %d" % input_dim_v
    # pprint.pprint(featdict)

    """
    save the dictionary information
    """
    output = open('featdict.pkl', 'wb')
    sPickle.dump((featnamearray, feattypedict, featdict), output)
    output.close()
