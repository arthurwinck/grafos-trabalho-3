from grafo import Grafo

def hopcroft_karp(grafo):
    distancias = [float("inf") for x in range(len(grafo.vertices))]
    mates = [None for x in range(len(grafo.vertices))]
    distNone = [0]

    X = (int)(grafo.qtdVertices()/2 - 1)
    m = 0
    while(busca_em_largura_emparelhamento(grafo, mates, distancias, distNone)):
        for x in range(X+1):
            if mates[x] == None:
                if busca_em_profundidade_emparelhamento(grafo, mates, x, distancias, distNone):
                    m += 1

    print(f"Emparelhamento máximo: {m}")
    print(f"Arestas: {mates}")

def busca_em_largura_emparelhamento(grafo, mates, distancias, distNone):
        Q = []
        X = (int)(grafo.qtdVertices()/2 - 1)

        INF = float("inf")

        for x in range(X+1):
            if mates[x]== None:
                distancias[x] = 0
                Q.append(x)
            else:
                distancias[x] = INF

        distNone[0] = INF
        while len(Q) > 0:
            x = Q.pop()
            x += 1
            if distancias[x+1] < distNone[0]: 
                for y in grafo.vizinhos(x):
                    if mates[y-1] == None:
                        if distNone[0] == INF:
                            distNone[0] = distancias[x] + 1
                    else:
                        if distancias[mates[y]] == INF:
                            distancias[mates[y]] = distancias[x] + 1
                            Q.append(mates[y])

        return distNone[0] != INF      

def busca_em_profundidade_emparelhamento(grafo, mates, x, distancias, distNone):
    INF = float("inf")
    
    if x != None:
        for y in grafo.vizinhos(x+1):
            if mates[y-1] == None:
                if distNone[0] == distancias[x] + 1:
                    if busca_em_profundidade_emparelhamento(grafo, mates, mates[y-1], distancias, distNone):
                        # mates[y] = x
                        mates[x] = y
                        return True
            else:
                if distancias[mates[y]] == distancias[x] + 1:
                    if busca_em_profundidade_emparelhamento(grafo, mates, mates[y-1], distancias, distNone):
                        mates[y] = x
                        mates[x] = y
                        return True
        distancias[x] = INF
        return False

    return True

grafo1 = Grafo()

grafo1.ler('entradas/gr128_10-alt.gr')

ordenacao = hopcroft_karp(grafo1)
