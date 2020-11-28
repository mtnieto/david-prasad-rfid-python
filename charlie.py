import numpy as np
import random
import logging
import logging.config
import statistics
class Charlie:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info('[Init] - Initializing Charlie')
        self.L = 8
        self.k1_list = [[] for i in range(self.L)]
        self.k1_estimation = 0
        self.k2_list = [[] for i in range(self.L)]
        self.k2_estimation = 0
        
    def receivesABD(self, a, b, d):
        self.a = a
        self.b = b
        self.d = d
    
    def receivesEF(self, e, f):
        self.e = e
        self.f = f

    def computeAproximation(self):
        self.k1Estimation()
        self.k2Estimation()

    
    def k1Estimation(self):
        output = "Best estimation of k1 is:"
        self.k1_estimation = 0 
        print(self.d, self.f, self.a ^ self.d) # , 
        operations = [int(self.d), int(self.f), int(self.a ^ self.d), int(self.a ^ self.b ^ self.f), int(np.uint8(~(self.b ^ self.d))), int(self.b ^ self.f), int(self.a ^ self.b ^ self.d)]
        for i in range(self.L):
            for j in range(len(operations)):
                aux = int(operations[j]/int(2**i))
                value = aux % 2
                self.k1_list[i].append(value)
                if i == 0:
                    print(f'{operations[j]:08b}')
            self.k1_estimation += int(statistics.median(self.k1_list[i])) * 2**i
        
        # for i in range(self.L):
        #     print("List of bins of position",i,"is:",self.k1_list[i])
        #     print("Sum of numbers:",sum(self.k1_list[i]))
            
        print("----------------")

        print(output, f'{self.k1_estimation:08b}')

    def k2Estimation(self):
        output = "Best estimation of k2 is:"
        self.k2_estimation = 0 
        operations = [int(self.d), int(self.f), int(np.uint8(~(self.a ^ self.d))), int(self.a ^ self.f),  int(self.b ^ self.d),int(np.uint8(~(self.b ^ self.f))), int(self.a ^ self.b ^ self.f), int(self.a ^ self.b ^ self.d)]
        for i in range(self.L):
            for j in range(len(operations)):
                aux = int(operations[j]/int(2**i))
                value = aux % 2
                self.k2_list[i].append(value)
                if i == 0:
                    print(f'{operations[j]:08b}')
            self.k2_estimation += int(statistics.median(self.k2_list[i])) * 2**i
        
        # for i in range(self.L):
        #     print("List of bins of position",i,"is:",self.k2_list[i])
        #     print("Sum of numbers:",sum(self.k2_list[i]))
            
        print("----------------")
        print(output, f'{self.k2_estimation:08b}')

