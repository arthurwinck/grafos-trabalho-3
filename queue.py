
from msilib.schema import Error


class Queue:
    def __init__(self):
        self.lista = []

    def enqueue(self, elem):
        self.lista.append(elem)

    def dequeue(self):
        if not self.empty():
            return self.lista.pop(0)
        else:
            print("Fila vazia!")

    def empty(self):
        return len(self.lista) == 0