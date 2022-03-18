from grafo import Grafo
from fluxo_maximo import FluxoMaximo
from lawler import lawler
from hopcroft_karp import hopcroft_karp

#Algoritmo de Fluxo Máximo / Ford-Fulkerson / Edmonds-Karp
print(" Fluxo Máximo --------------------------------------------------------------")
grafo1 = Grafo()
grafo1.ler('entradas/entrada_aula.net')
fluxo = FluxoMaximo(grafo1)
print("Emparelhamento --------------------------------------------------------------")
#Algoritmo de Hopcroft-Karp
grafo2 = Grafo()
grafo2.ler('entradas/gr128_10-alt.gr')
ordenacao = hopcroft_karp(grafo2)

#Algoritmo de Lawler
print("Coloração --------------------------------------------------------------")
grafo3 = Grafo()
grafo3.ler("entradas/lawler.net")
lawler(grafo3)

