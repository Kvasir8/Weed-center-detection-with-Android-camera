'''dEMONSTRATION of K Means Clustering
Requires : python 2.7.x, Numpy 1.7.1+, Matplotlib, 1.2.1+'''
#import sys
import pylab as plt
import numpy as np
plt.ion()

def E_Dist(x, y):  #Distance calculation
    return np.matmul( (x - y).T , (x - y) )

def kMeans(X, K, maxIters): #K means function definition, iteration numbers = 10
    Assign = []
    Temp = []
    centroids = X[np.random.choice(np.arange(len(X)), K), :] 
    #Centroid normalization 정규분포 랜덤 X개 만큼 0=<x<K=3 범위 값을 갖는 points를 행 단위로 고름, 즉 2D 상의 무작위로 centroids를 잡음
    for i in range(maxIters): 
        
        # Cluster Assignment step (=update assignments)
        for m in range(len(X)): #till X = 530
            for k in range(len(centroids)):
                Temp.append( E_Dist(X[m], centroids[k]) )
            Assign.append(np.argmin(Temp)) #Assignment
            Temp = []   #initialize Temp list values to compare new distance values
            
        C = np.array(Assign)
            
        # Move centroids step (=update means)
        centroids = [X[C == k].mean(axis = 0) for k in range(K)]
        
        #for k in range(len(centroids)):
        #    Assign_order = np.argwhere(Assign == k)
        #    for j in range(len(Assign_order)):
        #        Temp.append(X[Assign_order[j][0]])
            #Temp1 = np.asarray(Temp)
            #Temp1 = Temp.reshape((len(Assign_order),2))
        #    centroids[k] = ( np.nansum(Temp, axis = 0) )/Assign.count(k)
        #    Temp = []
        
        
        Assign = []
        
        show(X, C, np.array(centroids))
    return np.array(centroids) , C

def show(X, C, centroids, keep = False):
    import time
    time.sleep(0.5)
    plt.cla() # Clear axis
    plt.plot(X[C == 0, 0], X[C == 0, 1], '*b',
         X[C == 1, 0], X[C == 1, 1], '*r',
         X[C == 2, 0], X[C == 2, 1], '*g')
    plt.plot(centroids[:,0],centroids[:,1],'*m',markersize=20)
    plt.draw()
    if keep :
        plt.ioff()
        plt.show()

# generate 3 cluster data
# data = np.genfromtxt('data1.csv', delimiter=',')
#m1, cov1 = [9, 8], [[1.5, 2], [1, 2]] #data value float type from 8~9
#m2, cov2 = [5, 13], [[2.5, -1.5], [-1.5, 1.5]]
#m3, cov3 = [3, 7], [[0.25, 0.5], [-0.1, 0.5]]
#data1 = np.random.multivariate_normal(m1, cov1, 250) #normalized variables 1~3
#data2 = np.random.multivariate_normal(m2, cov2, 180) #Draw random samples from a multivariate normal distribution.
#data3 = np.random.multivariate_normal(m3, cov3, 100) #즉, 3개의 cluster를 생성하기 위해 정규분포를 따르는 랜덤한 points들을 생성
#X = np.vstack(   (data1, np.vstack( (data2,data3) )  )   )
#np.random.shuffle(X)
X = [None, None]
#from kMeans import kMeans
def Result(X, K, maxIters):
    centroids, C = kMeans(X, K, maxIters)
    show(X, C, centroids, True)