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
ALGO_NAMES = [HILL_CLIMBING, HILL_CLIMBING_RANDOM_RESET, TABU_SEARCH]


def main() -> None:
    """Funcion principal."""
    # Parsear los argumentos de la linea de comandos
    args = parse.parse()

    # Leer la instancia
    G, coords = load.read_tsp(args.filename)

    # Construir la instancia de TSP
    p = problem.TSP(G)

    # Construir las instancias de los algoritmos
    algos = {HILL_CLIMBING: search.HillClimbing(),
             HILL_CLIMBING_RANDOM_RESET: search.HillClimbingReset(),
             TABU_SEARCH: search.Tabu(3)}

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

Proponer una formulación de estados completa y una función
objetivo para el problema del viajante (TSP).    

Notación.
{c₁,…,cn}: conjunto de ciudades, suponer que c₁ es la inicial.
dist(ci,cj): distancia en km entre todo par de ciudades ci y cj.

En esta formulación, un estado es una (n+1)-tupla
tal que:
● (c₁ es la ciudad inicial).
● (c₁ es la ciudad final).
● para todo i ε {2,…,n}, es una ciudad diferente de {c₂,…,cn}.
el cual representa el orden en que se recorren las ciudades: se inicia en
aaaaaaa, luego se visita , y así sucesivamente, hasta visitar a y
finalmente regresar a .
El número total de estados es (n-1).(n-2).….2.1 = (n-1)!

Una acción es un par (i,k) є {2,…,n}², con i<k, que
representa intercambiar de lugar la i-ésima ciudad del tour
por la j-ésima ciudad del tour.

pag 49

function ASCENSIÓN-COLINAS(problema) return estado
    s ← problema.estado-inicial
    do
        S’ ← {problema.resultado(s,a) for
            є problema.acciones(s)}
        s’ ← argmax(problema.f, S’)
        if (problema.f(s’) ≤ problema.f(s)) then return s
    s ← s’

'''