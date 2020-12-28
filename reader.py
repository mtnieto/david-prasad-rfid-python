import numpy as np
import random
import logging
import logging.config
class Reader():
    def __init__(self,pid, pid2, k1, k2):
        self.logger = logging.getLogger(__name__)
        self.logger.info('[Init] - Initializing Reader')
        self.pid = pid
        self.pid2 = pid2
        self.k1 = k1
        self.k2 = k2
        self.n1 = random.randint(0, pow(2,32))
        self.n2 = random.randint(0, pow(2,32))
        self.L = 32

    def generateA(self): # (PID2 and K1 and K2) xor n
        return (self.pid2 & self.k1 &  self.k2) ^ self.n1

    def generateB(self): # (negado PID2and K2 and K1) xor n2
        return (np.uint32(~self.pid2) & self.k2 & self.k1) ^ self.n2

    def generateD(self): # (K1 and n2) xor (K2 and n1)
        return ((self.k1 & self.n2) ^ self.k2 & self.n1)
    
    def receivesEF(self, e, f):
        rot = self.pid2 % self.L
        self.e = self.rotl(e,rot)
        self.f = f
    
    def getID(self):
        self.y1 = self.k2 ^ self.n2
        self.y2 = self.k1 ^ self.n1
        self.y3 = self.e ^ self.y1
        self.id = self.y3 ^ self.y2

    def checkN1N2(self):
        if self.f != ((self.k1 & self.n1) ^(self.k2 & self.n2)):
            raise Exception("Failed Reader at check n1-n2")

    def updateN1N2(self):
        self.n1 = random.randint(0, pow(2,32)) 
        self.n2 = random.randint(0, pow(2,32))

    def recalculatePseudonim(self): # (K1 and n1) xor (K2 and n2)
        self.pid = self.pid2
        self.pid2 = self.pid2 ^ self.n1 ^ self.n2
        return 0
    
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
