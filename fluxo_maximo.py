from grafo import Grafo, Aresta
from queue import Queue

#O FluxoMaximo aceita grafos que estejam com rotulos indicando fonte com 's' e sorvedouro com 't' ou
#grafos que possuem como fonte o seu primeiro vértice = 1 e o seu último vértice como sorvedouro
class FluxoMaximo:
    def __init__(self, grafo):
        self.grafo = grafo
        self.grafoResidual = grafo
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
        #Criando a fila
        self.queue = Queue()
    
    def checaFluxoMin(self, caminho):
        
        fluxoMin = None
        fluxoLista = []

        for i in range(1,len(caminho)):
            arco = self.grafo.getArco(caminho[i-1].index, caminho[i].index)
            fluxoLista.append(arco)
            print(caminho[i-1].index, caminho[i].index, arco.peso, fluxoMin)

            if fluxoMin == None:
                print(f"None -> {arco.peso}")
                fluxoMin = arco.peso

            if arco != None:
                if fluxoMin > arco.peso:
                    (f"Maior -> {arco.peso}")
                    fluxoMin = arco.peso

        return fluxoMin, fluxoLista


    #Executa o algoritmo de Ford-Fulkerson
    def executar(self):
        #Encontrar a fonte
        s = self.encontrarFonte()
        
        #Criar array de fluxo (função de fluxo)
        self.f = [0 for i in range(len(self.grafo.arestas)*2)]

        # Enquanto existir um caminho aumentante p na rede residual s a t
        while True:
            caminho = self.encontrarCaminhoAumentante(s)

            if caminho == None:
                break

            print(caminho)
            fluxoMin, listaArcos = self.checaFluxoMin(caminho)
            print(fluxoMin)


            ultimo = self.a[-1]
            
            for arco in listaArcos:
                arc = self.grafo.getArco(arco.vertices[0],arco.vertices[1])

                if arc != None:
                    self.f[listaArcos.index(arco)] = self.f[listaArcos.index(arco)] + fluxoMin
                else:
                    self.f[(listaArcos.index(arco))*2] = self.f[(listaArcos.index(arco))*2] - fluxoMin
            
            # Atualização do fluxo da cada um dos vértices
            # for i in range(len(self.grafo.arestas)):
            #     print(self.a[ultimo.index-1].index-1, ultimo.index)
            #     if self.grafo.getArco(self.a[ultimo.index-1].index-1, ultimo.index):
            #             self.f[i] = self.f[i] + fluxoMin
            #     else:
            #         self.f[i*2] = self.f[i*2] - fluxoMin
                    
                             
        print(self.f)
        self.grafo.print()

    #Retorna um caminho aumentante ou retorna None
    def encontrarCaminhoAumentante(self, s):
        #Recebemos o index da fonte s, então setamos seu visitado para True
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
                if self.v[vizinho-1] == False and self.grafo.getAresta(u.index, vizinho):
                    self.v[vizinho-1] = True
                    self.a[vizinho-1] = u

                    # Encontramos o sorvedouro - Vamos criar o caminho aumentante e colocar o sorvedouro
                    #if self.grafo.vertices[vizinho-1].rotulo == 't':
                    if self.checaSorvedouro(vizinho-1):
                        vertice = vizinho-1
                        verticeObj = self.grafo.vertices[vertice]
                        print(verticeObj.rotulo)
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

        