import random

## Random int random.randint(0, 9)
## Random bin bin(random.randint(0, 7))
import numpy as np



class World:
    
    def __init__(self): #añadimso numero de rondas?
        self.reader = self.Reader(1,2,6,5) # Reciben lo mismo tag y reader al init
        self.tag = self.Tag(2,1,2,6,5)
        #to do , create loop to simulate the rounds
        # Reader starts with a,b,d

        self.a = self.Reader.generateA(self.reader)
        self.b = self.Reader.generateB(self.reader)
        self.d = self.Reader.generateD(self.reader)
        # Reader -> Tag
        self.Tag.receivesABD(self.tag, self.a,self.b,self.d) # receibes A, B, D in order to get n1 and n2 and then check it
        self.Tag.calculateN1N2(self.tag) # Calculate n1 and n2 with A, B
        self.Tag.checkN1N2(self.tag) # Check result with D
        self.e = self.Tag.generateE(self.tag)
        self.f = self.Tag.generateF(self.tag)
        # Tag -> Reader
        self.Reader.receivesEF(self.reader, self.e,self.f)
        self.Reader.getID(self.reader) # Calculate ID with E
        self.Reader.checkN1N2(self.reader) # Check with F
        # Round finished, recalculating pseudonim pid and pid2
        self.Reader.recalculatePseudonim(self.reader)
        self.Tag.recalculatePseudonim(self.tag)

        

    

    class Tag:
        def __init__(self,id, pid, pid2, k1, k2):
            self.id = id
            self.pid = pid
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

            self.x2 = np.uint16(~self.pid2) & self.k2 & self.k1
            self.n2 = self.b ^ self.x2
        
        def checkN1N2(self): # K1∧n2 xor ⊕(K2∧n2)
            if self.d != ((self.k1 & self.n2) ^(self.k2 & self.n1)):
                raise Exception("Failed Tag at check n1-n2")


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
        def __init__(self,pid, pid2, k1, k2):
            self.pid = pid
            self.pid2 = pid2
            self.k1 = k1
            self.k2 = k2
            self.n1 = random.randint(0, 7)
            self.n2 = random.randint(0, 7)

        def generateA(self): # (PID2 and K1 and K2) xor n
            return (self.pid2 & self.k1 &  self.k2) ^ self.n1

        def generateB(self): # (negado PID2and K2 and K1) xor n2
            return (np.uint16(~self.pid2) & self.k2 & self.k1) ^ self.n2

        def generateD(self): # (K1 and n2) xor (K2 and n1)
            return ((self.k1 & self.n2) ^ self.k2 & self.n1)
        
        def receivesEF(self, e, f):
            self.e = e
            self.f = f
        
        def getID(self):
            self.y1 = self.k2 ^ self.n2
            self.y2 = self.k1 ^ self.n1
            self.y3 = self.e ^ self.y1
            self.id = self.y3 ^ self.y2

        def checkN1N2(self):
            if self.f != ((self.k1 & self.n1) ^(self.k2 & self.n2)):
                raise Exception("Failed Reader at check n1-n2")


        def recalculatePseudonim(self): # (K1 and n1) xor (K2 and n2)
            self.pid = self.pid2
            self.pid2 = self.pid2 ^ self.n1 ^ self.n2
            return 0
          

if __name__ == "__main__":
    world = World()
 
    # import pdb 
    # pdb.set_trace()