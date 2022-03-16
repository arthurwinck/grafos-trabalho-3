class Grafo:
    def __init__(self):
        #Vértices é uma lista de objetos do tipo vértice
        self.vertices = []
        #Arestas é uma lista de objetos do tipo Aresta
        self.arestas = []
        #Hashmap que retorna o vértice correspondente a determinado índice
        self.indice_to_vertice = {}
        #Hashmap que retorna a aresta correspondente ao par de índices de vértices
        self.pair_to_aresta = {}
        # Matriz de adjacência
        self.matriz = []

    def qtdVertices(self):
        return len(self.vertices)

    def qtdArestas(self):
        return len(self.arestas)
    
    def grau(self, vertice):
        return vertice.grau

    def rotulo(self, vertice):
        #Rotulo ligado a um vértice
        return vertice.rotulo
    
    def vizinhos(self, vertice):
        #Todos os vértices ligados diretamente a esse vértice
        return self.indice_to_vertice[vertice].vizinhos

    def haAresta(self, verticeA, verticeB):
        #Retorna um bool se existe uma aresta entre dois vértices
        return self.matriz[verticeA-1][verticeB-1] == 1

    def peso(self, verticeA, verticeB):
        #Retorna o peso de uma aresta entre vértices A e B, retorna infinto se não exsitir essa aresta
        
        if (verticeA, verticeB) in self.pair_to_aresta:
            return self.pair_to_aresta[(verticeA, verticeB)].peso
        else:
            return float('inf')
    
    def ler(self, arquivo):
        #Carrega um grafo a partir de um input especificado
        arq = open(arquivo, 'r')
        linhas = arq.readlines()

        flag_vertices = False
        flag_arestas = False

        flag_matriz = True

        for linha in linhas:
            
            if linha == '\n':
                break

            elif '*vertices' in linha:
                lista_linha = linha.split(' ')
                flag_vertices = True

            elif '*edges' in linha or '*arcs' in linha:
                lista_linha = linha.split(' ')
                flag_vertices = False
                flag_arestas = True

            elif flag_vertices:
    
                lista_linha = linha.split(' ')

                if lista_linha[1].endswith('\n'):
                    lista_linha[1] = lista_linha[1][:-1]

                indice, rotulo = lista_linha[0], lista_linha[1]

                vertice = Vertice(indice, rotulo)
                self.indice_to_vertice[int(indice)] = vertice
                self.adicionarVertice(vertice)

            elif flag_arestas:

                if flag_matriz:
                    n = self.qtdVertices()
                    self.matriz = [[0 for i in range(n)] for j in range(n)]
                    flag_matriz = False

                lista_linha = linha.split(' ')

                if lista_linha[2].endswith('\n'):
                    lista_linha[2] = lista_linha[2][:-1]


                indice1, indice2 = int(lista_linha[0]), int(lista_linha[1])
                aresta = Aresta([int(indice1), int(indice2)], int(lista_linha[2]))

                self.pair_to_aresta[(indice1, indice2)] = aresta

                # Aumenta o grau dos vértices
                self.indice_to_vertice[indice1].aumentar_grau()
                self.indice_to_vertice[indice2].aumentar_grau()

                # Adiciona os novos vizinhos
                self.indice_to_vertice[indice1].add_vizinho(indice2)
                self.indice_to_vertice[indice2].add_vizinho(indice1)

                # Adiciona na matriz
                self.matriz[indice1-1][indice2-1] = 1
                self.matriz[indice2-1][indice1-1] = 1

                self.adicionarAresta(aresta)


    def adicionarVertice(self, vertice):
        self.vertices.append(vertice)

    def adicionarAresta(self, aresta):
        self.arestas.append(aresta)

    def acharVertice(self, index):
        for vertice in self.vertices:
            if int(vertice.index) == int(index):
                return vertice
            
        return None

    def getAresta(self, verticeA, verticeB):
        #Retorna a aresta entre o vérticeA e vérticeB e se não existir retonar None
        for aresta in self.arestas:
            if verticeA == aresta.vertices[0] and verticeB == aresta.vertices[1]:
                return aresta
            if verticeA == aresta.vertices[1] and verticeB == aresta.vertices[0]:
                return aresta
                    
        return None

    def print(self):
        print("\nPrint do Grafo ------------")
        print("Vértices: --------")
        for vertice in self.vertices:
            print(f"Index: {vertice.index} / Vértice: {vertice.rotulo}")
        print("Arestas: ---------")
        for aresta in self.arestas:
            print(f"Aresta: {aresta.vertices} / Peso: {aresta.peso}")

class Vertice:
    def __init__(self, index, rotulo):
        self.index = int(index)
        self.rotulo = rotulo
        self.grau = 0
        self.vizinhos = []
    
    def aumentar_grau(self):
        self.grau += 1

    def add_vizinho(self, vertice):
        self.vizinhos.append(vertice)

class Aresta:
    def __init__(self, vertices, peso):
        #o atributo vértices de arestas é uma tupla de vértices (rótulo)
        self.vertices = vertices
        self.peso = int(peso)

