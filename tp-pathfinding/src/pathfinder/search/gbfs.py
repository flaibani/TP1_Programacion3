from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class GreedyBestFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Encuentra el camino entre dos puntos en una grilla usando la Búsqueda Avara Primero el mejor(GBFS)

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
        frontier.add(node, grid.h_manhatan(node.state))

        while True:

            # Falla si la Frontera está vacía
            if frontier.is_empty():
                return NoSolution(reached)

            # Elimina un nodo de la Frontera
            node = frontier.pop()

            # Retorna si el nodo contiene un estado objetivo
            # Aplica el test objetivo
            # después de sacar el nodo de la Frontera
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
                    frontier.add(new_node, grid.h_manhatan(node.state))
