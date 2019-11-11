#!/usr/bin/python

from collections import namedtuple
import time
import sys

class Edge:
    def __init__ (self, origin=None, destination=None):
        self.origin = origin 
        self.destination = destination 
        self.weight = 0

    def __repr__(self):
        return "edge: {0} {1}".format(self.origin, self.weight)
        

class Airport:
    def __init__ (self, iden=None, name=None):
        self.code = iden
        self.name = name
        self.routes = []
        self.routeHash = dict()
        self.outweight =    # write appropriate value

    def __repr__(self):
        return "{0}\t{2}\t{1}".format(self.code, self.name, self.pageIndex)

edgeList = [] # list of Edge
edgeHash = dict() # hash of edge to ease the match
airportList = [] # list of Airport
airportHash = dict() # hash key IATA code -> Airport

def readAirports(fd):
    print("Reading Airport file from {0}".format(fd))
    airportsTxt = open(fd, "r");
    cont = 0
    for line in airportsTxt.readlines():
        a = Airport()
        try:
            temp = line.split(',')
            if len(temp[4]) != 5 :
                raise Exception('not an IATA code')
            a.name=temp[1][1:-1] + ", " + temp[3][1:-1]
            a.code=temp[4][1:-1]
        except Exception as inst:
            pass
        else:
            cont += 1
            airportList.append(a)
            airportHash[a.code] = a
    airportsTxt.close()
    print("There were {0} Airports with IATA code".format(cont))


def readRoutes(fd):
    print("Reading Routes file from {0}".format(fd))
    routesTxt = open(fd, "r");
    cont = 0
    for line in routesTxt.readlines():
    	try:
    		temp = line.split(',')
            if len(temp[2]) != 5 or len(temp[3]) != 5:
                raise Exception('not an IATA code')
            IATAori = temp[2][1:-1]
            IATAdes = temp[3][1:-1]
        except Exception as inst:
            pass
        else:
        	cont += 1
        	edgeHash[(IATAori, IATAdes)] += 1
    routesTxt.close()
    print("There were {0} Routes with IATA code".format(cont))
        	

def computePageRanks():
    # write your code

def outputPageRanks():
    # write your code

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