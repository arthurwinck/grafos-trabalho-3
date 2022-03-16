from grafo import Grafo
from fluxo_maximo import FluxoMaximo

grafo1 = Grafo()
grafo1.ler('entradas/db4096.net')
#grafo1.print()
fluxo = FluxoMaximo(grafo1)