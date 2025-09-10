"""
Implementación de Lista Enlazada desde cero
"""

class Node:
    """Nodo de la lista enlazada"""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Lista enlazada simple"""

    def __init__(self):
        self.head = None
        self.size = 0

    def is_empty(self):
        """Verifica si la lista está vacía"""
        return self.head is None

    def append(self, data):
        """Agrega un elemento al final de la lista"""
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_node
        self.size += 1

    def prepend(self, data):
        """Agrega un elemento al inicio de la lista"""
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1

    def insert_at(self, index, data):
        """Inserta un elemento en una posición específica"""
        if index < 0 or index > self.size:
            raise IndexError("Índice fuera de rango")

        if index == 0:
            self.prepend(data)
            return

        new_node = Node(data)
        current = self.head
        for i in range(index - 1):
            current = current.next

        new_node.next = current.next
        current.next = new_node
        self.size += 1

    def remove_at(self, index):
        """Remueve un elemento en una posición específica"""
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")

        if index == 0:
            data = self.head.data
            self.head = self.head.next
            self.size -= 1
            return data

        current = self.head
        for i in range(index - 1):
            current = current.next

        data = current.next.data
        current.next = current.next.next
        self.size -= 1
        return data

    def get(self, index):
        """Obtiene el elemento en una posición específica"""
        if index < 0 or index >= self.size:
            raise IndexError("Índice fuera de rango")

        current = self.head
        for i in range(index):
            current = current.next
        return current.data

    def index_of(self, data):
        """Encuentra el índice de un elemento"""
        current = self.head
        index = 0
        while current:
            if current.data == data:
                return index
            current = current.next
            index += 1
        return -1

    def contains(self, data):
        """Verifica si un elemento existe en la lista"""
        return self.index_of(data) != -1

    def clear(self):
        """Limpia la lista"""
        self.head = None
        self.size = 0

    def __len__(self):
        """Retorna el tamaño de la lista"""
        return self.size

    def __str__(self):
        """Representación en string de la lista"""
        if self.is_empty():
            return "[]"

        result = []
        current = self.head
        while current:
            result.append(str(current.data))
            current = current.next
        return "[" + " -> ".join(result) + "]"

    def __iter__(self):
        """Iterador para la lista"""
        current = self.head
        while current:
            yield current.data
            current = current.next
