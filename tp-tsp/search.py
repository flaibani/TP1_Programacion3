"""Este modulo define la clase LocalSearch.

LocalSearch representa un algoritmo de busqueda local general.

Las subclases que se encuentran en este modulo son:

* HillClimbing: algoritmo de ascension de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascension de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de busqueda tabu.
No viene implementado, se debe completar.
"""

from __future__ import annotations
from problem import OptProblem
from random import choice
from time import time
import math

class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem, instancia):
        """Resuelve un problema de optimizacion."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascension de colinas.

    En cada iteracion se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un optimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)

            # Retornar si estamos en un optimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:
                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, nos movemos al sucesor
            else:
                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1

class HillClimbingReset(LocalSearch):

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        repeat: int
            número de reinicios aleatorios permitidos
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)
        self.value = float('-inf')

        # Criterio: el número de nodos determinada el número de repeticiones 
        repeat = int(problem.G.number_of_nodes()) * 2
        print(repeat)

        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]
            #print("max_acts HCR", max_acts)
            # Elegir una accion aleatoria
            act = choice(max_acts)
            #print("act HCR", act)
            # Encontramos un máximo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:
                repeat -= 1
                #El valor objetivo se mejora 
                if self.value < value:
                    self.tour = actual
                    self.value = value
                #Retornamos porque agotamos la posibilidad 
                #de reiniciar la búsqueda
                if repeat == 0:
                    end = time()
                    self.time = end - start
                    return
                #Reiniciamos la búsqueda con un nuevo estado inicial 
                else: 
                    actual = problem.random_reset()
                    value = problem.obj_val(actual)
                                    
            # Sino, nos movemos al sucesor
            else:
                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1


class Tabu(LocalSearch):
    """Algoritmo de busqueda tabu."""

    # COMPLETAR
    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizacion con ascension de colinas.
        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimizacion
        """
        # Inicio del reloj
        start = time()

        # Arrancamos del estado inicial
        actual = problem.init
        value = problem.obj_val(problem.init)
        better = actual
        value_better = value
        tabu_list = []  # Lista Tabú
        tabu_size = math.floor(problem.G.number_of_nodes()/8)  # Tamaño de la lista Tabú
        print("size", tabu_size)
        counter = 0

        while True: #self.niters < 2000:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            # y que no están en la lista Tabu
            #max_acts = [act for act, val in diff.items() if val ==
            #            max(diff.values())]

            # Ordenar los valores de diff de mayor a menor y quedarse con los 10 mayores
            max_acts = [act for act, val in diff.items() if val in sorted(diff.values(), reverse=True)[:10]]
            #print("max_acts", max_acts)

            # lista de acciones que no están en la lista tabu
            no_tabu = [act for act in max_acts if act not in tabu_list]
            #print("no_tabu", no_tabu)

            # Si no hay acciones disponibles, terminar la búsqueda
            #if not no_tabu:
            if len(no_tabu) == 0:
                print("pasos", self.niters)
                break
            # Elegir una accion aleatoria
            act = choice(no_tabu)
            #print("accion seleccionada", act)

            # Actualizar la lista Tabú
            tabu_list.append(act)
            #print("tabu_list", tabu_list)

            # Si pasó el largo máximode la lista, elimina el primer elemento ingresado
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            actual = problem.result(actual, act)
            value = value + diff[act]
            #print("value, value_better", value , value_better)
            self.niters += 1
            if value_better < value:
                counter = 0
                better = actual
                value_better = value
                #print("actualiza better", value_better)
            else:
                counter += 1
            if counter >= 1000:
                break
        # Asignar la solución encontrada
        self.tour = better
        self.value = value_better
        # Calcular el tiempo de ejecución
        end = time()
        self.time = end - start

'''
Ejemplo — TSP.
Comenzar con un tour con la ciudad inicial y agregar las
ciudades de a una, en el orden en que se visitan en el estado
objetivo.

function LOCAL-SEARCH(problema) return estado
    s ← problema.estado-inicial
    while no se cumple criterio de parada do:
        S’ ← {problema.resultado(s,a) for
            a є problema.acciones(s)}
        elegir un buen sucesor s’ є S’
        s ← s’
    return s

function ASCENSIÓN-COLINAS(problema) return estado
    s ← problema.estado-inicial
    do
        S’ ← {problema.resultado(s,a) for
            є problema.acciones(s)}
        s’ ← argmax(problema.f, S’)
        if (problema.f(s’) ≤ problema.f(s)) then return s
    s ← s’

function BÚSQUEDA-TABÚ(problema) return estado
    actual ← problema.estado-inicial
    mejor ← actual
    tabu ← inicialmente vacía
    while no se cumpla el criterio de parada do
        sucesores ← {problema.resultado(actual,a) for a є problema.acciones(actual)}
        #algun cambio
        no_tabues ← {sucesor for sucesor є sucesores if sucesor no es tabú}
        sucesor ← argmax(problema.f, no_tabues}
        if problema.h(mejor) < problema.h(sucesor) then mejor ← sucesor
        actualizar la lista tabú
        actual ← sucesor
    return mejor
'''
