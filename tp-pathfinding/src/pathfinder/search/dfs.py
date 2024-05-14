from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Encuentra el camino entre dos puntos en una grilla usando la Busqueda Primero en Profundidad(DFS)

        Args:
            grid (Grid): Grilla de puntos
            
        Returns:
            Solution: Solución encontrada
        """

        # Inicializa un nodo con la posición inicial
        node = Node("", state=grid.start, cost=0, parent=None, action=None)

        # Inicializa el diccionario de Explorados como vacío
        explored = {} 

        # Retorna si el nodo contiene un estado objetivo
        if node.state == grid.end:
            return Solution(node, explored)

        # Inicializar la Frontera con el nodo inicial
        # En este ejemplo, la frontera es una Pila
        frontier = StackFrontier()
        frontier.add(node)

        # Add the node to the explored dictionary
        #explored[node.state] = True

        while True:

            # Falla si la Frontera está vacía
            if frontier.is_empty():
                return NoSolution(explored)

            # Elimina un nodo de la Frontera
            node = frontier.remove()

            if node.state in explored: 
                continue
            explored[node.state] = True

            successors = grid.get_neighbours(node.state)
            for (dir, new_state) in successors.items():

                # Chequea si el sucesor no fue explorado
                if new_state not in explored:

                    # Inicializa el nodo hijo
                    new_node = Node("", new_state,
                                node.cost + grid.get_cost(new_state),
                                parent=node, action=dir)

                    # Retorna si el nodo contiene un estado objetivo
                    # In this example, the goal test is run
                    # before adding a new node to the frontier
                    if new_state == grid.end:
                        return Solution(new_node, explored)

                    # Agrega el nodo de la Frontera
                    frontier.add(new_node)

'''
function GRAPH-DFS(problema) return solución o fallo
    n₀ ← NODO(problema.estado-inicial, None, None, 0)
    if problema.test-objetivo(n₀.estado) then return solución(n₀)
    frontera ← Pila()
    frontera.apilar(n₀)
    expandidos ← {}
    do
        if frontera.vacía() then return fallo
        n ← frontera.desapilar()

        if n.estado is in expandidos then continue
        expandidos.insertar(n.estado)

        forall a in problema.acciones(n.estado) do
            s’ ← problema.resultado(n.estado, a)
            if s’ is not in expandidos then
                n’ ← Nodo(s’, n, a, n.costo + problema.costo-individual(n.estado,a))
                if problema.test-objetivo(s’) then return solución(n’)
                frontera.apilar(n’)
'''