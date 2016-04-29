import numpy as np
import os
from tools import GetFileFromRootDir


lf0files=GetFileFromRootDir("lf0","lf0")
#os.mkdir("lf0_inter")
for file in lf0files:
    lf0s=np.fromfile(file,dtype=np.float32)
    lf0s=np.append(lf0s,0)
    vflag=1
    lf0_inter=[]
    uv_flag=[]
    for i in xrange(len(lf0s)):
        if lf0s[i]==-1e10:
            uv_flag.append(0)
            if vflag==1:
                start=i
                if i==0:
                    startvalue=0
                else:
                    startvalue=lf0s[i-1]

            vflag=0
        else:
            uv_flag.append(1)
            if vflag==0:
                end=i
                endvalue=lf0s[i]
                array=np.linspace(startvalue,endvalue,end-start+2)
                lf0_inter+=list(array[1:-1])
            lf0_inter.append(lf0s[i])
            vflag=1
    lf0_inter.pop()
    uv_flag.pop()
    file_inter="lf0_inter/"+os.path.split(file)[1]
    file_uv=file_inter+".uv"
    np.array(lf0_inter,dtype=np.float32).tofile(file_inter)
    np.array(uv_flag,dtype=np.int).tofile(file_uv," ")









