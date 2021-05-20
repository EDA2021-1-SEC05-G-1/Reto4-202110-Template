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
import csv
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


def loadServices(analyzer, connectionsfile, landing_points_file, countriesfile):
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

    lastcable = None
    for cable in input_file1:
        if lastcable is not None:
            sameservice = lastcable[0]['cable_id'] == cable['cable_id']
            samedirection = lastcable[0]['destination'] == cable['destination']
            for cable2 in input_file2:
                samebusStop = lastcable[1]['landing_point_id'] == cable2['landing_point_id']#Vertice
            if sameservice and samedirection and not samebusStop:
                model.addStopConnection(analyzer, lastcable, cable, cable2)
        lastcable = [cable, cable2]
    model.addRouteConnections(analyzer)
    return analyzer


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros

# Funciones para la carga de datos

# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo
