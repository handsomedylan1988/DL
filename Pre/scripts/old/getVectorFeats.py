import os
import re
import sPickle
import numpy


pattern = 'p1^p2-p3+p4=p5/A:a1+a2+a3/B:b1-b2_b3/C:c1_c2+c3/D:d1+d2_d3/E:e1_e2!e3_e4-e5/F:f1_f2#f3_f4@f5_f6|f7_f8/G:g1_g2%g3_g4_g5/H:h1_h2/I:i1-i2@i3+i4&i5-i6|i7+i8/J:j1_j2/K:k1+k2-k3'


def GetFileFromRootDir(dir, ext=None):
    allfiles = []
    needExtFilter=(ext !=None)
    for root, dirs, files in os.walk(dir):
        for filespath in sorted(files):
            filepath=os.path.join(root,filespath)
            extension=os.path.splitext(filepath)[1][1:]
            if needExtFilter and extension in ext:
                allfiles.append(filepath)
            elif not needExtFilter:
                allfiles.append(filepath)
    return allfiles

def getArrayFromPattern(pattern):
    array=[]
    pattern=re.sub(r"\/[A-Z]:",",",pattern)
    array=re.split(r"[^a-z0-9A-Z]",pattern)
    i=0
    while i< len(array):#some feature values may be negative -5
        if array[i]=="":
            array.pop(i)
            array[i]="-"+array[i]
        i+=1
    return array

featdict = dict()
feattypedict=dict()
dataarrays=[]
numberfeatures=[]

if __name__ == '__main__':
    featnamearray=getArrayFromPattern(pattern)
#    fp_feattype=open("feat.type","w")
#    for x in featnamearray:
#        fp_feattype.write("%s %d\n" % (x,1))
#    fp_feattype.close()

    with open("scripts/feat.type") as fp:
        for line in fp.readlines():
            featname,feattype=line.strip().split()
            feattypedict[featname]=int(feattype)


    for featname in featnamearray:
        featdict[featname]=dict()

    labfiles=GetFileFromRootDir("./frame","lab")
    for file in labfiles:
        with open(file) as fp:
            for line in fp.readlines():
                lines=line.strip().split()
                if(len(lines)<3):
                    break
                label=lines[0]
                dataarray=getArrayFromPattern(label)
                dataarrays.append(dataarray)
                for x in xrange(len(dataarray)):
                    featdict[featnamearray[x]][dataarray[x]]=1
                numberfeatures.append(lines[1:])

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

    output=open('featdict.pkl','wb')
    sPickle.dump(featdict , output)
    output.close()




    featurearrays=[]
    for dataarray in dataarrays:
        featurearray=[]
        for x in xrange(len(dataarray)):
            if feattypedict[featnamearray[x]]==1:
                vector=[0 for y in featdict[featnamearray[x]].values()]
                vector[featdict[featnamearray[x]][dataarray[x]]]=1
                featurearray=featurearray+vector
            else :
                pass
        featurearrays.append(featurearray)

    numberfeatures=numpy.array(numberfeatures,dtype=numpy.float32)
    mean=numberfeatures.mean(axis=0)
    std=numberfeatures.std(axis=0)

    numberfeatures=(numberfeatures-mean)/std
    vectorfeatures=numpy.array(featurearrays)

    assert len(numberfeatures)==len(vectorfeatures) 


    allfeatures=numpy.hstack((vectorfeatures,numberfeatures))

    print vectorfeatures.shape
    print allfeatures.shape
    
    output =open('allfeat.pkl','wb')
    sPickle.s_dump(mean,output)
    sPickle.s_dump(std,output)
    sPickle.s_dump(allfeatures,output)
    output.close()
    print "end"

