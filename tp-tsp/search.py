"""Este módulo define la clase LocalSearch.

LocalSearch: representa un algoritmo de búsqueda local general.

Las subclases que se encuentran en este módulo son:

* HillClimbing: algoritmo de ascensión de colinas. Se mueve al sucesor con
mejor valor objetivo, y los empates se resuelvan de forma aleatoria.
Ya viene implementado.

* HillClimbingReset: algoritmo de ascensión de colinas de reinicio aleatorio.
No viene implementado, se debe completar.

* Tabu: algoritmo de búsqueda tabú.
No viene implementado, se debe completar.
"""

from __future__ import annotations
from problem import OptProblem
from random import choice
from time import time
import math
import random
import heapq

class LocalSearch:
    """Clase que representa un algoritmo de búsqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0     # Número de iteraciones totales
        self.time = 0       # Tiempo de ejecucion
        self.tour = []      # Solución, inicialmente vacía
        self.value = None   # Valor objetivo de la solución

    def solve(self, problem: OptProblem, instancia):
        """Resuelve un problema de optimización."""
        self.tour = problem.init
        self.value = problem.obj_val(problem.init)


class HillClimbing(LocalSearch):
    """Clase que representa un algoritmo de ascensión de colinas.

    En cada iteración se mueve al estado sucesor con mejor valor objetivo.
    El criterio de parada es alcanzar un óptimo local.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con ascensión de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        """
        # Iniciar del reloj
        start = time()

        # Arranca del estado inicial: [c0, c1, c2,..., cn-1, 0]
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Determina las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Busca las acciones que generan el mayor incremento de valor objetivo
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elige una acción aleatoria
            act = choice(max_acts)

            # Retorna si estamos en un óptimo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:
                self.tour = actual
                self.value = value
                end = time()
                self.time = end-start
                return

            # Sino, se mueve al sucesor
            else:
                actual = problem.result(actual, act)
                value = value + diff[act]
                self.niters += 1


class HillClimbingReset(LocalSearch):
    """Clase que representa un algoritmo de ascensión de colinas con reinicio aleatorio.

    Realiza una serie de ascensiones de colinas. Cuando se atasca, se reinicia desde 
    un estado inicial aleatorio.
    Retorna el estado con mejor valor objetivo encontrado entre todos los reinicios realizados.
    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con ascensión de colinas.

        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        repeat: int
            número de reinicios aleatorios permitidos
        """
        # Inicia el reloj
        start = time()

        # Arranca del estado inicial: [c0, c1, c2,..., cn-1, 0]
        actual = problem.init
        value = problem.obj_val(problem.init)
        self.value = float('-inf')

        # Criterio: el número de nodos determina el número de repeticiones 
        repeat = int(problem.G.number_of_nodes()) * 2
        print("HCR - Reinicios aleatorios: ",repeat)

        while True:

            # Determina las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Busca las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elige una acción aleatoria
            act = choice(max_acts)
 
            # Encuentra un máximo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:
                repeat -= 1
                # El valor objetivo se mejora 
                if self.value < value:
                    self.tour = actual
                    self.value = value
                # Retorna al llegar al límite de reinicios establecido
                if repeat == 0:
                    end = time()
                    self.time = end - start
                    return
                # Reinicia la búsqueda con un nuevo estado inicial 
                else: 
                    actual = problem.random_reset()
                    value = problem.obj_val(actual)
                                    
            # Sino, se mueve al sucesor
            else:
                actual = problem.result(actual, act)
                #print(value, diff[act])
                value = value + diff[act]
                self.niters += 1


class Tabu(LocalSearch):
    """Clase que representa un algoritmo de búsqueda tabú.
    
    Incorpora mejoras al algoritmo de ascensión de colinas ciertas
    para escapar de máximos locales que no son globales.

    Se mueve siempre al sucesor con mejor valor objetivo (mejor, igual o peor o que el actual).
    Mantiene una memoria de corto plazo con información de las últimas iteraciones,
    para evitar estados visitados recientemente y no ciclar.

    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con la búsqueda Tabú.
        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        """
        # Inicia del reloj
        start = time()

        # Arranca del estado inicial: [c0, c1, c2,..., cn-1, 0]
        actual = problem.init
        value = problem.obj_val(problem.init)
        best = actual                                           # mejor solución
        best_value = value                                      # valor objetivo de la mejor solución
        tabu_list = []                                          # lista Tabú
        tabu_size = math.floor(problem.G.number_of_nodes()/8)   # tamaño de la lista Tabú
        action_size = math.floor(problem.G.number_of_nodes()/3) # amplia la búsqueda en los mejores vecinos
        counter_max = 1000                                      # máimode repeticiones sin mejoras
        counter = 0                                             # contador de soluciones sin mejoras 
        print("tabu_size:", tabu_size, "tabu_action:", action_size, "counter_max:", counter_max)

        while True: #self.niters < 2000:
            # Determina las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Filtrar los elementos de diff donde act no esté en tabu_list
            no_tabu_val = {act: diff[act] for act in diff if act not in tabu_list}

            # Obtener el valor máximo en no_tabu_val
            max_val = max(no_tabu_val.values())

            # Crear una lista con todos los act donde val sea igual al máximo valor
            no_tabu = [act for act, val in no_tabu_val.items() if val == max_val]

            # los 10 mayores
            #n = 7
            #top_n_items = heapq.nlargest(n, no_tabu_val.items(), key=lambda x: x[1])
            #no_tabu = [act for act, val in top_n_items]

            # Si no hay acciones disponibles, termina la búsqueda
            #if not no_tabu:
            if len(no_tabu) == 0:
                print("Tabú: No existen acciones permitidas", self.niters)
                break
            # Elige una acción aleatoria
            act = choice(no_tabu)
            print("accion seleccionada", act)

            # Controla la longitud de la lista Tabú
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            # Actualiza la lista Tabú
            tabu_list.append(act)
            #print("tabu_list", tabu_list)    

            actual = problem.result(actual, act)
            value = value + diff[act]
            print("value, value_better", value , best_value)
            self.niters += 1
            # Guarda el mejor estado, que será la solución
            if best_value < value:
                counter = 0
                best = actual
                best_value = value
                #print("actualiza better", value_better)
            else:
                counter += 1
            # Criterio de parada
            # Permite counter_max repeticiones sin mejoras
            if counter >= counter_max:
                break

        # Asigna la solución encontrada
        self.tour = best
        self.value = best_value
        # Calcula el tiempo de ejecución
        end = time()
        self.time = end - start

class Tabu_ant(LocalSearch):
    """Clase que representa un algoritmo de búsqueda tabú.
    
    Incorpora mejoras al algoritmo de ascensión de colinas ciertas
    para escapar de máximos locales que no son globales.

    Se mueve siempre al sucesor con mejor valor objetivo (mejor, igual o peor o que el actual).
    Mantiene una memoria de corto plazo con información de las últimas iteraciones,
    para evitar estados visitados recientemente y no ciclar.

    """

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con la búsqueda Tabú.
        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        """
        # Inicia del reloj
        start = time()

        # Arranca del estado inicial: [c0, c1, c2,..., cn-1, 0]
        actual = problem.init
        value = problem.obj_val(problem.init)
        best = actual                                           # mejor solución
        best_value = value                                      # valor objetivo de la mejor solución
        tabu_list = []                                          # lista Tabú
        tabu_size = math.floor(problem.G.number_of_nodes()/8)   # tamaño de la lista Tabú
        action_size = math.floor(problem.G.number_of_nodes()/3) # amplia la búsqueda en los mejores vecinos
        counter_max = 1000                                      # máimode repeticiones sin mejoras
        counter = 0                                             # contador de soluciones sin mejoras 
        print("tabu_size:", tabu_size, "tabu_action:", action_size, "counter_max:", counter_max)

        while True: #self.niters < 2000:
            # Determina las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Busca las acciones que generan el mayor incremento de valor obj
            #max_acts = [act for act, val in diff.items() if val ==
            #            max(diff.values())]

            # Ordena los valores de diff de mayor a menor y se queda con los 10 mayores
            max_acts = [act for act, val in diff.items() if val in sorted(diff.values(), reverse=True)[:action_size]]
            #max_acts_val = {act: diff[act] for act in max_acts}
            #print("max_acts", max_acts_val)
            #print("tabu_list", tabu_list) 
            # Selecciona las acciones que no están en la lista Tabú
            no_tabu = [act for act in max_acts if act not in tabu_list]
            #no_tabu_val = {act: max_acts_val[act] for act in no_tabu}
            #print("no_tabu", no_tabu_val)

            # Si no hay acciones disponibles, termina la búsqueda
            #if not no_tabu:
            if len(no_tabu) == 0:
                print("Tabú: No existen acciones permitidas", self.niters)
                break
            # Elige una acción aleatoria
            act = choice(no_tabu)
            print("accion seleccionada", act)

            # Controla la longitud de la lista Tabú
            if len(tabu_list) > tabu_size:
                tabu_list.pop(0)

            # Actualiza la lista Tabú
            tabu_list.append(act)
            #print("tabu_list", tabu_list)    

            actual = problem.result(actual, act)
            value = value + diff[act]
            #print("value, value_better", value , best_value)
            self.niters += 1
            # Guarda el mejor estado, que será la solución
            if best_value < value:
                counter = 0
                best = actual
                best_value = value
                #print("actualiza better", value_better)
            else:
                counter += 1
            # Criterio de parada
            # Permite counter_max repeticiones sin mejoras
            if counter >= counter_max:
                break

        # Asigna la solución encontrada
        self.tour = best
        self.value = best_value
        # Calcula el tiempo de ejecución
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
