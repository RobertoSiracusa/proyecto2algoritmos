"""
Implementación de Cola desde cero usando lista enlazada
"""

from .linked_list import LinkedList

class Queue:
    """Cola FIFO (First In, First Out)"""

    def __init__(self):
        self.items = LinkedList()

    def is_empty(self):
        """Verifica si la cola está vacía"""
        return self.items.is_empty()

    def enqueue(self, item):
        """Agrega un elemento al final de la cola"""
        self.items.append(item)

    def dequeue(self):
        """Remueve y retorna el elemento del frente de la cola"""
        if self.is_empty():
            raise IndexError("La cola está vacía")
        return self.items.remove_at(0)

    def peek(self):
        """Retorna el elemento del frente sin removerlo"""
        if self.is_empty():
            raise IndexError("La cola está vacía")
        return self.items.get(0)

    def size(self):
        """Retorna el tamaño de la cola"""
        return len(self.items)

    def clear(self):
        """Limpia la cola"""
        self.items.clear()

    def __str__(self):
        """Representación en string de la cola"""
        return f"Queue({self.items})"

    def __len__(self):
        """Retorna el tamaño de la cola"""
        return self.size()
