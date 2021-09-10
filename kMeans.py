##############################################################
# Vinod Rufus Motani
# Robert Piskule
# 09/07/2021
# DATA-51100: Statistical Programming
# Fall 2021
# Programming Assignment 2 - k-Means Clustering
##############################################################

import sys
import math

inputDatafile="prog2-input-data.txt"
outputDatafile="prog2-output-data.txt"

class Logger:
    level="none"

    @staticmethod
    def print(*argv):
        argv = [str(a) for a in argv]
        s = ''
        for a in argv:
            s += a
        print(s)
            
    @staticmethod
    def error(*argv):
        if (Logger.level == "error" or Logger.level == "info" or Logger.level == "debug"):        
            Logger.print("ERROR:",*argv)
    
    @staticmethod
    def info(*argv):
        if (Logger.level == "info" or Logger.level == "debug"):
            Logger.print("INFO :",*argv)            
        
    @staticmethod
    def debug(*argv):
        if (Logger.level == "debug"):
            Logger.print("DEBUG:",*argv)
    
class kMeans:
    def __init__(self,k,maxIterations = 100):
        # 1. Pick k, the number of clusters (input)
        self.k = k
        self.currentIteration = 0
        self.maxIterations = maxIterations
        self.assignments = []
        self.centroids = []
        self.data = []

    def fit(self,data):
        Logger.debug(data)
        
        centroids = self.initializeClusters(data)
        Logger.debug("Centroids - ",centroids)
        assignments = self.assignPointsToCluster(centroids,data)
        Logger.debug("Assignments - ",assignments)

        iterations = 1
        while (True):
            print("Iteration ",iterations)
            print(self.dictToStr(self.toCentroidDict(centroids,assignments,data)))
            print("")
            Logger.info(self.toCentroidDict(centroids,assignments,data))            
            lastCentroids = centroids.copy()
            
            # After all points are assigned, update the locations of
            # centroids of the k clusters
            centroids = self.updateCentroids(centroids,data,assignments)
            Logger.debug("Centroids - ",centroids)

            converged = True
            for i,*_ in enumerate(centroids):
                Logger.debug("Comparing:",centroids[i]," to ",lastCentroids[i])
                if (not(math.isclose(centroids[i],lastCentroids[i]))):
                    converged=False

            # Reassign all points to their closest centroid. This
            # sometimes moves points between clusters
            assignments = self.assignPointsToCluster(centroids,data)
            Logger.debug("Assignments - ",assignments)

            if (converged == True):
                break
            
            iterations += 1
            if (self.maxIterations != None
                and iterations > self.maxIterations):
                break

        self.assignments=assignments
        self.centroids=centroids
        self.data=data

    def __str__(self):
        string=""
        for i,d in enumerate(self.data):
            string += "Point " + str(d) + " in cluster " + str(self.assignments[i]) + "\n"
        return string
                
    def initializeClusters(self,data):
        """
        Initialize clusters by picking one centroid per cluster
        For this assignment you can pick the first k points as
        the initial centroids for each corresponding cluster
        """
        return data[0:self.k]

    def assignPointsToCluster(self,centroids,data):
        """
        For each point, place it in the cluster whose current
        centroid it is nearest
        """
        assignments = [0] * len(data)        
        for i,point in enumerate(data):
            bestCentroid=0
            bestCentroidDistance=None
            for j,centroid in enumerate(centroids):
                trialDistance = self.distance(point,centroid)
                if (bestCentroidDistance == None):
                    bestCentroid=j
                    bestCentroidDistance=trialDistance
                elif (bestCentroidDistance >= trialDistance):
                    bestCentroid=j
                    bestCentroidDistance=trialDistance
            assignments[i]=bestCentroid
        return assignments

    def distance(self,a,b):
        return math.sqrt((a-b)**2)
        # term1 = (a[0]-b[0])**2
        # term2 = (a[1]-b[1])**2
        # return sqrt(term1+term2)

    def updateCentroids(self,centroids,data,assignments):
        # centroids = [0] * len(centroids)
        calculators = [OnlineCalculator() for c in centroids]
        for i,d in enumerate(data):
            c = assignments[i]
            centroids[c] = calculators[c].calculate(d)[0]
        return centroids

    def toCentroidDict(self,centroids,assignments,data):
        Logger.info(centroids)
        Logger.info(assignments)
        Logger.info(data)
        
        centroidsDict = {}

        for i in range(len(centroids)):
            centroidsDict[i] = []
            for j in range(len(assignments)):
                Logger.debug(i," ",j," ",centroids[i]," ",assignments[j])
                if i == assignments[j]:
                    centroidsDict[i].append(data[j])
                    
        return centroidsDict

    def dictToStr(self,dictionary):
        string=""
        needNewLine=False
        for k,v in dictionary.items():
            if (needNewLine):
                string += "\n"
            string += str(k) + " " + str(v)
            needNewLine=True
        return string

class OnlineCalculator:
    """A calculator for mean and standard deviation using online algorithm"""
    def __init__(self):
        """Initialize online calculator"""
        # Make sure everything is a float
        self.xbarn = float(0)
        self.xbarnm1 = float(0)
        self.s2n = float(0)
        self.s2nm1 = float(0)
        self.n = float(0)
        self.nm1 = float(0)
        self.nm2 = float(0)

    def calculate(self, xn):
        """Recalculate mean and sd with added value xn"""
        xn = float(xn)

        self.xbarnm1 = self.xbarn
        self.s2nm1 = self.s2n
        self.n = self.n+float(1)
        self.xbarn = self.xbarnm1 + ((xn-self.xbarnm1)/self.n)
        if (self.n > 1):
            # It is less error prone to store these as
            # separate variables
            self.nm2 = self.n-2.0
            self.nm1 = self.n-1.0
            self.s2n = ((self.nm2/self.nm1)*self.s2nm1) + \
                (((xn - self.xbarnm1)**2)/self.n)
        return (self.xbarn,  self.s2n)
        
class UI:
    """Class for presenting to user and receiving input"""
    def __init__(self,inputDatafile,outputDatafile,k=None):
        """Initialize the UI"""
        self.inputDatafile=inputDatafile
        self.outputDatafile=outputDatafile
        self.k=k

    def run(self):
        """Run the main program"""
        print("DATA-51100, Fall 2021")
        print("NAME: Vinod Rufus Motani")        
        print("NAME: Robert Piskule")
        print("PROGRAMMING ASSIGNMENT #2")
        print("")

        while True:
            try:
                if (self.k == None):
                    self.k = int(input("Enter the number of clusters: "))
                print("")                    
                break
            except ValueError:
                # Catch cases where user does not input
                # a number
                print("ERROR: Invalid Input!")
                print("")
                continue
        data = self.getData(self.inputDatafile)
        data = [float(line) for line in data]
        kmeans = kMeans(k=self.k)
        kmeans.fit(data)
        # print(kmeans)
        self.saveData(self.outputDatafile,str(kmeans))
        data = self.getData(self.outputDatafile)
        print("\n".join(data))

    def getData(self,df):
        with open(df) as f:
            lines = f.readlines()
        lines = [line.strip() for line in lines]
        return lines

    def saveData(self,df,data):
        with open(df, 'w') as file:
            file.write(str(data))

        
if __name__ == '__main__':
    if (len(sys.argv) == 2 and sys.argv[1] == "test"):
        del sys.argv[1]
        unittest.main()
    else:
        k=None
        if (len(sys.argv) == 2):
            k=int(sys.argv[1])
        ui = UI(inputDatafile,outputDatafile,k=k)
        ui.run()
