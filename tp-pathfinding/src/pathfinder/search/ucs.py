from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Encuentra el camino entre dos puntos en una grilla usando la Búsqueda de Costo Uniforme(UCS)

        Args:
            grid (Grid): Grilla de puntos

        Returns:
            Solution: Solución encontrada
        """
        # Inicializa un nodo con la posición inicial
        node = Node("", state=grid.start, cost=0, parent=None, action=None)

        # Inicializa el diccionario de Alcanzados como vacío
        reached = {} 

        # Agrega el nodo al diccionario de Alcanzados
        reached[node.state] = 0

        # Retorna si el nodo contiene un estado objetivo
        if node.state == grid.end:
            return Solution(node, reached)

        # Inicializar la frontera con el nodo inicial
        # En este ejemplo, la frontera es una Cola con Prioridad
        frontier = PriorityQueueFrontier()
        frontier.add(node)

        while True:

            # Falla si la Frontera está vacía
            if frontier.is_empty():
                return NoSolution(reached)

            # Elimina un nodo de la Frontera
            node = frontier.pop()

            # Retorna si el nodo contiene un estado objetivo
            # In this example, the goal test is run
            # before adding a new node to the frontier
            if node.state == grid.end:
                return Solution(node, reached)

            successors = grid.get_neighbours(node.state)
            for (dir, new_state) in successors.items():

                cost = node.cost + grid.get_cost(new_state)
                # Chequea si el sucesor no fue alcanzado
                if new_state not in reached or cost < reached[new_state]:
                        
                    # Inicializa el nodo hijo
                    new_node = Node("", new_state,
                                cost,
                                parent=node, action=dir)

                    # Marca al sucesor como Alcanzado
                    reached[new_state] = cost

                    # Agrega el nodo de la Frontera
                    frontier.add(new_node, cost)
   
'''
function GRAPH-UCS(problema) return solución o fallo
    n₀ ← NODO(problema.estado-inicial, None, None, 0)
    frontera ← ColaPrioridad()
    frontera.encolar(n₀,n₀.costo)
    alcanzados ← {n₀.estado: n₀.costo}
    do
        if frontera.vacía() then return fallo
        n ← frontera.desencolar()

        if problema.test-objetivo(n.estado) then return solución(n)
        forall a in problema.acciones(n.estado) do
            s’ ← problema.resultado(n.estado, a)
            c’ ← n.costo + problema.costo-individual(n.estado,a)
            if s’ is not in alcanzados or c’ < alcanzados[s’] then
                n’ ← Nodo(s’, n, a, c’)
                alcanzados[s’] ← c’
                frontera.encolar(n’,c’)
'''
