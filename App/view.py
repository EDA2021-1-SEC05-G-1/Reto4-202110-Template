"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import sys
import config
import threading
from App import controller
from DISClib.ADT import stack
assert config

"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""
connectionsfile = 'connections.csv'
countriesfile = 'countries.csv'
landing_points_file = 'landing_points.csv'
initialStation = None

def printMenu():
    print("\n")
    print("*******************************************")
    print("Bienvenido")
    print("1- Inicializar Analizador")
    print("2- Cargar información de los landing points")
    print("3- Conocer si dos landing points estan en el mismo cluster")
    print("4- Encontrar el (los) landing point(s) que sirven como punto de interconexión a más cables en la red")
    print("5- Encontrar la ruta mínima en distancia para enviar información entre dos paises")
    print("6- Identificar la red de expansión mínima en distancias que llegue a más landing points")
    print("7- Cuántos y cuáles son los países afectados con la caída del landing point")
    print("0- Salir")
    print("*******************************************")


def optionTwo(cont):
    print("\nCargando información de transporte de singapur ....")
    controller.loadServices(cont, connectionsfile, landing_points_file, countriesfile)
    numedges = controller.totalConnections(cont)
    numvertex = controller.totalStops(cont)
    print('Numero de vertices: ' + str(numvertex))
    print('Numero de arcos: ' + str(numedges))
    print('El limite de recursion actual: ' + str(sys.getrecursionlimit()))


def optionThree(cont):
    print('El número de componentes conectados es: ' +
          str(controller.connectedComponents(cont)))



"""
Menu principal
"""
def thread_cycle():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar\n>')

        if int(inputs[0]) == 1:
            print("\nInicializando....")
            # cont es el controlador que se usará de acá en adelante
            cont = controller.init()

        elif int(inputs[0]) == 2:
            optionTwo(cont)
    else:
        sys.exit(0)
sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()