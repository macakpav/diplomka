
import csv
import numpy as np
from math import *

targetUy=[ 45.31522570142732, 50.905965298005164, 62.526295500526324, 68.5974669056153, 74.87391857743567, 81.38236795746637 ] 
angles=[17.703084218392917, 19.703084218392917, 23.703084218392917, 25.703084218392938, 27.703084218392917, 29.703084218392917]
#angles=[ 17.45819002769148, 19.458190027691480, 23.458190027691480, 25.4581900276915, 27.45819002769148, 29.45819002769148 ]
targetFy=[ 9.115034013352567, 8.6523658390505691, 7.6858512587729884, 7.17362135080829, 6.650746461757007, 6.100292287899188 ]
angNames=[17, 19, 23, 25, 27, 29]
methodNames=["Uy", "Fy"]

# SA
# Ux0=1.4408807664587323e+02
# Uy0=56.636378742932301
# alpha20=21.458190027691480
# Fy0=8.1762779628202242
# KO
Ux0=1.440720603672e+02
Uy0=57.34221986548
alpha20=21.703084218392917
Fy0=8.116824583140

UyConv=np.empty((51,7))
UyConvAlpha=np.empty((51,7))
FyConv=np.empty((51,7))
FyConvAlpha=np.empty((51,7))
UyPost=np.empty((51,7))
FyPost=np.empty((51,7))

for i in range(51):
    UyConv[i,0]=i
    UyConvAlpha[i,0]=i
    FyConv[i,0]=i
    FyConvAlpha[i,0]=i
    UyPost[i,0]=i
    FyPost[i,0]=i

for k in range(len(methodNames)):
    method=methodNames[k]
    for j in range(len(angNames)):
        angleName=angNames[j]
        tAng=angles[j]
        tUy=targetUy[j]
        tFy=targetFy[j]

        filename="angle"+str(angleName)+"_"+method
        data=np.empty((51,8))
        with open(filename+".csv") as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            next(reader) #skip first line
            for row in reader: #loop over time
                time=int(row[0])
                data[time,0]=time
                for i in range(1,5):
                    data[time,i]=float(row[i])

                #interpret cols for current time
                Ux=data[time,1]
                Uy=data[time,2]
                Fx=data[time,3]
                Fy=data[time,4]
                Jval=0

                #alpha convergence
                alph2=np.rad2deg(atan(Uy/Ux))
                data[time,7] = fabs(alph2-tAng)/fabs(alpha20)

                #Uy/Fy convergence
                if k==0:
                    data[time,6] = fabs(Uy-tUy)/fabs(Uy0)
                    UyConv[time,j+1]=data[time,6]
                    UyConvAlpha[time,j+1]=data[time,7]
                    UyPost[time,j+1]=Jval-Uy
                else:
                    data[time,6] = fabs(Fy-tFy)/fabs(Fy0)
                    FyConv[time,j+1]=data[time,6]
                    FyConvAlpha[time,j+1]=data[time,7]
                    FyPost[time,j+1]=Jval-Fy

        
        #np.savetxt(filename+".csv", data, delimiter=" ", header="Iter Ux Uy Fx Fy TargetVal "+method+"conv alphaConv")

# Uy convergence compar
np.savetxt("UyConvergence.dat", UyConv, delimiter=" ", header="Iter a17 a19 a23 a25 a27 a29")
np.savetxt("UyConvergenceAlpha.dat", UyConvAlpha, delimiter=" ", header="Iter a17 a19 a23 a25 a27 a29")

# Fy convergence compar
np.savetxt("FyConvergence.dat", FyConv, delimiter=" ", header="Iter a17 a19 a23 a25 a27 a29")
np.savetxt("FyConvergenceAlpha.dat", FyConvAlpha, delimiter=" ", header="Iter a17 a19 a23 a25 a27 a29")

# Fy postProcess compar
np.savetxt("UyPost.dat", UyPost, delimiter=" ", header="Iter a17 a19 a23 a25 a27 a29")
np.savetxt("FyPost.dat", FyPost, delimiter=", ", header="Iter a17 a19 a23 a25 a27 a29")


# compare some case of Uy vs Fy


# some k-Omegga SST validation
        