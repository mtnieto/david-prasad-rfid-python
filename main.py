import random

## Random int random.randint(0, 9)
## Random bin bin(random.randint(0, 7))
import numpy as np



class World:
    
    def __init__(self): #añadimso numero de rondas?
        self.channel = []
        #self.reader = self.Reader(2,1,2,6, 5) # Reciben lo mismo tag y reader al init
        self.tag = self.Tag(2,1,2,6,5)
        self.tag.generateF()

        

    

    class Tag:
        def __init__(self,id, pid, pid2, k1, k2):
            self.id = id
            self.pid = pid
            self.pid2 = pid2
            self.k1 = k1
            self.k2 = k2
            self.n1 = 2
            self.n2 = 2

        def generateE(self): # (K1 xor n1 xor PID) xor (k2 ^ n2)
            print(((self.k1 ^ self.n1 ^ self.pid) ^(self.k2 & self.n2)))
            return ((self.k1 ^ self.n1 ^ self.pid) ^(self.k2 & self.n2))

        def generateF(self): # (K1 and n1) xor (K2 and n2)
            print((self.k1 & self.n1) ^ (self.k2 & self.n2))
            return ((self.k1 & self.n1) ^ (self.k2 & self.n2))

        def recalculatePseudonim(self): # (K1 and n1) xor (K2 and n2)
            self.pid = self.pid2
            self.pid2 = self.pid2 ^ self.n1 ^ self.n2
            return 0



    class Reader():
        def __init__(self,pid, pid2, k1, k2, channel):
            self.pid = pid
            self.pid2 = pid2
            self.k1 = k1
            self.k2 = k2
            self.channel = channel
            self.n1 = random.randint(0, 7) # estos son compartidos no iria en el world?
            self.n2 = random.randint(0, 7)

        def generateA(self): # (PID2 and K1 and K2) xor n
            print(self.pid2 & self.k1 &  self.k2) ^ self.n1
            return (self.pid2 & self.k1 &  self.k2) ^ self.n1

        def generateB(self): # (negado PID2and K2 and K1) xor n2
            return (np.uint16(~self.pid2) & self.k2 & self.k1) ^ self.n2

        def generateD(self): # (K1 and n2) xor (K2 and n1)
            #TODO
            return ((self.k1 & self.n2) ^ self.k2 & self.n1)

        def recalculatePseudonim(self): # (K1 and n1) xor (K2 and n2)
            self.pid = self.pid2
            self.pid2 = self.pid2 ^ self.n1 ^ self.n2
            return 0

        def sendMessage(self): #vamos a usar websockets?
            #TODO
            recomputeRandoms()

          

if __name__ == "__main__":
    world = World()
 
    # import pdb 
    # pdb.set_trace()