import numpy as np
import random
import logging
import logging.config
class Tag:
    def __init__(self,id, pid, pid2, k1, k2):
        self.logger = logging.getLogger(__name__)
        self.logger.info('[Init] - Initializing Tag')
        self.id = id
        self.pid2 = pid2
        self.k1 = k1
        self.k2 = k2
        
    def receivesABD(self, a, b, d):
        self.a = a
        self.b = b
        self.d = d
    
    def calculateN1N2(self): # n1 = A XOR (pid2 & k1 & k2)
        self.x1 = self.pid2 & self.k1 & self.k2
        self.n1 = self.a ^ self.x1

        self.x2 = np.uint32(~self.pid2) & self.k2 & self.k1
        self.n2 = self.b ^ self.x2
    
    def checkN1N2(self): # K1∧n2 xor ⊕(K2∧n2)
        if self.d != ((self.k1 & self.n2) ^(self.k2 & self.n1)):
            raise Exception("Failed Tag at check n1-n2")


    def generateE(self): # (K1 xor n1 xor PID) xor (k2 ^ n2)
        """print(((self.k1 ^ self.n1 ^ self.id) ^(self.k2 & self.n2)))"""
        return ((self.k1 ^ self.n1 ^ self.id) ^(self.k2 & self.n2))
    

    def generateF(self): # (K1 and n1) xor (K2 and n2)
        """print((self.k1 & self.n1) ^ (self.k2 & self.n2))"""
        return ((self.k1 & self.n1) ^ (self.k2 & self.n2))

    def recalculatePseudonim(self): # (K1 and n1) xor (K2 and n2)
        self.pid = self.pid2
        self.pid2 = self.pid2 ^ self.n1 ^ self.n2
        return 0