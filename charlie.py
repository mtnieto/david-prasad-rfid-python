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
        
    def receivesABD(self, a, b, d):
        self.a = a
        self.b = b
        self.d = d
    
    def receivesEF(self, e, f):
        self.e = e
        self.f = f

    def computeAproximation(self):
        self.k1Estimation()

    
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
        
        for i in range(self.L):
            print("List of bins of position",i,"is:",self.k1_list[i])
            print("Sum of numbers:",sum(self.k1_list[i]))
            
        print("----------------")

        print(output, f'{self.k1_estimation:08b}')

        """
        Tenemos un array de arrays tal que, en el caso de que k1, k2 e ID fueran de 3 bits:
        lista = [[][][]]
        Donde guardaremos en cada posicion i, los valores de los mensajes clave en esa posicion
        Por ejemplo, obtenemos los mensajes A B D E F. La aproximacion nos dice que A y B nos dan
        valores buenos para K1.
        for i in range(3):
            aux = A/2^i
            value = aux % 2
            lista[i].append(value)
            aux = B/2^i
            value = aux % 2
            lista[i].append(value)
            print(statistics.median(lista[i])) //Esto te devuelve la nueva media de la lista de numeros binarios para la posicion i
        

        ----------------

        [7, 6, 5, 4, 3, 2 ,1,0]

        """