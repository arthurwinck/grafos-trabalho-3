from grafo import Grafo, Aresta, Vertice


def quicksortMatriz(matriz, low, high):
        if len(matriz) == 1:
            return matriz
        if low < high:

            pi = partition(matriz,low,high)

            quicksortMatriz(matriz, low, pi-1)
            quicksortMatriz(matriz,pi+1, high)

def partition(matriz,low,high):
    i = low - 1
    pivot = matriz[high][2] 

    for j in range(low,high):

        if matriz[j][2] <= pivot:
            i += 1
            matriz[i], matriz[j] = matriz[j], matriz[i]

    matriz[i+1], matriz[high] = matriz[high], matriz[i+1]
    return (i+1)

class CompFortConexas:
    def __init__(self, grafo):
        self.grafo = grafo
        self.grafoTransp = None
        self.componentes = []
        self.tempo = 0
        self.executar()
        
    # Função DFS Visit, que exectutará em cima da matrizDFS onde estão as informações de auxiliares do algoritmo
    def DFSVisit(self, k):
        self.matrizDFS[k][0] = True
        self.tempo += 1
        self.matrizDFS[k][1] = self.tempo

        vizinhos = []

        # Descobrir os arcos que saem de k para outros vértices // Respeitar o fato do grafo ser dirigido
        # Por conta de como implementamos o grafo, o atributo é chamado de aresta
        # mas, podemos utilizá-la como arco facilmente interpretando ela se fosse um arco de K para J. Não aceitamos ela como J -> K
        for j in range(len(self.grafo.arestas)):
            if self.grafo.arestas[j].vertices[0] == k+1:
                vizinhos.append(self.grafo.arestas[j].vertices[1])

        for m in range(len(vizinhos)):
            viz = vizinhos[m]
            
            if self.matrizDFS[viz-1][0] == False:
                self.matrizDFS[viz-1][3] = self.matrizDFS[k][4]
                self.DFSVisit(viz-1)

        self.tempo += 1
        self.matrizDFS[k][2] = self.tempo

    # Função de DFSVisit para o DFS alterado, que irá executar em cima da matrizDFS alterada.
    def DFSVisitAlt(self, k):
        self.matrizDFSAlt[k][0] = True
        self.tempo += 1
        self.matrizDFSAlt[k][1] = self.tempo

        vizinhos = []

        # Descobrir os arcos que saem de k para outros vértices // Respeitar o fato do grafo ser dirigido
        for j in range(len(self.grafoTransp.arestas)):
            if self.grafoTransp.arestas[j].vertices[0] == k+1:
                vizinhos.append(self.grafoTransp.arestas[j].vertices[1])

        for m in range(len(vizinhos)):
            viz = vizinhos[m]
            
            if self.matrizDFSAlt[viz-1][0] == False:
                self.matrizDFSAlt[viz-1][3] = self.matrizDFSAlt[k][4]
                self.DFSVisitAlt(viz-1)

        self.tempo += 1
        self.matrizDFSAlt[k][2] = self.tempo

    # Função DFS que executará com DFSVisit
    def DFS(self):
        # Instanciação da nossa matriz auxiliar: Cv, Tv, Fv, Av e mais um novo elemento identidade, identificando o vértice associado a linha da matriz auxiliar
        self.matrizDFS = [[False, float('inf'), float('inf'), None, self.grafo.vertices[i].rotulo] for i in range(self.grafo.qtdVertices())]

        self.tempo = 0

        for k in range(self.grafo.qtdVertices()):
            if self.matrizDFS[k][0] == False:
                self.DFSVisit(k)

    # Função DFS Alterado que executa em cima da lista de vértices em ordem decrescente de Fv
    def DFSAlterado(self):
        # Restauração dos valores iniciais da matriz auxiliar, gerando a matrizDFSAlt inicial (cópia de MatrizDFS depois de executar quicksort e reverse em cima de Fv)
        for i in range(self.grafo.qtdVertices()):
            # matrizDFS[i] = Cv, Tv, Fv, Av
            self.matrizDFSAlt[i][0] = False 
            self.matrizDFSAlt[i][1] = float('inf') 
            self.matrizDFSAlt[i][2] = float('inf') 
            self.matrizDFSAlt[i][3] = None

        self.tempo = 0

        # Esse for não vai funcionar, é necessário ordenar a matriz por valor de Fv descendente e realizar o for
        for k in range(self.grafoTransp.qtdVertices()):
            if self.matrizDFSAlt[k][0] == False:    
                self.DFSVisitAlt(k)

    def executar(self):
        self.DFS()
        #Criar o grafo transposto
        arestasTransp = []
        
        for aresta in self.grafo.arestas:
            arestasTransp.append(Aresta([aresta.vertices[1], aresta.vertices[0]], aresta.peso))

        # Criação do Grafo Transposto, girando as arestas
        self.grafoTransp = Grafo()
        self.grafoTransp.arestas = arestasTransp
        self.grafoTransp.vertices = self.grafo.vertices

        # Cópia de matrizDFS para matrizDFSAlt
        self.matrizDFSAlt = self.matrizDFS
        
        #Realização de quicksort pelo Fv e depois reverso, para ordem decresente
        quicksortMatriz(self.matrizDFSAlt, 0, len(self.matrizDFSAlt) - 1)
        self.matrizDFSAlt.reverse()

        # Execução de DFS Alterado utilizando DFSVisitAlt e a matriz matrizDFSAlt
        self.DFSAlterado()

        #print(self.matrizDFSAlt)

        for i in range(len(self.matrizDFSAlt)):
            print(f"Elemento: {self.matrizDFSAlt[i][4]} Antecessor: {self.matrizDFSAlt[i][3]}")

        # Criação da representação das árvores

                        

