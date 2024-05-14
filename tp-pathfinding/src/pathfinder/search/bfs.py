from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Encuentra el camino entre dos puntos en una grilla usando la Búsqueda Primero en Anchura(BFS)

        Args:
            grid (Grid): Grilla de puntos
            
        Returns:
            Solution: Solución encontradas
        """

        # Inicializa un nodo con la posición inicial
        node = Node("", state=grid.start, cost=0, parent=None, action=None)

        # Inicializa el diccionario de Alcanzados como vacío
        reached = {} 

        # Retorna si el nodo contiene un estado objetivo
        if node.state == grid.end:
            return Solution(node, reached)

        # Inicializar la Frontera con el nodo inicial
        # En este ejemplo, la frontera es una Cola
        frontier = QueueFrontier()
        frontier.add(node)

        # Agrega el nodo al diccionario de Alcanzados
        reached[node.state] = True

        while True:

            # Falla si la Frontera está vacía
            if frontier.is_empty():
                return NoSolution(reached)

            # Elimina un nodo de la Frontera
            node = frontier.remove()

            successors = grid.get_neighbours(node.state)
            for (dir, new_state) in successors.items():

                # Chequea si el sucesor no fue alcanzado
                if new_state not in reached:

                    # Inicializa el nodo hijo
                    new_node = Node("", new_state,
                                node.cost + grid.get_cost(new_state),
                                parent=node, action=dir)

                    # Retorna si el nodo contiene un estado objetivo
                    # In this example, the goal test is run
                    # before adding a new node to the frontier
                    if new_state == grid.end:
                        return Solution(new_node, reached)

                    # Marca al sucesor como Alcanzado
                    reached[new_state] = True

                    # Agrega el nodo de la Frontera
                    frontier.add(new_node)

'''
function GRAPH-BFS(problema) return solución o fallo
    n₀ ← NODO(problema.estado-inicial, None, None, 0)
    if (problema.test-objetivo(n₀.estado)) then return solución(n₀)
    frontera ← Cola()
    frontera.encolar(n₀)
    alcanzados ← {n₀.estado}
    do
        if frontera.vacía() then return fallo
        n ← frontera.desencolar()

        forall a in problema.acciones(n.estado) do
            s’ ← problema.resultado(n.estado, a)
            if s’ is not in alcanzados then
                n’ ← Nodo(s’, n, a, n.costo + problema.costo-individual(n.estado,a))
                if problema.test-objetivo(s’) then return solución(n’)
                alcanzados.insertar(s’)
                frontera.encolar(n’)
'''