from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
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

        # Initialize the explored dictionary to be empty
        explored = {} 

        # Return if the node contains a goal state
        if node.state == grid.end:
            return Solution(node, explored)

        # Initialize the frontier with the initial node
        # In this example, the frontier is a queue
        frontier = StackFrontier()
        frontier.add(node)

        # Add the node to the explored dictionary
        #explored[node.state] = True

        while True:

            #  Fail if the frontier is empty
            if frontier.is_empty():
                return NoSolution(explored)

            # Remove a node from the frontier
            node = frontier.remove()

            if node.state in explored: 
                continue
            explored[node.state] = True

            successors = grid.get_neighbours(node.state)
            for (dir, new_state) in successors.items():

                # Check if the successor is not reached
                if new_state not in explored:

                    # Initialize the son node
                    new_node = Node("", new_state,
                                node.cost + grid.get_cost(new_state),
                                parent=node, action=dir)

                    # Return if the node contains a goal state
                    # In this example, the goal test is run
                    # before adding a new node to the frontier
                    if new_state == grid.end:
                        return Solution(new_node, explored)

                    # Add the new node to the frontier
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