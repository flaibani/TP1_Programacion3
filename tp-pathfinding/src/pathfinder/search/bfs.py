from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """

        # Initialize a node with the initial position
        #node = Node("", grid.start, 0)
        node = Node("", state=grid.start, cost=0, parent=None, action=None)

        # Initialize the reached dictionary to be empty
        reached = {} 

        # Return if the node contains a goal state
        if node.state == grid.end:
            return Solution(node, reached)

        # Initialize the frontier with the initial node
        # In this example, the frontier is a queue
        frontier = QueueFrontier()
        frontier.add(node)

        # Add the node to the reached dictionary
        reached[node.state] = True

        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(reached)

            # Remove a node from the frontier
            node = frontier.remove()

            successors = grid.get_neighbours(node.state)
            for (dir, new_state) in successors.items():

                # Check if the successor is not reached
                if new_state not in reached:

                    # Initialize the son node
                    new_node = Node("", new_state,
                                node.cost + grid.get_cost(new_state),
                                parent=node, action=dir)

                    # Return if the node contains a goal state
                    # In this example, the goal test is run
                    # before adding a new node to the frontier
                    if new_state == grid.end:
                        return Solution(new_node, reached)

                    # Mark the successor as reached
                    reached[new_state] = True

                    # Add the new node to the frontier
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