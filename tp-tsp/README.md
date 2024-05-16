# TP: Problema del Viajante (TSP)
Solver de TSP en Python. 

Consultar enunciado en el campus virtual de la materia.

## Algoritmos ya implementados
1. Ascensión de colinas (hill climbing).

## Algoritmos a implementar
2. Ascensión de colinas con reinicio aleatorio (random restart hill climbing).
3. Búsqueda tabú (tabu search).

## Requerimientos
* Python 3.10 o superior (https://www.python.org/downloads/).
* tsplib95.
* matplotlib.

## Criterios para la resolusión de los algoritmos
Se parametrizan las variables en funcióm del número de nodos del grafo

2. Ascensión de colinas con reinicio aleatorio (random restart hill climbing). 
Para los grafos con menor número de nodos, alcanza el valor objetivo con reinicios = nro_nodos
Para los grafos con mayor número de nodos, alcanza el valor objetivo con reinicios = nro_nodos * 2
reinicios = round(number_nodes * 2)

3. Búsqueda tabú (tabu search)
Experimentalmente se encuentran los valores objetivos de los distintos grafos:
* burma14.tsp     -3323
* ulysses16.tsp   -6859
* ar24.tsp        -86585
* att48.tsp       -10653
* berlin52.tsp    -7542

y los tamaños de la lista tabú para alcanzarlos.

En función de esos resultados, se busca la ecuación de una recta que funcione para los grafos: ar24.tsp y att48.tsp
tamaño lista tabú = round(number_nodes * 5 / 24 + 15)

Para los grafos con menor número de nodos el valor objetivo se encuentra con mayor facilidad.
Para los grafos con mayor número de nodos el valor objetivo no se encuentra con esta solución.

En general, a medida que aumenta el número de nodos en el grafo puede necesitarse una lista tabú de mayor tamaño,
pero la relación no es lineal porque depende de la disposición específica de los puntos (si están más concentrados o más alejados). Para lograr mejores soluciones existen distintas técnicas que no se implementan en este TP.

Se observa que al tratarse de un problema de distancias, la elección de una acción aleatoria, no es tal, porque difícilmente dos o más cálculos de distancia den un mismo resultado y pueden descartarse soluciones muy próximas.

Por ese motivo y previo a encontrar mejores parámetros para el algoritmo Tabú (en ar24.tsp), se desarrolla una variante del algoritmo tabú que elige entre un determinado número de mejores valores objetivos que no estén en la lista tabú. Esta variante está ajustada para el grafo ar24.tsp y se basa en la estrategia de ampliar la definición de vecindad para explorar otras soluciones cuando la búqueda tabú se atasca.


