from reader import Reader
from tag import Tag
from charlie import Charlie
import logging
import logging.config
import random
import sys

class World:
    
    def __init__(self, loop): 
        pid = random.randint(0, (pow(2,32)))
        pid2 = random.randint(0, (pow(2,32)))
        k1 = random.randint(0, (pow(2,32)))
        k2 = random.randint(0, (pow(2,32)))
        identificator = random.randint(0, pow(2,32))
        self.loop = loop

        self.reader = Reader(pid,pid2,k1,k2) # Reciben lo mismo tag y reader al init (self,pid, pid2, k1, k2)
        self.tag = Tag(identificator,pid,pid2,k1,k2)  #(self,id, pid, pid2, k1, k2)
        self.charlie = Charlie(identificator, k1, k2, self.loop)
        #to do , create loop to simulate the rounds
        # Reader starts with a,b,d
    def start_simulation(self):
        i = 0
        while i < self.loop:
            self.a = self.reader.generateA()
            self.b = self.reader.generateB()
            self.d = self.reader.generateD()
            # Reader -> Charlie
            self.charlie.receivesABD(self.a,self.b,self.d)
            # Reader -> Tag
            self.tag.receivesABD(self.a,self.b,self.d) # receibes A, B, D in order to get n1 and n2 and then check it
            self.tag.calculateN1N2() # Calculate n1 and n2 with A, B
            self.tag.checkN1N2() # Check result with D
            self.e = self.tag.generateE()
            self.f = self.tag.generateF()
            # Tag -> Charlie
            self.charlie.receivesEF(self.e,self.f)
            # Tag -> Reader
            self.reader.receivesEF(self.e,self.f)
            self.reader.getID() # Calculate ID with E
            self.reader.checkN1N2() # Check with F
            # Round finished, now Charlie tries to guess k1, k2, ID
            self.charlie.computeAproximation(i)
            # Round finished, recalculating pseudonim pid and pid2
            self.reader.recalculatePseudonim()
            self.reader.updateN1N2()
            self.tag.recalculatePseudonim()
            i+=1
        
        self.charlie.printPlots()

        
          

if __name__ == "__main__":
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger(__name__)
    world = World(65)
    world.start_simulation()
 