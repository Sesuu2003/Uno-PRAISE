# cargar DB
from conexionDB import consultar_DB
import numpy as np
import pandas as pd
import random
import os
query = """select c.color, tc.tipo from carta c
join tipoCarta tc on tc.id = c.id_tipo;
"""

class Jugador:
    def __init__(self, nombre, mano=[]):
        self.nombre = nombre
        self.mano = mano
    def comparar(self, carta, pila_descartes):
        carta_pila = pila_descartes[-1]
        return ((carta[0] == carta_pila[0]) or (carta[0] == "wild")) or (carta[1] == carta_pila[1])
    def jugar(self, carta, pila_descartes):
        if self.comparar(carta, pila_descartes):
            pila_descartes.append(carta)
            self.mano.remove(carta)
            print("Jugué la carta "+ carta[0]+" "+carta[1])
        else:
            print("Carta inválida")
    def pedir(self, pila_descartes):
        repartir(mazo, self, 1) 
    def turno(self, pila_descartes):
        print("Mano de "+self.nombre+" :")
        #print(self.mano)
        posiciones(self.mano)
        print("Jugar carta: 1, pedir: 2")
        eleccion = int(input())
        if eleccion == 1:
            print("Seleccione qué carta jugar: ")
            carta = input()
            carta = int(carta) -1
            self.jugar(self.mano[carta], pila_descartes)
        else:
            self.pedir(pila_descartes)


class Bot(Jugador):
    def __init__(self, nombre, mano=[]):
        self.nombre = nombre
        self.mano = mano
    def turno(self, pila_descartes):
        coincidencia = False
        for c in self.mano:
            if self.comparar(c,pila_descartes):
                self.jugar(c,pila_descartes)
                coincidencia = True
                break;
        if coincidencia == False:
            print("Saco una carta")
            self.pedir(pila_descartes)
            

def desapilar(mazo,cantidad):
    cartas = mazo[-cantidad:]
    del mazo[-cantidad:]
    return cartas

def repartir(mazo,jugador,cantidad=2):
    jugador.mano += desapilar(mazo, cantidad)

def posiciones(lista):
    for (i, item) in enumerate(lista, start=0):
        print(i+1, item)

    

mazo = consultar_DB(query).values.tolist()*2
random.shuffle(mazo)
pila_descartes = list()
j = Jugador("Sesuu")
j2 = Bot("Botardo")
repartir(mazo,j)
repartir(mazo,j2)
pila_descartes = desapilar(mazo,1)
jugadores = list()
jugadores += [j,j2]
def gameloop(jugadores,mazo):
    fin = False
    while fin == False:
        print("Pila de descartes: ")
        print(pila_descartes[-1])
        for jugador in jugadores:
            print("Turno de "+jugador.nombre)  
            jugador.turno(pila_descartes)
            if jugador.mano == []:
                ganador = jugador
                fin = True
            os.system('clear')
        
    print("Juego terminado. Ganador: "+ganador.nombre)

gameloop(jugadores,mazo)