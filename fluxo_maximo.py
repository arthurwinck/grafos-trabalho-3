from grafo import Grafo
from queue import Queue

class FluxoMaximo:
    def __init__(self, grafo):
        self.grafo = grafo
        self.grafoResidual = grafo
        self.configurar()
        s = self.encontrarFonte()
        caminhoAumentante = self.executar(s)
        print(caminhoAumentante)

    def checaFonte(self, i):
        if isinstance(i, int):
            return self.grafo.vertices[i].rotulo == 's' or self.grafo.vertices[i].rotulo == str(len(self.grafo.vertices))
        else:
            return i.rotulo == 's' or i.rotulo == str(len(self.grafo.vertices))

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
    
    def executar(self, s):
        #Recebemos o index da fonte s, então setamos seu visitado para True
        self.v[s] = True
        self.queue.enqueue(self.grafo.vertices[s])
        
        #Propagação das visitas
        while not self.queue.empty():
            u = self.queue.dequeue()
            print(f"U = {u.index}")
            #Ajuste da função vizinhos para que possamos pegar apenas arcos saintes (pode apenas estar saindo do vértice em questão)
            vizinhos = []

            for j in range(len(self.grafo.arestas)):
                if self.grafo.arestas[j].vertices[0] == u.index:
                    vizinhos.append(self.grafo.arestas[j].vertices[1])

            for vizinho in vizinhos:
                # Se v não foi visitado e capacidade de fluxo de (u,v) é maior que 0
                if self.v[vizinho-1] == False and self.grafo.getAresta(u.index, vizinho):
                    self.v[vizinho-1] = True
                    self.a[vizinho-1] = u


                    # Encontramos o sorvedouro - Vamos criar o caminho aumentante e colocar o sorvedouro
                    if self.grafo.vertices[vizinho-1].rotulo == 't':
                        caminhoAumentante = ['t',]
                        vertice = vizinho-1
                        verticeObj = self.grafo.vertices[vertice]
                        # Enquanto não chegarmos na fonte, estaremos fazendo o caminho de volta
                        # a ela. E por isso vamos adicionando os vértices ao caminho
                        while True:
                            verticeObj = self.a[verticeObj.index-1]
                            print(verticeObj.rotulo)
                            caminhoAumentante.append(verticeObj.rotulo)

                            if self.checaFonte(verticeObj):
                                break

                        return caminhoAumentante[::-1]

                    self.queue.enqueue(self.grafo.vertices[vizinho-1])

        