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
    def __init__(self,reseat) -> None:
        """Construye una instancia de la clase."""
        self.reseat = reseat  # Numero de reinicios
        super().__init__()
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
                self.reseat -= 1
                #El valor objetivo se mejora 
                if self.value < value:
                    self.tour = actual
                    self.value = value
                #Retornamos porque agotamos la posibilidad 
                #de reiniciar la búsqueda
                if self.reseat == 0:
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

    def __init__(self,max_tabu_size,limit_iters_without_progress) -> None:
        """Construye una instancia de la clase."""
        self.count_iters_without_progress = 0
        self.max_tabu_size = max_tabu_size
        self.limit_iters_without_progress = limit_iters_without_progress
        super().__init__()

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
        mejor = actual
        mejor_value = value 
        tabu = []
        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)
            for act in list(diff.keys()):
                if act in tabu:
                    diff.pop(act)

            # Buscar las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val == 
                        max(diff.values())]
    
            # Elegir una accion aleatoria
            act = choice(max_acts)

            #nos movemos al sucesor
            actual = problem.result(actual, act)
            value = value + diff[act]
            tabu.append(act)   
            if (len(tabu)>self.max_tabu_size):
                tabu.pop(0)
            
            if (value>mejor_value):
                self.count_iters_without_progress=0
                mejor=actual
                mejor_value=value  
            else:
                self.count_iters_without_progress+=1

            self.niters += 1
            if (self.count_iters_without_progress==self.limit_iters_without_progress):
                self.tour = mejor
                self.value = mejor_value
                end = time()
                self.time = end-start
                break 
            
class TabuVariante(LocalSearch):
    """Algoritmo de busqueda tabu."""

    def __init__(self,max_tabu_size,limit_iters_without_progress,number_best_actions) -> None:
        """Construye una instancia de la clase."""
        self.count_iters_without_progress = 0
        self.max_tabu_size = max_tabu_size
        self.limit_iters_without_progress = limit_iters_without_progress
        self.number_best_actions = number_best_actions
        super().__init__()

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
        mejor = actual
        mejor_value = value 
        tabu = []
        while True:

            # Determinar las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)
            for act in list(diff.keys()):
                if act in tabu:
                    diff.pop(act)

            # cambiar comentario
            max_acts = [act for act, val in diff.items() if val in 
                        sorted(diff.values(),reverse=True)[:self.number_best_actions]]
    
            # Elegir una accion aleatoria
            act = choice(max_acts)

            #nos movemos al sucesor
            actual = problem.result(actual, act)
            value = value + diff[act]
            tabu.append(act)   
            if (len(tabu)>self.max_tabu_size):
                tabu.pop(0)
            
            if (value>mejor_value):
                self.count_iters_without_progress=0
                mejor=actual
                mejor_value=value  
            else:
                self.count_iters_without_progress+=1

            self.niters += 1
            if (self.count_iters_without_progress==self.limit_iters_without_progress):
                self.tour = mejor
                self.value = mejor_value
                end = time()
                self.time = end-start
                break 

        
        
