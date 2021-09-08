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

datafile="prog2-input-data.txt"

class kMeans:
    def __init__(self,k,data,maxIterations = 100):
        # 1. Pick k, the number of clusters (input)
        self.k = k
        self.data = data
        self.assignments = [0] * 100
        self.currentIteration = 0
        self.maxIterations = maxIterations

    def run(self):
        # 2. Initialize clusters by picking one centroid per cluster
        # For this assignment you can pick the first k points as
        # the initial centroids for each corresponding cluster
        centroids = self.initializeClusters()

        # 3. For each point, place it in the cluster whose current
        # centroid it is nearest
        self.assignPointsToCluster(centroids)

        converged = False
        iterations = 0
        while (True):
            # 4. After all points are assigned, update the locations of
            # centroids of the k clusters
            centroids = self.updateCentroids(centroids)

            # 5. Reassign all points to their closest centroid. This
            # sometimes moves points between clusters
            self.assignPointsToCluster(centroids)


            if (converged == True):
                break
            
            iterations += 1
            if (self.maxIterations != None
                and iterations > self.maxIterations):
                break

    def initializeClusters(self):
        return self.data[0:self.k]

    def assignPointsToCluster(self,centroids):        
        for i,point in enumerate(self.data):
            bestCentroid=0
            bestCentroidDistance=None
            for j,centroid in enumerate(centroids):
                trialDistance = self.distance(point,centroid)
                if (bestCentroidDistance == None):
                    bestCentroid=j
                    bestCentroidDistance=trialDistance
                elif (bestCentroidDistance > trialDistance):
                    bestCentroid=j
                    bestCentroidDistance=trialDistance
            self.assignments[i]=bestCentroid

    def distance(self,a,b):
        return math.sqrt((a-b)**2)
        # term1 = (a[0]-b[0])**2
        # term2 = (a[1]-b[1])**2
        # return sqrt(term1+term2)

    def updateCentroids(self,centroids):
        return centroids

    
class UI:
    """Class for presenting to user and receiving input"""
    def __init__(self,datafile,k=None):
        """Initialize the UI"""
        self.datafile=datafile
        self.k=k

    def run(self):
        """Run the main program"""
        print("DATA-51100,  Fall 2021")
        print("Vinod Rufus Motani")        
        print("Robert Piskule")
        print("PROGRAMMING ASSIGNMENT #2")
        print("")

        while True:
            try:
                if (self.k == None):
                    self.k = int(input("Enter a number: "))
                break
            except ValueError:
                # Catch cases where user does not input
                # a number
                print("ERROR: Invalid Input!")
                print("")
                continue
        data = self.getData(self.datafile)
        kmeans = kMeans(k=self.k,data=data)
        kmeans.run()

    def getData(self,data):
        with open(data) as f:
            lines = f.readlines()
        lines = [float(line.strip()) for line in lines]
        return lines

        
if __name__ == '__main__':
    if (len(sys.argv) == 2 and sys.argv[1] == "test"):
        del sys.argv[1]
        unittest.main()
    else:
        k=None
        if (len(sys.argv) == 2):
            k=int(sys.argv[1])
        ui = UI(datafile,k=k)
        ui.run()
