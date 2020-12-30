from reader import Reader
from tag import Tag
from charlie import Charlie
import logging
import logging.config
import random
import sys
import numpy as np

distances_vectors_k1 = []
distances_vectors_k2 = []
distances_vectors_id = []

for i in range(31):
    distances_vectors_k1.append([])
    distances_vectors_k2.append([])
    distances_vectors_id.append([])


class World:
    
    def __init__(self, loop): 
        pid = random.randint(0, (pow(2,32)))
        pid2 = random.randint(0, (pow(2,32)))
        k1 = random.randint(0, (pow(2,32)))
        k2 = random.randint(0, (pow(2,32)))
        identificator = random.randint(0, pow(2,32))

        self.loop = loop

        self.reader = Reader(pid,pid2,k1,k2) # Reciben lo mismo tag y reader al insit (self,pid, pid2, k1, k2)
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
            self.charlie.computeCombinations()
            self.charlie.computeAproximation(i)
            # Round finished, recalculating pseudonim pid and pid2
            self.reader.recalculatePseudonim()
            self.reader.updateN1N2()
            self.tag.recalculatePseudonim()
            i+=1
        
        for i in range(31):
            distances_vectors_k1[i].append(self.charlie.distance_vector_k1[i])            
            distances_vectors_k2[i].append(self.charlie.distance_vector_k2[i])
            distances_vectors_id[i].append(self.charlie.distance_vector_id[i])
        
    # Tratar los datos
        #self.charlie.printPlots()

        
          

if __name__ == "__main__":
    for i in range(1000):
        logging.config.fileConfig('logging.conf')
        logger = logging.getLogger(__name__)
        world = World(1)
        world.start_simulation()
    
    output = "L, K1, K2, ID\n"
    combinations = ["a","b","d","e","f","a ^ b",
        "a ^ d","a ^ e","a ^ f","b ^ d","b ^ ","b ^ f","d ^ e",
        "d ^ f","e ^f ","a ^ b ^ d","a ^ b ^ e","a ^ b ^ f",
        "a ^ d ^ f","a ^ d ^ f","a ^ e ^ f", 
        "b ^ d ^ e" ,"b ^ d ^ f","b ^ e ^ f",
        "d ^ e ^ f " ,"a ^ b ^ d ^ e","a ^ b ^ d ^ f",
        "a ^ b ^ e ^ f","a ^ d ^ e ^ f","b ^ d ^ e ^ f",
        "a ^ b ^ d ^ e ^ f"]
    for i in range(31):
        value = np.mean(distances_vectors_k1[i])
        output += combinations[i] + ", " + str(value) + ", "
        value = np.mean(distances_vectors_k2[i])
        output += "" + str(value) + ", "
        value = np.mean(distances_vectors_id[i])
        output += "" + str(value) + "\n"
    
    with open("results.csv", "w") as f:
        f.write(output)
 