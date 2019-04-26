import psycopg2
import csv
import numpy
from math import radians, cos, sin, asin, sqrt
#importing data
file =  open('2014_02_chicago.twt','r')
dic = {}
for num, line in enumerate(file):
    list = []
    list = line.split('\x01')
    dic[num] = list
#select coordinates and text data
coor = {}
for key, value in dic.items():
    try:
        list = []
        list.append(dic[key][0])
        list2 = dic[key][2].split(',')
        list3 = dic[key][6]
        list4 = dic[key][1]
        for item in list2:
            list.append(item)
        list.append(list3)
        list.append(list4)
        coor[key] = list
    except:
        IndexError
#dataset demo
D = []
for i in range(6000):
    a = []
    a.append(float(coor[i][2]))
    a.append(float(coor[i][1]))
    D.append(tuple(a))

#dbscan algorithm

#main function
def DBscan(D, eps, MinPts):
    labels = [0]*len(D)
    C = 0
    
    for P in range(0, len(D)):
        if not (labels[P] == 0):
            continue
        NeighborPts = regionQuery(D, P, eps)
        if len(NeighborPts) < MinPts:
            labels[P] = -1
        else:
            C += 1
            growCluster(D, labels, P, NeighborPts, C, eps, MinPts)
    return labels
    
#grow every cluster and label them by increased C
def growCluster(D, labels, P, NeighborPts, C, eps, MinPts):
    labels[P] = C
    i = 0
    while i < len(NeighborPts):
        Pn = NeighborPts[i]
        if labels[Pn] == -1:
            labels[Pn] = C
        elif labels[Pn] == 0:
            labels[Pn] = C
            
            PnNeighborPts = regionQuery(D, Pn, eps)
            if (len(PnNeighborPts)) >= MinPts:
                NeighborPts = NeighborPts + PnNeighborPts
        i += 1
        
#find every point's neighber and judge whether their distance < eps
def regionQuery(D, P, eps):
    neighbors = []
    for Pn in range(0, len(D)):
#         if numpy.sqrt(numpy.square((D[P][0] - D[P][1])) + numpy.square((D[Pn][0] - D[Pn][1]))) < eps:
#             neighbors.append(Pn)
        lon1, lat1, lon2, lat2 = map(radians, [D[Pn][0], D[Pn][1], D[P][0], D[P][1]])

        dlon = lon2 - lon1 
        dlat = lat2 - lat1 
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a)) 
        r = 6371
        distance = r * c * 10000
        if distance < eps:
            neighbors.append(Pn)
    return neighbors
clustering = DBscan(D,10000,20)

#combine coordinates and their clustering label
DLabel = []
for i in range(len(clustering)):
    a = []
    a.append(float(coor[i][2]))
    a.append(float(coor[i][1]))
    a.append(clustering[i])
    DLabel.append(tuple(a))
print(sorted(DLabel, key = lambda y: y[2]))
### the result is each coordinates with its label that represents which cluster it belongs to.
### label:-1 means noisy point
