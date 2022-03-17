from grafo import Grafo, Aresta
from queue import Queue

#O FluxoMaximo aceita grafos que estejam com rotulos indicando fonte com 's' e sorvedouro com 't' ou
#grafos que possuem como fonte o seu primeiro vértice = 1 e o seu último vértice como sorvedouro
class FluxoMaximo:
    def __init__(self, grafo):
        self.grafo = grafo
        self.grafoResidual = Grafo()
        self.fluxoMaximo = 0
        self.configurar()
        self.executar()

    def checaFonte(self, i):
        if isinstance(i, int):
            return self.grafo.vertices[i].rotulo == 's' or self.grafo.vertices[i].rotulo == '1'
        else:
            return i.rotulo == 's' or i.rotulo == '1'

    def checaSorvedouro(self, i):
        if isinstance(i, int):
            return self.grafo.vertices[i].rotulo == 't' or self.grafo.vertices[i].rotulo == str(len(self.grafo.vertices))
        else:
            return i.rotulo == 't' or i.rotulo == str(len(self.grafo.vertices))

    def encontrarFonte(self):
        for i in range(len(self.grafo.vertices)):
            if self.checaFonte(i) == True:
                return i
        
        raise Exception('Não foi possível achar a fonte')

    def configurar(self):
        #Criar array de visitados
        self.v = [False for i in range(len(self.grafo.vertices))]
        #Criar array de antecedentes
        self.a = [None for i in range(len(self.grafo.vertices))]
        #Criar array de fluxo
        self.f = [0 for i in range(len(self.grafo.arestas))]
        
        #Criando a fila
        self.queue = Queue()

        for vertice in self.grafo.vertices:
             self.grafoResidual.adicionarVertice(vertice)
        for aresta in self.grafo.arestas:
            #Adicionar arestas originais
            self.grafoResidual.adicionarAresta(aresta)
            #Adicionar arestas de volta no grafo residual
            #Para cada arco (u,v) E A tem-se um arco invertido em Af com capacidade cf((v,u)) = f((u,v)) 
            self.grafoResidual.adicionarAresta(Aresta([aresta.vertices[1],aresta.vertices[0]], self.f[self.grafo.arestas.index(aresta)]))
    
    def checaFluxoMin(self, caminho):
        
        fluxoMin = None
        fluxoLista = []

        for i in range(1,len(caminho)):
            arco = self.grafoResidual.getArco(caminho[i-1].index, caminho[i].index)
            arcoRetorno = self.grafoResidual.getArco(caminho[i].index, caminho[i-1].index)

            fluxoLista.append(arco)
            fluxoLista.append(arcoRetorno)


            if fluxoMin == None:
                fluxoMin = arco.peso

            if arco != None:
                if fluxoMin > arco.peso:
                    fluxoMin = arco.peso

        return fluxoMin, fluxoLista


    #Executa o algoritmo de Ford-Fulkerson
    def executar(self):
        
        # print("---------------")         
        # print(self.f)
        # self.grafoResidual.print()
        # print("---------------")
        
        #Encontrar a fonte
        s = self.encontrarFonte()
        
        #Criar array de fluxo (função de fluxo)
        

        # Enquanto existir um caminho aumentante p na rede residual s a t
        while True:
            caminho = self.encontrarCaminhoAumentante(s)

            if caminho == None:
                break

            fluxoMin, listaArcos = self.checaFluxoMin(caminho)
            
            for arco in listaArcos:
                arc = self.grafo.getArco(arco.vertices[0],arco.vertices[1])

                if arc != None:
                    self.f[self.grafo.arestas.index(arco)] = self.f[self.grafo.arestas.index(arco)] + fluxoMin
                    arco.peso = arco.peso - fluxoMin
                else:
                    #self.f[(listaArcos.index(arco))*2] = self.f[(listaArcos.index(arco))*2] - fluxoMin
                    arco.peso = arco.peso + fluxoMin
            
            self.fluxoMaximo += fluxoMin

            # Atualização do fluxo da cada um dos vértices
            # for i in range(len(self.grafo.arestas)):
            #     print(self.a[ultimo.index-1].index-1, ultimo.index)
            #     if self.grafo.getArco(self.a[ultimo.index-1].index-1, ultimo.index):
            #             self.f[i] = self.f[i] + fluxoMin
            #     else:
            #         self.f[i*2] = self.f[i*2] - fluxoMin
                    
        #     print("---------------")         
        #     print(self.f)
        #     self.grafoResidual.print()
            for i in range(len(listaArcos)):
                print(listaArcos[i].vertices, end=',')
        #     print("\n")
            print(fluxoMin)
        #     print("---------------")

        # print(f"Fluxo máximo = {self.fluxoMaximo}")

    #Retorna um caminho aumentante ou retorna None
    def encontrarCaminhoAumentante(self, s):
        #Recebemos o index da fonte s, então setamos seu visitado para True
        self.v = [False for i in range(len(self.grafo.vertices))]
        self.v[s] = True
        self.queue.enqueue(self.grafo.vertices[s])
        
        #Propagação das visitas
        while not self.queue.empty():
            u = self.queue.dequeue()
            #print(f"U = {u.index}")

            #Ajuste da função vizinhos para que possamos pegar apenas arcos saintes (pode apenas estar saindo do vértice em questão)
            vizinhos = []
            for aresta in self.grafo.arestas:
                if aresta.vertices[0] == u.index:
                    vizinhos.append(aresta.vertices[1])

            #print(f"Vizinhos = {vizinhos}")

            for vizinho in vizinhos:
                # Se v não foi visitado e capacidade de fluxo de (u,v) é maior que 0
                if self.v[vizinho-1] == False and self.grafoResidual.getArco(u.index, vizinho).peso > 0:
                    self.v[vizinho-1] = True
                    self.a[vizinho-1] = u

                    # Encontramos o sorvedouro - Vamos criar o caminho aumentante e colocar o sorvedouro
                    #if self.grafo.vertices[vizinho-1].rotulo == 't':
                    if self.checaSorvedouro(vizinho-1):
                        vertice = vizinho-1
                        verticeObj = self.grafo.vertices[vertice]
                        caminhoAumentante = [verticeObj]
                        # Enquanto não chegarmos na fonte, estaremos fazendo o caminho de volta
                        # a ela. E por isso vamos adicionando os vértices ao caminho
                        while True:
                            #self.grafoResidual.adicionarAresta(Aresta([self.a[verticeObj.index-1],verticeObj.index]))
                            verticeObj = self.a[verticeObj.index-1]
                            caminhoAumentante.append(verticeObj)

                            if self.checaFonte(verticeObj):
                                break

                        return caminhoAumentante[::-1]

                    self.queue.enqueue(self.grafo.vertices[vizinho-1])

        