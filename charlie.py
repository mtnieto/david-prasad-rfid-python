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
        print(self.d, self.f, self.a ^ self.d)
        for i in range(self.L):
            
            # For D
            aux = int(int(self.d)/int(2**(i)))
            value = aux % 2
            self.k1_list[i].append(value)
            print(bin(int(self.d)))
            # For F
            aux = int(int(self.f)/int(2**(i)))
            value = aux % 2
            self.k1_list[i].append(value)
            print(bin(int(self.f)))
            # For A xor D
            aux = int(int(self.a ^ self.d)/int(2**(i)))
            value = aux % 2
            self.k1_list[i].append(value)
            print(bin(int(self.a ^ self.d)))
            # For not A xor F
            aux = int(int(np.uint16(~(self.a ^ self.f)))/int(2**(i)))
            value = aux % 2
            self.k1_list[i].append(value)
            print(bin(int(np.uint16(~(self.a ^ self.f)))))
            # For not B xor D
            aux = int(int(np.uint16(~(self.b ^ self.d)))/int(2**(i)))
            value = aux % 2
            self.k1_list[i].append(value)
            print(bin(int(np.uint16(~(self.b ^ self.d)))))
            # For B xor F
            aux = int(int(self.b ^ self.f)/int(2**(i)))
            value = aux % 2
            self.k1_list[i].append(value)
            print(bin(int(self.b ^ self.f)))
            # For A xor B xor D
            aux = int(int(self.a ^ self.b ^ self.d)/int(2**(i)))
            value = aux % 2
            self.k1_list[i].append(value)
            print(bin(int(self.a ^ self.b ^ self.d)))
             # For A xor B xor F
            aux = int(int(self.a ^ self.b ^ self.f)/int(2**(i)))
            value = aux % 2
            self.k1_list[i].append(value)
            print(bin(int(self.a ^ self.b ^ self.f)))
            
            self.k1_estimation += int(statistics.median(self.k1_list[i])) * 2**i
        print(self.k1_list)
        print(output, self.k1_estimation)

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
        

        """