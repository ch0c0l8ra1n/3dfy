import sys


if(len(sys.argv)<2):
	print ("Usage python3 main.py filename")
	exit()	

import cv2
import numpy as np
import math
import time
import copy
from PIL import Image
import engine
import m_engine



test = cv2.imread(sys.argv[1])

img = test

cv2.imshow("Supplied Image",img)
cv2.waitKey(1)
#img = cv2.resize(test,(200,200))


img_inv = cv2.bitwise_not(img)

img_gray = cv2.cvtColor(img_inv,cv2.COLOR_BGR2GRAY)



ret, thresh = cv2.threshold(img_gray,127,255, 0)
im2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

view_rects = []
views = []
contours_new = []

for i in range(2):
    stuff = [item[0] for item in contours[i]]
    #print ("contour no:{} ".format(i)+str(stuff))
    cnt = contours[i]

    x,y,w,h = cv2.boundingRect(cnt)


    view = copy.deepcopy(img[y:y+h,x:x+w])

    contour_new = [cnt-(x,y)]


    contours_new.append(contour_new)

    views.append(view)

    view_rects.append((x,y,w,h))

    cv2.drawContours(img, [cnt], 0, (0,255,0), 1)


views_T = []

row = []
view_proc = []
views_proc = []

for i in range(2):

    temp = np.transpose(views[i],(1,0,2))

    views_T.append(temp)

    l , h = temp.shape[:2]

    for j in range(h):

        for k in range(l):

            test = cv2.pointPolygonTest(contours_new[i][0], (k,j),False)
            
            if test != -1:
                #print ("1",end="")
                row.append(1)
            else:
                #print ("0",end="")
                row.append(0)    

        view_proc.append(row)
        row = []

    views_proc.append(view_proc)

    view_proc = []

l_v = np.array(views_proc[0])
f_v = np.array(views_proc[1])



h1,l1 =  l_v.shape[:2]

h2,l2 =  f_v.shape[:2]

#print (h1,l1)
#print (h2,l2)

obj_3d = []
strip_0 = []

for i in range(l2):
    strip_0.append(0)

#print(f_v[1])

layer = []

#object building algorithm
print("\n\nBuilding Object...\n\n")
for i in range(l1):
    for j in range(h1):
        if   l_v[j][i] == 0:
            layer.append(strip_0)
        elif l_v[j][i] == 1:
            layer.append(f_v[j])
    
    obj_3d.append(layer)
    layer = []

temp = np.array(obj_3d)[:,::-1,:]

ind = np.transpose(np.where(temp == 1))
print("Total Points = ",len(ind))

l,b,h = temp.shape[:3]


new_ind = []
big = 0

print("\n\nExtracting surface of the object...\n\n")
t1 = time.time()
#surface finding algorithm
for i,j,k in ind:
    if i==0 or i == l-1 or j==0 or j==b-1 or k==0 or k == h-1:
        new_ind.append((i,j,k))

    elif (temp[i+1,j,k]     == 0 or 
          temp[i-1,j,k]     == 0 or 
          temp[i,j+1,k]     == 0 or 
          temp[i,j-1,k]     == 0 or 
          temp[i+1,j+1,k]   == 0 or 
          temp[i+1,j-1,k]   == 0 or 
          temp[i-1,j+1,k]   == 0 or 
          temp[i-1,j-1,k]   == 0 or 
          temp[i+1,j,k+1]   == 0 or 
          temp[i-1,j,k+1]   == 0 or 
          temp[i,j+1,k+1]   == 0 or 
          temp[i,j-1,k+1]   == 0 or 
          temp[i+1,j+1,k+1] == 0 or 
          temp[i+1,j-1,k+1] == 0 or 
          temp[i-1,j+1,k+1] == 0 or 
          temp[i-1,j-1,k+1] == 0 or 
          temp[i+1,j,k-1]   == 0 or 
          temp[i-1,j,k-1]   == 0 or 
          temp[i,j+1,k-1]   == 0 or 
          temp[i,j-1,k-1]   == 0 or 
          temp[i+1,j+1,k-1] == 0 or 
          temp[i+1,j-1,k-1] == 0 or 
          temp[i-1,j+1,k-1] == 0 or 
          temp[i-1,j-1,k-1] == 0 or  
          temp[i,j,k+1]     == 0 or 
          temp[i,j,k-1]     == 0):
        new_ind.append((i,j,k))

new_ind_np = np.array(new_ind)
print("Surface Points = "+str(len(new_ind_np)))

print("Reduction percentage = ",100*(1-len(new_ind_np)/len(ind)),"%")
print("Time Elapsed = ",time.time()-t1)




m_engine.main(new_ind_np,len(obj_3d),len(obj_3d[0]),len(obj_3d[0][0]))


