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
from DISClib.ADT import map as m
from DISClib.ADT import list as lt

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
    answera=controller.loadData(cont, connectionsfile, landing_points_file, countriesfile)
    cont=answera[0]
    numLP = m.size(cont['landingPoints'])
    numCountries = m.size(cont['countries'])
    numConections = controller.totalConnections(cont)
    print('Total de landing points: '+str(numLP))
    print('Total de conexiones: '+str(numConections))
    print('Total de paises: '+str(numCountries))
    firstLp = controller.getFirstLandingPoint(cont)
    print('Informacion del primer landing point:')
    print('     Identificador: '+firstLp['id'])
    print('     Nombre: '+firstLp['name'])
    print('     Latitud: '+firstLp['latitude'])
    print('     Longitud: '+firstLp['longitude'])
    lastCountry = controller.getLastCountry(cont)
    print('Informacion del ultimo pais cargado:')
    print('     Nombre: '+lastCountry['CountryName'])
    print('     Población: '+lastCountry['Population'])
    print('     Usuarios de internet: '+lastCountry['Internet users'])
    print("Tiempo [ms]: ", f"{answera[1]:.3f}", "  ||  ", #Imprime el tiempo
              "Memoria [kB]: ", f"{answera[2]:.3f}") #Imprime la memoria
def optionthree(cont,lp1,lp2):
    answerb=controller.optionthree(cont,lp1,lp2)
    valor=answerb[0]
    r1=valor[0]
    r2=valor[1]
    if r1==True:
        print("Los landing points estan en el mismo cluster.")
    else:
        print("Los landing points no estan en el mismo cluster.")
    print("El numero de clusteres presentes en la red son: "+str(r2))
    print("Tiempo [ms]: ", f"{answerb[1]:.3f}", "  ||  ", #Imprime el tiempo
              "Memoria [kB]: ", f"{answerb[2]:.3f}") #Imprime la memoria
    
def optionFour(cont):
    answerc = controller.optionFour(cont)
    lst=answerc[0]
    for landingPoint in lt.iterator(lst):
        print('*'*20)
        print('Nombre: '+landingPoint['name'])
        print('Pais: '+landingPoint['country'])
        print('Id: '+landingPoint['id'])
        print('# de cables conectados: '+str(landingPoint['conecctions']))
    print("Tiempo [ms]: ", f"{answerc[1]:.3f}", "  ||  ", #Imprime el tiempo
              "Memoria [kB]: ", f"{answerc[2]:.3f}") #Imprime la memoria

def optionFive(cont,countryA,countryB):
    answerd=controller.optionFive(cont,countryA,countryB)
    print(answerd[0])
    print("Tiempo [ms]: ", f"{answerd[1]:.3f}", "  ||  ", #Imprime el tiempo
              "Memoria [kB]: ", f"{answerd[2]:.3f}") #Imprime la memoria
def optionSix(cont,lp):
    answere=controller.optionSix(cont,lp)
    print(cont['paths'])

    print("Tiempo [ms]: ", f"{answere[1]:.3f}", "  ||  ", #Imprime el tiempo
              "Memoria [kB]: ", f"{answere[2]:.3f}") #Imprime la memoria
def optionSeven(cont,lp):
    answerf=controller.optionSeven(cont,lp)

    print("Tiempo [ms]: ", f"{answerf[1]:.3f}", "  ||  ", #Imprime el tiempo
              "Memoria [kB]: ", f"{answerf[2]:.3f}") #Imprime la memoria
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
            answer = controller.init()
            cont=answer[0]
            print("Tiempo [ms]: ", f"{answer[1]:.3f}", "  ||  ", #Imprime el tiempo
              "Memoria [kB]: ", f"{answer[2]:.3f}") #Imprime la memoria
        elif int(inputs[0]) == 2:
            print("\nCargar información de los landing points...")
            optionTwo(cont)  
        elif int(inputs[0])==3:
            lp1=input("Ingrese el id del primer landing point: ")
            lp2=input("Ingrese el id del segundo landing point: ")
            optionthree(cont,lp1,lp2)
        elif int(inputs[0]) == 4:
            optionFour(cont)  
        elif int(inputs[0]) == 5:
            countryA = input("Pais A: ")
            countryB = input("Pais B: ")
            optionFive(cont,countryA,countryB) 
        elif int(inputs[0]) == 6:
            lp = input("Landing Point: ")
            optionSix(cont,lp)
        elif int(inputs[0]) == 7:
            lp=input("Landing point: ")
            optionSeven(cont, lp)
        elif int(inputs[0])==0:
            sys.exit(0)
        else:
            sys.exit(0)
    sys.exit(0)

if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=thread_cycle)
    thread.start()
