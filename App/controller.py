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
    analyzer = model.newAnalyzer()
    return analyzer


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

    return analyzer

def optionthree(cont,lp1,lp2):
    valor2=model.stronglyConnected(cont, lp1, lp2)
    return valor2

def optionFour(cont):
    lstLandingPoints = m.keySet(cont['landingPoints'])
    lst = lt.newList()
    for key in lt.iterator(lstLandingPoints):
        landingPoint = m.get(cont['landingPoints'], key)['value']
        noc = model.getNumberOfConnections(key,cont)
        lt.addLast(lst, {
                   'name': landingPoint['name'], 'country': landingPoint['country'], 'id': key, 'conecctions': noc})
    return lst

def optionFive(cont,countryA,countryB):
    countryA = model.getCountry(cont,countryA)
    countryB = model.getCountry(cont,countryB)
    model.minimumCostPaths(cont,countryA)

def optionSix(cont,lp):
    model.minimumCostPaths(cont,lp)
    
def optionSeven(cont,lp):
    return model.optionSeven(cont,lp)


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