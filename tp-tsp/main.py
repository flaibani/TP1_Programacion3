"""Modulo principal.

Autor: Mauro Lucci.
Fecha: 2023.
Materia: Prog3 - TUIA
"""

import parse
import load
import search
import plot
import problem

# Algoritmos involucrados
HILL_CLIMBING = "hill"
HILL_CLIMBING_RANDOM_RESET = "hill_reset"
TABU_SEARCH = "tabu"
TABU_SEARCH_VARIANTE = "tabu_variante"
ALGO_NAMES = [HILL_CLIMBING, HILL_CLIMBING_RANDOM_RESET, TABU_SEARCH,TABU_SEARCH_VARIANTE]


def main() -> None:
    """Funcion principal."""
    # Parsear los argumentos de la linea de comandos
    args = parse.parse()
    """ print("argumento")
    print(args.filename) """
    # Leer la instancia
    G, coords = load.read_tsp(args.filename)

    # Construir la instancia de TSP
    p = problem.TSP(G)

    number_nodes = p.G.number_of_nodes()
    # Construir las instancias de los algoritmos
    algos = {HILL_CLIMBING: search.HillClimbing(),
             HILL_CLIMBING_RANDOM_RESET: search.HillClimbingReset(round(number_nodes * 2)),
             TABU_SEARCH: search.Tabu(max_tabu_size = round(number_nodes * 5 / 24 + 15),
                                        limit_iters_without_progress = number_nodes * 20),
             TABU_SEARCH_VARIANTE: search.TabuVariante(max_tabu_size = round(number_nodes / 8) ,
                                                        limit_iters_without_progress = 1000, #number_nodes * 30,
                                                        number_best_actions = round(number_nodes / 3))}

    # Resolver el TSP con cada algoritmo
    for algo in algos.values():
        algo.solve(p)
        
    # Mostrar resultados por linea de comandos
    print("Valor:", "Tiempo:", "Iters:", "Algoritmo:", sep="\t\t")
    for name, algo in algos.items():
        print(algo.value, "%.2f" % algo.time, algo.niters, name, sep="\t\t")

    # Graficar los tours
    tours = {}
    tours['init'] = (p.init, p.obj_val(p.init))  # estado inicial
    for name, algo in algos.items():
        tours[name] = (algo.tour, algo.value)
    plot.show(G, coords, args.filename, tours)


if __name__ == "__main__":
    main()
