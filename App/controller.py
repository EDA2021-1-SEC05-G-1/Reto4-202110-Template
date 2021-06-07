"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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

import time
import tracemalloc
import config as cf
from App import model
from DISClib.ADT import map as m
import csv
from DISClib.ADT import list as lt
# ___________________________________________________
#  Inicializacion del catalogo
# ___________________________________________________


def init():
    """
    Llama la funcion de inicializacion  del modelo.
    """
    # analyzer es utilizado para interactuar con el modelo


    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    analyzer = model.newAnalyzer()
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return analyzer,delta_time, delta_memory


# ___________________________________________________
#  Funciones para la carga de datos y almacenamiento
#  de datos en los modelos
# ___________________________________________________


def loadData(analyzer, connectionsfile, landing_points_file, countriesfile):
    """
    Carga los datos de los archivos CSV en el modelo.
    Se crea un arco entre cada par de estaciones que
    pertenecen al mismo servicio y van en el mismo sentido.

    addRouteConnection crea conexiones entre diferentes rutas
    servidas en una misma estación.
    """

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    connectionsfile = cf.data_dir + connectionsfile
    input_file1 = csv.DictReader(open(connectionsfile, encoding="utf-8"),
                                 delimiter=",")
    landing_points_file = cf.data_dir + landing_points_file
    input_file2 = csv.DictReader(open(landing_points_file, encoding="utf-8"),
                                 delimiter=",")
    countriesfile = cf.data_dir + countriesfile
    input_file3 = csv.DictReader(open(countriesfile, encoding="utf-8"),
                                 delimiter=",")

    for country in input_file3:
        model.addCountry(analyzer, country)

    for landingPoint in input_file2:
        model.addLandingPoint(analyzer, landingPoint)

    for connection in input_file1:
        model.addConection(analyzer, connection)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return analyzer,delta_time, delta_memory

def optionthree(cont,lp1,lp2):

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    valor2=model.stronglyConnected(cont, lp1, lp2)

    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return valor2,delta_time,delta_memory

def optionFour(cont):
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    lstLandingPoints = m.keySet(cont['landingPoints'])
    lst = lt.newList()
    for key in lt.iterator(lstLandingPoints):
        landingPoint = m.get(cont['landingPoints'], key)['value']
        noc = model.getNumberOfConnections(key,cont)
        lt.addLast(lst, {
                   'name': landingPoint['name'], 'country': landingPoint['country'], 'id': key, 'conecctions': noc})
    
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return lst,delta_time,delta_memory

def optionFive(cont,countryA,countryB):
    
    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    countryA = model.getCountry(cont,countryA)
    countryB = model.getCountry(cont,countryB)
    resp=model.minimumCostPaths(cont,countryA)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return resp,delta_time,delta_memory
def optionSix(cont,lp):

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    resp=model.minimumCostPaths(cont,lp)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return resp,delta_time,delta_memory
def optionSeven(cont,lp):

    tracemalloc.start()
    start_time = getTime()
    start_memory = getMemory()
    devuelve=model.optionSeven(cont,lp)
    stop_memory = getMemory()
    stop_time = getTime()
    tracemalloc.stop()

    delta_time = stop_time - start_time
    delta_memory = deltaMemory(start_memory, stop_memory)
    return devuelve,delta_time,delta_memory


def totalConnections(analyzer):
    """
    Total de enlaces entre las paradas
    """
    return model.totalConnections(analyzer)


def getFirstLandingPoint(analyzer):
    return model.getFirstLandingPoint(analyzer)


def getLastCountry(analyzer):
    return model.getLastCountry(analyzer)


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
# ======================================
# Funciones para medir tiempo y memoria
# ======================================


def getTime():
    """
    devuelve el instante tiempo de procesamiento en milisegundos
    """
    return float(time.perf_counter()*1000)



def getMemory():
    """
    toma una muestra de la memoria alocada en instante de tiempo
    """
    return tracemalloc.take_snapshot()


def deltaMemory(start_memory, stop_memory):
    """
    calcula la diferencia en memoria alocada del programa entre dos
    instantes de tiempo y devuelve el resultado en bytes (ej.: 2100.0 B)
    """
    memory_diff = stop_memory.compare_to(start_memory, "filename")
    delta_memory = 0.0

    # suma de las diferencias en uso de memoria
    for stat in memory_diff:
        delta_memory = delta_memory + stat.size_diff
    # de Byte -> kByte
    delta_memory = delta_memory/1024.0
    return delta_memory
