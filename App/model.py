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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config
from DISClib.ADT.graph import gr
from DISClib.ADT import map as m
from DISClib.DataStructures import mapentry as me
from DISClib.ADT import list as lt
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.Algorithms.Graphs import bfs
assert config

"""
En este archivo definimos los TADs que vamos a usar y las operaciones
de creacion y consulta sobre las estructuras de datos.
"""

# -----------------------------------------------------
#                       API
# -----------------------------------------------------


def newAnalyzer():
    """ Inicializa el analizador

   landing_points: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre estaciones
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    try:
        analyzer = {
                    'landingPoints': None,
                    'countries': None,
                    'connections': None,
                    }

        analyzer['landingPoints'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIds)
        
        analyzer['countries'] = m.newMap(numelements=14000,
                                     maptype='PROBING',
                                     comparefunction=compareIds)

        analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',
                                              directed=True,
                                              size=14000,
                                              comparefunction=compareIds)

        analyzer['connectionsLst'] = lt.newList()
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:newAnalyzer')


def addLandingPoint(analyzer, landingPoint):
    """
    Agrega un landingPoint
    """
    country = landingPoint['name'].split(',')[-1]
    entry = m.get(analyzer['countries'],country[1:])
    landingPoint['country'] = country[1:]
    if entry is not None:
        country = me.getValue(entry)
        lt.addLast(country['landingPoints'], landingPoint)
        # if(country['CapitalLatitude'] == landingPoint['latitude'] and country['CapitalLongitude'] == landingPoint['longitude']):
        #     print('test')
    m.put(analyzer['landingPoints'], landingPoint['landing_point_id'], landingPoint) 
    addVertex(analyzer,landingPoint['landing_point_id'])
    return analyzer

def addVertex(analyzer, landingPointId):
    """
    Adiciona una estación como un vertice del grafo
    """
    try:
        if not gr.containsVertex(analyzer['connections'], landingPointId):
            gr.insertVertex(analyzer['connections'], landingPointId)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addstop')

def addCountry(analyzer, country):
    """
    Agrega un landingPoint
    """
    country['landingPoints']= lt.newList('ARRAY_LIST')
    m.put(analyzer['countries'], country['CountryName'], country) 
    return analyzer

def addConection(analyzer, connection):
    """
    Agrega un landingPoint
    """
    lt.addLast(analyzer['connectionsLst'],connection)
    #error dato
    edge = gr.getEdge(analyzer['connections'], connection['\ufefforigin'], connection['destination'])
    if edge is None:
        gr.addEdge(analyzer['connections'], connection['\ufefforigin'], connection['destination'], formatKM(connection['cable_length']))
    return analyzer

def formatKM(cableLength):
    if(cableLength!='n.a.'):
        length = cableLength.split(' ')[0]
        length= length.replace(',', '')
        return float(length)
    return 0

def getFirstLandingPoint(analyzer):
    lpints = m.keySet(analyzer['landingPoints'])
    entry = m.get(analyzer['landingPoints'],lpints['first']['info'])
    return entry['value']

def getLastCountry(analyzer):
    lpints = m.keySet(analyzer['countries'])
    entry = m.get(analyzer['countries'],lpints['last']['info'])
    return entry['value']
    

def getNumberOfConnections(landingPoint,cont):
    if gr.containsVertex(cont['connections'], landingPoint):
        return gr.outdegree(cont['connections'],landingPoint)
    return 0

def getCountry(cont,country):
    entry = m.get(cont['countries'],country)
    if entry is not None:
        country = me.getValue(entry)
    return None

def getLP(cont,lp):
    entry=m.get(cont['landingPoints'],lp)
    if entry is not None:
        lp=me.getValue(entry)
    return None


def addStopConnection(analyzer, lastcable, cable, cable2):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve.  Por ejemplo:

    75009-10

    Si la estacion sirve otra ruta, se tiene: 75009-101
    """
    try:
        origin = formatVertex(lastcable)
        destination = formatVertex(lastcable)
        addStop(analyzer, origin)
        addStop(analyzer, destination)
        addConnection(analyzer, origin, destination)
        addRouteStop(analyzer, cable)
        addRouteStop(analyzer, lastcable)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addStopConnection')


def addRouteStop(analyzer, service):
    """
    Agrega a una estacion, una ruta que es servida en ese paradero
    """
    entry = m.get(analyzer['landing_points'], service['landing_point_id'])
    if entry is None:
        lstroutes = lt.newList(cmpfunction=compareroutes)
        lt.addLast(lstroutes, service['cable_id'])
        m.put(analyzer['cable_id'], service['cable_id'], lstroutes)
    else:
        lstroutes = entry['value']
        info = service['cable_id']
        if not lt.isPresent(lstroutes, info):
            lt.addLast(lstroutes, info)
    return analyzer


