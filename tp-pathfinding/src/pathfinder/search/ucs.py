from ..models.grid import Grid
from ..models.frontier import PriorityQueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", state=grid.start, cost=0, parent=None, action=None)

        # Initialize the reached dictionary to be empty
        reached = {} 

        # Add the node to the reached dictionary
        reached[node.state] = 0

        # Return if the node contains a goal state
        if node.state == grid.end:
            return Solution(node, reached)

        # Initialize the frontier with the initial node
        # In this example, the frontier is a queue
        frontier = PriorityQueueFrontier()
        frontier.add(node)

        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(reached)

            # Remove a node from the frontier
            node = frontier.pop()

            # Return if the node contains a goal state
            # In this example, the goal test is run
            # before adding a new node to the frontier
            if node.state == grid.end:
                return Solution(node, reached)

            successors = grid.get_neighbours(node.state)
            for (dir, new_state) in successors.items():

                cost = node.cost + grid.get_cost(new_state)
                # Check if the successor is not reached
                if new_state not in reached or cost < reached[new_state]:
                        
                    # Initialize the son node
                    new_node = Node("", new_state,
                                cost,
                                parent=node, action=dir)

                    # Mark the successor as reached
                    reached[new_state] = cost

                    # Add the new node to the frontier
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
