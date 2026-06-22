# cargar DB
from conexionDB import consultar_DB
import numpy as np
import pandas as pd
import random
query = """select c.color, tc.tipo from carta c
join tipoCarta tc on tc.id = c.id_tipo;
"""

class Jugador:
    def __init__(self, nombre, mano=[]):
        self.nombre = nombre
        self.mano = mano
    def comparar(self, carta, pila_descartes):
        carta_pila = pila_descartes[-1]
        return (carta[0] == carta_pila[0]) or (carta[1] == carta_pila[1])
    def jugar(self, carta, pila_descartes):
        if self.comparar(carta, pila_descartes) == True:
            pila_descartes.append(carta)
            self.mano.remove(carta)
            print("Jugué la carta "+ carta[0]+" "+carta[1])
        else:
            return False   


def desapilar(mazo,cantidad):
    cartas = mazo[-cantidad:]
    del mazo[-cantidad:]
    return cartas

def repartir(mazo,jugador):
    jugador.mano = desapilar(mazo, 7)

    

mazo = consultar_DB(query).values.tolist()*2
random.shuffle(mazo)
pila_descartes = list()
j = Jugador("Sesuu")
j2 = Jugador("Bot")
repartir(mazo,j)
repartir(mazo,j2)
pila_descartes = desapilar(mazo,1)
print("Mano de J")
print(j.mano)
print("Mano de J2")
print(j2.mano)
print("Pila")
print(pila_descartes)

print("Jugada de "+j.nombre)
j.jugar(random.choice(j.mano),pila_descartes)

print("Mano de J")
print(j.mano)
print("Mano de J2")
print(j2.mano)
print("Pila")
print(pila_descartes)



# jugar