def addRouteConnections(analyzer):
    """
    Por cada vertice (cada estacion) se recorre la lista
    de rutas servidas en dicha estación y se crean
    arcos entre ellas para representar el cambio de ruta
    que se puede realizar en una estación.
    """
    lstlanding_points = m.keySet(analyzer['landing_points'])
    for key in lt.iterator(lstlanding_points):
        lstroutes = m.get(analyzer['landing_points'], key)['value']
        prevrout = None
        for route in lt.iterator(lstroutes):
            route = key + '-' + route
            if prevrout is not None:
                addConnection(analyzer, prevrout, route, 0)
                addConnection(analyzer, route, prevrout, 0)
            prevrout = route


def addConnection(analyzer, origin, destination, distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination, distance)
    return analyzer

# ==============================
# Funciones de consulta
# ==============================


def stronglyConnected(cont,lp1,lp2):
    kos=scc.KosarajuSCC(cont['connections']) #Creamos un otro grafo desde Kosaraju y desde un grafo
    z=scc.stronglyConnected(kos, lp1, lp2) #Buscamos si los dos vertices son componentes fuertemente conectados o pertenecen en el mismo cluster
    x=scc.connectedComponents(kos) #Retorna el numero de componentes fuertemente conectados desde Kosaraju
    return (z,x)


def optionSeven(cont,lp):
    b=bfs.BreadhtFisrtSearch(cont['connections'], lp) #Hacer un befs a partir del landing point
    bs=bfs.bfsVertex(b, cont['connections'], lp)#Hacer un bfs y mirar los componentes que estan conectados con el landing point
    tam=bs['visited']['size']
    print(tam)
    return tam

def connectedComponents(analyzer):
    """
    Calcula los componentes conectados del grafo
    Se utiliza el algoritmo de Kosaraju
    """
    analyzer['components'] = scc.KosarajuSCC(analyzer['connections'])
    return scc.connectedComponents(analyzer['components'])


def minimumCostPaths(analyzer, lp):
    """
    Calcula los caminos de costo mínimo desde la estacion initialStation
    a todos los demas vertices del grafo
    """
    analyzer['paths'] = djk.Dijkstra(analyzer['connections'], lp)
    return analyzer


def hasPath(analyzer, destStation):
    """
    Indica si existe un camino desde la estacion inicial a la estación destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    return djk.hasPathTo(analyzer['paths'], destStation)


def minimumCostPath(analyzer, destStation):
    """
    Retorna el camino de costo minimo entre la estacion de inicio
    y la estacion destino
    Se debe ejecutar primero la funcion minimumCostPaths
    """
    path = djk.pathTo(analyzer['paths'], destStation)
    return path


def totalStops(analyzer):
    """
    Retorna el total de estaciones (vertices) del grafo
    """
    return gr.numVertices(analyzer['connections'])


def totalConnections(analyzer):
    """
    Retorna el total arcos del grafo
    """
    return gr.numEdges(analyzer['connections'])


def servedRoutes(analyzer):
    """
    Retorna la estación que sirve a mas rutas.
    Si existen varias rutas con el mismo numero se
    retorna una de ellas
    """
    lstvert = m.keySet(analyzer['landing_points'])
    maxvert = None
    maxdeg = 0
    for vert in lt.iterator(lstvert):
        lstroutes = m.get(analyzer['landing_points'], vert)['value']
        degree = lt.size(lstroutes)
        if(degree > maxdeg):
            maxvert = vert
            maxdeg = degree
    return maxvert, maxdeg


# ==============================
# Funciones Helper
# ==============================


def formatVertex(service):
    """
    Se formatea el nombrer del vertice con el id de la estación
    seguido de la ruta.
    """
    name = service['landing_point_id'] + '-'
    name = name + service['cable_id']
    return name


# ==============================
# Funciones de Comparacion
# ==============================


def compareIds(object, keyvalueObject):
    """
    Compara dos estaciones
    """
    objectCode = keyvalueObject['key']
    if (object == objectCode):
        return 0
    elif (object > objectCode):
        return 1
    else:
        return -1


def compareLPoints(lp1, lp2):
    """
    Compara dos rutas
    """
    if (lp1 == lp2):
        return 0
    elif (lp1 > lp2):
        return 1
    else:
        return -1

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

# Funciones para agregar informacion al catalogo

# Funciones para creacion de datos

# Funciones de consulta

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

