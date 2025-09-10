"""
Implementación de Pila desde cero usando lista enlazada
"""

from .linked_list import LinkedList

class Stack:
    """Pila LIFO (Last In, First Out)"""

    def __init__(self):
        self.items = LinkedList()

    def is_empty(self):
        """Verifica si la pila está vacía"""
        return self.items.is_empty()

    def push(self, item):
        """Agrega un elemento a la cima de la pila"""
        self.items.prepend(item)

    def pop(self):
        """Remueve y retorna el elemento de la cima de la pila"""
        if self.is_empty():
            raise IndexError("La pila está vacía")
        return self.items.remove_at(0)

    def peek(self):
        """Retorna el elemento de la cima sin removerlo"""
        if self.is_empty():
            raise IndexError("La pila está vacía")
        return self.items.get(0)

    def size(self):
        """Retorna el tamaño de la pila"""
        return len(self.items)

    def clear(self):
        """Limpia la pila"""
        self.items.clear()

    def __str__(self):
        """Representación en string de la pila"""
        return f"Stack({self.items})"

    def __len__(self):
        """Retorna el tamaño de la pila"""
        return self.size()
