from grafo import Grafo
from fluxo_maximo import FluxoMaximo

grafo1 = Grafo()
#grafo1.ler('entradas/fluxo_maximo_aula.net')
grafo1.ler('entradas/db4096.net')
#print(grafo1.getArco(1,2))
#grafo1.print()
fluxo = FluxoMaximo(grafo1)