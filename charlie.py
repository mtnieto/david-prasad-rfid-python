import numpy as np
import random
import logging
import logging.config
import statistics
import matplotlib.pyplot as plt
class Charlie:
    def __init__(self, id, k1, k2, loop):
        self.logger = logging.getLogger(__name__)
        self.logger.info('[Init] - Initializing Charlie')
        self.L = 32
        self.id = id
        self.k1 = k1
        self.k2 = k2
        self.loop = loop

        self.k1_list = [[] for i in range(self.L)]
        self.k1_estimation = 0
        self.k1_estimation_list = []

        self.k2_list = [[] for i in range(self.L)]
        self.k2_estimation = 0
        self.k2_estimation_list = []
        self.id_list = [[] for i in range(self.L)]
        self.id_estimation = 0
        
        self.distance_vector_k1 = []
        self.distance_vector_k2 = []
        self.distance_vector_id = []
        
    def receivesABD(self, a, b, d):
        self.a = a
        self.b = b
        self.d = d
    
    def receivesEF(self, e, f):
        self.e = e
        self.f = f

    def computeAproximation(self, l):
        self.k1Estimation(l)
        self.k2Estimation(l)
        self.idEstimation(l)

    def computeCombinations(self):
     self.combinations = [int(self.a), int(self.b),int(self.d),int(self.e),int(self.f),int(self.a ^ self.b),
        int(self.a ^ self.d),int(self.a ^ self.e),int(self.a ^ self.f),int(self.b ^ self.d),int(self.b ^ self.e),int(self.b ^ self.f),int(self.d ^ self.e),
        int(self.d ^ self.f),int(self.e ^ self.f), int(self.a ^ self.b ^ self.d),int(self.a ^ self.b ^ self.e), int(self.a ^ self.b ^ self.f),
        int(self.a ^ self.d ^ self.f), int(self.a ^ self.d ^ self.f), int(self.a ^ self.e ^ self.f), 
        int( self.b ^ self.d ^ self.e) ,int(self.b ^ self.d ^ self.f), int(self.b ^ self.e ^ self.f),
        int( self.d ^ self.e ^ self.f) ,int(self.a ^ self.b ^ self.d ^ self.e), int(self.a ^ self.b ^ self.d ^ self.f),
        int(self.a ^ self.b ^ self.e ^ self.f), int(self.a ^ self.d ^ self.e ^ self.f), int(self.b ^ self.d ^ self.e ^ self.f),
        int( self.a ^ self.b ^ self.d ^ self.e ^ self.f)]

    def k1Estimation(self,l):
        output = "K1 estimation:"
        self.k1_estimation = 0 
    
        operations = [int(self.d), int(self.f), int(self.a ^ self.d), int(self.a ^ self.b ^ self.f), int(np.uint32(~(self.b ^ self.d))), int(self.b ^ self.f), int(self.a ^ self.b ^ self.d)]
        for i in range(self.L):
            for j in range(len(operations)):
                aux = int(operations[j]/int(2**i))
                value = aux % 2
                self.k1_list[i].append(value)
                
            self.k1_estimation += int(statistics.median(self.k1_list[i])) * 2**i

        for j in range(len(self.combinations)):
            result = self.hammingDistance(self.combinations[j],self.k1)
            self.distance_vector_k1.append(result)

        self.k1_estimation_list.append(self.k1_estimation)
        if (self.loop-1) ==  l:
            print("K1 value:     ", f'{self.k1:032b}')
            print(output, f'{self.k1_estimation:032b}')

    def k2Estimation(self, l):
        output = "K2 estimation:"
        self.k2_estimation = 0 
        operations = [int(self.d), int(self.f), int(np.uint32(~(self.a ^ self.d))), int(self.a ^ self.f),  int(self.b ^ self.d),int(np.uint32(~(self.b ^ self.f))), int(self.a ^ self.b ^ self.f), int(self.a ^ self.b ^ self.d)]
        for i in range(self.L):
            for j in range(len(operations)):
                aux = int(operations[j]/int(2**i))
                value = aux % 2
                self.k2_list[i].append(value)
            self.k2_estimation += int(statistics.median(self.k2_list[i])) * 2**i
        
        for j in range(len(self.combinations)):
            result = self.hammingDistance(self.combinations[j],self.k2)
            self.distance_vector_k2.append(result)

        self.k2_estimation_list.append(self.k2_estimation)
        if (self.loop-1) ==  l:
            print("K2 value:     ", f'{self.k2:032b}')
            print(output, f'{self.k2_estimation:032b}')
            

    def hammingDistance(self,a,b):
        res = 0
        for i in range(self.L):
            aux = int((a ^ b )/int(2**i))
            value = aux % 2
            res += value
            
        return res
    
    def printPlots(self):
        k1_distances = []
        for i in range(self.loop):
            k1_distances.append(self.hammingDistance(self.k1, self.k1_estimation_list[i]))
        plt.plot(range(self.loop),k1_distances)
        plt.show()


    def idEstimation(self, l):
        output = "ID estimation:"
        self.id_estimation = 0 
        operations = [int(np.uint32(~(self.e ^ self.f))), int(self.a ^ self.b ^ self.e),  int(self.a ^ self.d ^ self.e), int(self.a ^ self.e ^ self.f),
        int(self.b ^ self.d ^ self.e), int(self.d ^ self.e ^ self.f), int(np.uint32(~(self.a ^ self.b ^ self.d ^ self.e))),
        int(self.a ^ self.d ^ self.e ^ self.f), int(np.uint32(~(self.b ^ self.d ^ self.e ^ self.f)))]
        for i in range(self.L):
            for j in range(len(operations)):
                aux = int(operations[j]/int(2**i))
                value = aux % 2
                self.id_list[i].append(value)
            self.id_estimation += int(statistics.median(self.id_list[i])) * 2**i 
        
        for j in range(len(self.combinations)):
            result = self.hammingDistance(self.combinations[j],self.id)
            self.distance_vector_id.append(result)

        if (self.loop-1) ==  l:
            print("ID value:     ", f'{self.id:032b}')
            print(output, f'{self.id_estimation:032b}')

    def rotl(self, num, bits):
        firstBits = int(num / (2**(self.L-bits)))
        lastBits = num & (2**(self.L-bits)-1)
        newBits = int(lastBits*(2**(bits))) + firstBits
        return newBits

    def rotr(self, num, bits):
        lastBits = num & (2**bits-1)
        firstBits = int(num/2**bits)
        newBits = int(lastBits*(2**(self.L-bits))) + firstBits
        return newBits
