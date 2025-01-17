#!/usr/bin/python

from collections import namedtuple
import time
import sys
import numpy as np
import operator


class Edge:
    def __init__(self, origin=None, destination=None):
        self.origin = origin 
        self.destination = destination 
        self.weight = 0

    def __repr__(self):
        return "edge: {0} {1} {2}".format(self.origin, self.destination, self.weight)
        

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight = 0
        self.pageIndex = 0

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)


edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport
OutAir = []  # list of airport outs
PageRank = []


def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return v
    return v / norm


def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r", encoding="utf8")
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5:
                raise Exception('not an IATA code')
            a.name = temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code = temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            a.pageIndex = cont
            cont += 1
            airportList.append(a.code)
            airportHash[a.code] = a
    airportsTxt.close()
    print("There were {0} Airports with IATA code".format(cont))


def readRoutes(fd):
    print("Reading Routes file from {0}".format(fd))
    routesTxt = open(fd, "r")
    cont = 0
    for line in routesTxt.readlines():
        try:
            temp = line.split(',')
            if len(temp[2]) != 3 or len(temp[4]) != 3:
                raise Exception('not an IATA code')
            IATAori = temp[2]
            IATAdes = temp[4]
        except Exception as inst:
            print("key ex")
            continue
        else:
            cont += 1
            try:
                if IATAori in airportList and IATAdes in airportList:
                    edgeHash[IATAori, IATAdes] += 1
                    airportHash[IATAdes].routes.append(IATAori)
                    airportHash[IATAori].outweight += 1
            except KeyError as e:
                edgeHash[IATAori, IATAdes] = 1
                airportHash[IATAdes].routes.append(IATAori)
                airportHash[IATAori].outweight += 1
    routesTxt.close()
    print("There were {0} Routes with IATA code".format(cont))


def computePageRanks():
    n = len(airportList)
    P = np.full(n, 1/n)
    L = 0.9
    diff = 1
    diff2 = 100
    iterations = 0
    while abs(diff - diff2) > 0.000001:
        Q = np.zeros(n)
        diff2 = diff
        for i in airportList:
            sum = 0
            airportHash[i].routes = list(dict.fromkeys(airportHash[i].routes))  # Eliminar repetits
            for ori in airportHash[i].routes:
                try:
                    sum += P[airportHash[ori].pageIndex] * edgeHash[ori, i] / airportHash[ori].outweight
                except KeyError as e:
                    print("excepcio")
                    continue
            Q[airportHash[i].pageIndex] = L * sum + (1 - L) / n
        Q = Q / np.sum(Q)
        diff = np.mean(np.absolute(P - Q))
        P = Q
        iterations += 1
    global PageRank
    PageRank = P
    return iterations


def outputPageRanks():
    res = dict()
    count = 1
    for a in airportList:
        res[airportHash[a].name] = PageRank[airportHash[a].pageIndex]
    sort = {k: v for k, v in reversed(sorted(res.items(), key=lambda x: x[1]))}  # Ordena per PageRank
    for ap in sort:
        print(count, ". ", ap, "has PageRank:", sort[ap])
        count += 1


def main(argv=None):
    readAirports("airports.txt")
    readRoutes("routes.txt")
    time1 = time.time()
    iterations = computePageRanks()
    time2 = time.time()
    outputPageRanks()
    print("#Iterations:", iterations)
    print("Time of computePageRanks():", time2-time1)


if __name__ == "__main__":
    sys.exit(main())
