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


class LocalSearch:
    """Clase que representa un algoritmo de búsqueda local general."""

    def __init__(self) -> None:
        """Construye una instancia de la clase."""
        self.niters = 0     # NÚmero de iteraciones totales
        self.time = 0       # Tiempo de ejecuciÓn
        self.tour = []      # SoluciÓn, inicialmente vacÍa
        self.value = None   # Valor objetivo de la soluciÓn

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimizaciÓn."""
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
        # Inicio del reloj
        start = time()

        # Arranca del estado inicial: [c0, c1, c2,..., cn-1, 0]
        actual = problem.init
        value = problem.obj_val(problem.init)

        while True:

            # Determina las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Busca las acciones que generan el mayor incremento de valor obj
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

    def __init__(self,reset) -> None:
        """Construye una instancia de la clase."""
        self.reset = reset  # Numero de reinicios
        super().__init__()

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con ascensión de colinas.
        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        repeat: int
            número de reinicios aleatorios permitidos
        """
        # Inicio del reloj
        start = time()

        # Arranca del estado inicial: [c0, c1, c2,..., cn-1, 0]
        actual = problem.init
        value = problem.obj_val(problem.init)
        self.value = float('-inf')
        while True:

            # Determina las acciones que se pueden aplicar
            # y las diferencias en valor objetivo que resultan
            diff = problem.val_diff(actual)

            # Busca las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val ==
                        max(diff.values())]
            #print("max_acts HCR", max_acts)

            # Elige una acción aleatoria
            act = choice(max_acts)
            #print("act HCR", act)

            # Encuentra un máximo local 
            # (diferencia de valor objetivo no positiva)
            if diff[act] <= 0:
                self.reset -= 1
                # El valor objetivo se mejora 
                if self.value < value:
                    self.tour = actual
                    self.value = value
                # Retorna al llegar al límite de reinicios establecido
                if self.reset == 0:
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

    def __init__(self,max_tabu_size,limit_iters_without_progress) -> None:
        """Construye una instancia de la clase."""
        self.count_iters_without_progress = 0
        self.max_tabu_size = max_tabu_size
        self.limit_iters_without_progress = limit_iters_without_progress
        super().__init__()

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con la búsqueda Tabú.
        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        """

        # Inicio del reloj
        start = time()

        # Arranca del estado inicial: [c0, c1, c2,..., cn-1, 0]
        actual = problem.init
        value = problem.obj_val(problem.init)
        best = actual           # mejor solución
        best_value = value      # valor objetivo de la mejor solución 
        tabu = []               # lista Tabú
        while True:

            # Determina las acciones que pueden aplicarse y que no están en la lista Tabú
            diff = problem.val_diff(actual)
            for act in list(diff.keys()):
                if act in tabu:
                    diff.pop(act)

            # Busca las acciones que generan el mayor incremento de valor obj
            max_acts = [act for act, val in diff.items() if val == 
                        max(diff.values())]

            # Elige una acción aleatoria
            act = choice(max_acts)

            # Se mueve al sucesor
            actual = problem.result(actual, act)
            value = value + diff[act]

            # Actualiza la lista Tabú
            tabu.append(act) 

            # Controla el tamaño de la lista Tabú            
            if (len(tabu) > self.max_tabu_size):
                tabu.pop(0)

            # Guarda el mejor estado, que será la solución
            if (value > best_value):
                self.count_iters_without_progress=0
                best = actual
                best_value = value  
            else:
                self.count_iters_without_progress += 1

            self.niters += 1

            # Criterio de parada
            # Límite de repeticiones sin mejoras
            if (self.count_iters_without_progress == self.limit_iters_without_progress):
                self.tour = best
                self.value = best_value
                end = time()
                self.time = end-start
                break 


class TabuVariante(LocalSearch):
    """Clase que representa una variante algoritmo de búsqueda tabú.
    
    Modificación del algoritmo Tabú que elige entre un número determinado de mejores 
    acciones posibles (number_best_actions)
    """

    def __init__(self,max_tabu_size,limit_iters_without_progress,number_best_actions) -> None:
        """Construye una instancia de la clase."""
        self.count_iters_without_progress = 0
        self.max_tabu_size = max_tabu_size
        self.limit_iters_without_progress = limit_iters_without_progress
        self.number_best_actions = number_best_actions
        super().__init__()

    def solve(self, problem: OptProblem):
        """Resuelve un problema de optimización con una variante de la búsqueda Tabú.
        Argumentos:
        ==========
        problem: OptProblem
            un problema de optimización
        """

        # Inicio del reloj
        start = time()

        # Arranca del estado inicial: [c0, c1, c2,..., cn-1, 0]
        actual = problem.init
        value = problem.obj_val(problem.init)
        best = actual
        best_value = value 
        tabu = []
        while True:

            # Determina las acciones que pueden aplicarse y que no están en la lista Tabú
            diff = problem.val_diff(actual)
            for act in list(diff.keys()):
                if act in tabu:
                    diff.pop(act)

            # Selecciona una cantidad (self.number_best_actions) de acciones con mejor valor objetivo
            max_acts = [act for act, val in diff.items() if val in 
                        sorted(diff.values(), reverse=True)[:self.number_best_actions]]

            # Elige una acción aleatoria
            act = choice(max_acts)

            # Se mueve al sucesor
            actual = problem.result(actual, act)
            value = value + diff[act]

            # Actualiza la lista Tabú
            tabu.append(act)   

            # Controla el tamaño de la lista Tabú
            if (len(tabu) > self.max_tabu_size):
                tabu.pop(0)

            # Guarda el mejor estado, que será la solución
            if (value > best_value):
                self.count_iters_without_progress = 0
                best = actual
                best_value = value  
            else:
                self.count_iters_without_progress += 1

            self.niters += 1

            # Criterio de parada
            # Límite de repeticiones sin mejoras            
            if (self.count_iters_without_progress == self.limit_iters_without_progress):
                self.tour = best
                self.value = best_value
                end = time()
                self.time = end-start
                break 

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
