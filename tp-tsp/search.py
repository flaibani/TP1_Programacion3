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


class LocalSearch:
    """Clase que representa un algoritmo de busqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0  # Numero de iteraciones totales
        self.time = 0  # Tiempo de ejecucion
        self.tour = []  # Solucion, inicialmente vacia
        self.value = None  # Valor objetivo de la solucion

    def solve(self, problem: OptProblem):
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
        repeat = 100
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
                repeat -= 1
                if self.value < value:
                    self.tour = actual
                    self.value = value
                if repeat == 0:
                    end = time()
                    self.time = end - start
                    return
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
        tabu_list = []  # Lista Tabú
        tabu_size = 100  # Tamaño de la lista Tabú

        while self.niters < 500:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]

            # Elegir una accion aleatoria
            act = choice(max_acts)



            actual = problem.result(actual, act)
            value = value + diff[act]
            self.niters += 1

        # Asignar la solución encontrada
        self.tour = actual
        self.value = value
        # Calcular el tiempo de ejecución
        end = time()
        self.time = end - start


'''
    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con búsqueda Tabú."""
        # Inicio del reloj
        start = time()
        print(start)
        # Arrancar desde un estado inicial
        actual = problem.init
        value = problem.obj_val(actual)

        while True:
            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Excluir las acciones en la lista Tabú
            diff_tabu = {act: val for act, val in diff.items() if act not in self.tabu_list}

            # Si no hay acciones disponibles, terminar la búsqueda
            if not diff_tabu:
                break

            # Buscar la acción que genera el mayor incremento de valor objetivo
            act = max(diff_tabu, key=diff_tabu.get)
            print("act",act)
            #act = choice(max_acts)

            # Actualizar la lista Tabú
            self.tabu_list.append(act)
            print(self.tabu_list)
            if len(self.tabu_list) > self.tabu_size:
                self.tabu_list.pop(0)

            # Moverse al sucesor
            actual = problem.result(actual, act)
            value += diff[act]
            self.niters += 1

        # Asignar la solución encontrada
        self.tour = actual
        self.value = value

        # Calcular el tiempo de ejecución
        end = time()
        self.time = end - start

'''

'''
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