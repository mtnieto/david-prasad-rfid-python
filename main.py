import random
from reader import Reader
from tag import Tag
## Random int random.randint(0, 9)
## Random bin bin(random.randint(0, 7))
import numpy as np



class World:
    
    def __init__(self): #añadimso numero de rondas?
        self.reader = Reader(1,2,6,5) # Reciben lo mismo tag y reader al init
        self.tag = Tag(2,1,2,6,5)
        #to do , create loop to simulate the rounds
        # Reader starts with a,b,d
    def start_simulation(self,loop):
        i = 0
        while i < loop:
            self.a = Reader.generateA(self.reader)
            self.b = Reader.generateB(self.reader)
            self.d = Reader.generateD(self.reader)
            # Reader -> Tag
            Tag.receivesABD(self.tag, self.a,self.b,self.d) # receibes A, B, D in order to get n1 and n2 and then check it
            Tag.calculateN1N2(self.tag) # Calculate n1 and n2 with A, B
            Tag.checkN1N2(self.tag) # Check result with D
            self.e = Tag.generateE(self.tag)
            self.f = Tag.generateF(self.tag)
            # Tag -> Reader
            Reader.receivesEF(self.reader, self.e,self.f)
            Reader.getID(self.reader) # Calculate ID with E
            Reader.checkN1N2(self.reader) # Check with F
            # Round finished, recalculating pseudonim pid and pid2
            Reader.recalculatePseudonim(self.reader)
            Tag.recalculatePseudonim(self.tag)
            i+=1

        
          

if __name__ == "__main__":
    world = World()
    world.start_simulation(1)
 
    # import pdb 
    # pdb.set_trace()