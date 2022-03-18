from grafo import Grafo, Vertice, Aresta

INF = 99999999999999

def subset(A):
    subsets = []
    f = {}
    n = len(A)
    for b in range(0, 1 << n):
        si = []
        for i in range(0, n):
            if (b&(1<<i)):
                si.append(A[i])
        f[tuple(si)] = b
        subsets.append(si)
    return subsets, f

def lawler(grafo):
    X = [0 for _ in range(0, 2**grafo.qtdVertices())]
    X[0] = 0   #Isso eh so pra se parecer com o codigo das anotacoes, sem utilidade pratica.
    S, f = subset(grafo.vertices)

    S1 = S.copy()
    S1.remove([])
    for S1_element in S1:
        s = f[tuple(S1_element)]
        X[s] = INF
        vertices = []
        arestas = []
        for element in S1_element:
            vertices.append(element)
        for aresta in grafo.arestas:
            u_indice, v_indice = aresta.vertices
            u, v = grafo.indice_to_vertice[u_indice], grafo.indice_to_vertice[v_indice]
            if u in vertices and v in vertices:
                arestas.append((u, v))
                print("h")
        
        
        
grafo1 = Grafo()
grafo1.ler("entradas/lawler.net")
lawler(grafo1)
