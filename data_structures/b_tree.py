"""
Implementación de B-Tree desde cero para índice persistente
"""

class BTreeNode:
    """Nodo del B-Tree"""
    def __init__(self, leaf=False):
        self.leaf = leaf
        self.keys = []
        self.children = []
        self.values = []  # Para almacenar los valores asociados a las claves

class BTree:
    """B-Tree para índice persistente de configuraciones"""

    def __init__(self, order=4):
        self.root = BTreeNode(leaf=True)
        self.order = order  # Orden del B-Tree (máximo número de hijos)
        self.nodes_count = 1
        self.splits = 0
        self.merges = 0

    def search(self, key, node=None):
        """Busca una clave en el B-Tree"""
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node.values[i]

        if node.leaf:
            return None

        return self.search(key, node.children[i])

    def split_child(self, parent, child_index):
        """Divide un nodo hijo cuando está lleno"""
        order = self.order
        child = parent.children[child_index]

        # Crear nuevo nodo
        new_node = BTreeNode(leaf=child.leaf)
        self.nodes_count += 1
        self.splits += 1

        # Mover la clave del medio al padre
        mid_key = child.keys[order // 2]
        mid_value = child.values[order // 2]

        parent.keys.insert(child_index, mid_key)
        parent.values.insert(child_index, mid_value)

        # Mover las claves de la derecha al nuevo nodo
        new_node.keys = child.keys[order // 2 + 1:]
        new_node.values = child.values[order // 2 + 1:]

        # Mover los hijos de la derecha al nuevo nodo
        if not child.leaf:
            new_node.children = child.children[order // 2 + 1:]
            child.children = child.children[:order // 2 + 1]

        # Actualizar el nodo original
        child.keys = child.keys[:order // 2]
        child.values = child.values[:order // 2]

        # Insertar el nuevo nodo en los hijos del padre
        parent.children.insert(child_index + 1, new_node)

    def insert_non_full(self, node, key, value):
        """Inserta en un nodo que no está lleno"""
        if node.leaf:
            # Encontrar la posición correcta
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1

            # Insertar la clave y valor
            node.keys.insert(i, key)
            node.values.insert(i, value)
        else:
            # Encontrar el hijo correcto
            i = 0
            while i < len(node.keys) and key > node.keys[i]:
                i += 1

            # Si el hijo está lleno, dividirlo
            if len(node.children[i].keys) == self.order - 1:
                self.split_child(node, i)
                if key > node.keys[i]:
                    i += 1

            self.insert_non_full(node.children[i], key, value)

    def insert(self, key, value):
        """Inserta una clave-valor en el B-Tree"""
        root = self.root

        # Si la raíz está llena
        if len(root.keys) == self.order - 1:
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            self.split_child(new_root, 0)
            self.root = new_root
            self.nodes_count += 1

        self.insert_non_full(self.root, key, value)

    def merge_nodes(self, parent, left_index):
        """Fusiona dos nodos hermanos"""
        left = parent.children[left_index]
        right = parent.children[left_index + 1]

        # Mover la clave del padre al nodo izquierdo
        left.keys.append(parent.keys[left_index])
        left.values.append(parent.values[left_index])

        # Mover todas las claves y valores del nodo derecho al izquierdo
        left.keys.extend(right.keys)
        left.values.extend(right.values)

        # Mover los hijos si no es hoja
        if not left.leaf:
            left.children.extend(right.children)

        # Remover la clave del padre y el nodo derecho
        parent.keys.pop(left_index)
        parent.values.pop(left_index)
        parent.children.pop(left_index + 1)

        self.merges += 1

    def borrow_from_prev(self, parent, child_index):
        """Toma prestado del hermano izquierdo"""
        child = parent.children[child_index]
        sibling = parent.children[child_index - 1]

        # Mover la clave del padre al hijo
        child.keys.insert(0, parent.keys[child_index - 1])
        child.values.insert(0, parent.values[child_index - 1])

        # Mover la última clave del hermano al padre
        parent.keys[child_index - 1] = sibling.keys.pop()
        parent.values[child_index - 1] = sibling.values.pop()

        # Mover los hijos si no es hoja
        if not child.leaf:
            child.children.insert(0, sibling.children.pop())

    def borrow_from_next(self, parent, child_index):
        """Toma prestado del hermano derecho"""
        child = parent.children[child_index]
        sibling = parent.children[child_index + 1]

        # Mover la clave del padre al hijo
        child.keys.append(parent.keys[child_index])
        child.values.append(parent.values[child_index])

        # Mover la primera clave del hermano al padre
        parent.keys[child_index] = sibling.keys.pop(0)
        parent.values[child_index] = sibling.values.pop(0)

        # Mover los hijos si no es hoja
        if not child.leaf:
            child.children.append(sibling.children.pop(0))

    def fill_child(self, parent, child_index):
        """Llena un nodo hijo que tiene menos claves que el mínimo"""
        if child_index > 0 and len(parent.children[child_index - 1].keys) >= self.order // 2:
            self.borrow_from_prev(parent, child_index)
        elif child_index < len(parent.children) - 1 and len(parent.children[child_index + 1].keys) >= self.order // 2:
            self.borrow_from_next(parent, child_index)
        else:
            if child_index > 0:
                self.merge_nodes(parent, child_index - 1)
            else:
                self.merge_nodes(parent, child_index)

    def delete_helper(self, node, key):
        """Ayudante recursivo para eliminación"""
        min_keys = self.order // 2

        # Encontrar la posición de la clave
        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        # Si la clave está en este nodo
        if i < len(node.keys) and node.keys[i] == key:
            if node.leaf:
                # Caso 1: Es una hoja, simplemente eliminar
                node.keys.pop(i)
                node.values.pop(i)
            else:
                # Caso 2: No es hoja
                if len(node.children[i].keys) >= min_keys:
                    # Caso 2a: El hijo izquierdo tiene suficientes claves
                    pred = self.get_predecessor(node.children[i])
                    node.keys[i] = pred[0]
                    node.values[i] = pred[1]
                    self.delete_helper(node.children[i], pred[0])
                elif len(node.children[i + 1].keys) >= min_keys:
                    # Caso 2b: El hijo derecho tiene suficientes claves
                    succ = self.get_successor(node.children[i + 1])
                    node.keys[i] = succ[0]
                    node.values[i] = succ[1]
                    self.delete_helper(node.children[i + 1], succ[0])
                else:
                    # Caso 2c: Ambos hijos tienen el mínimo, fusionar
                    self.merge_nodes(node, i)
                    self.delete_helper(node.children[i], key)
        else:
            # La clave no está en este nodo
            if node.leaf:
                return  # No encontrada

            flag = (i == len(node.keys))

            # Si el hijo no tiene suficientes claves, llenarlo
            if len(node.children[i].keys) < min_keys:
                self.fill_child(node, i)

            # Si el último hijo ha sido fusionado, usar el hijo anterior
            if flag and i > len(node.keys):
                self.delete_helper(node.children[i - 1], key)
            else:
                self.delete_helper(node.children[i], key)

    def get_predecessor(self, node):
        """Obtiene el predecesor de un nodo"""
        current = node
        while not current.leaf:
            current = current.children[-1]
        return (current.keys[-1], current.values[-1])

    def get_successor(self, node):
        """Obtiene el sucesor de un nodo"""
        current = node
        while not current.leaf:
            current = current.children[0]
        return (current.keys[0], current.values[0])

    def delete(self, key):
        """Elimina una clave del B-Tree"""
        if not self.root:
            return

        self.delete_helper(self.root, key)

        # Si la raíz se queda sin claves, hacer que su hijo sea la nueva raíz
        if len(self.root.keys) == 0:
            if not self.root.leaf:
                self.root = self.root.children[0]
                self.nodes_count -= 1
            else:
                self.root = None

    def inorder_traversal(self, node, result):
        """Recorrido inorder del B-Tree"""
        if node:
            i = 0
            for i in range(len(node.keys)):
                if not node.leaf:
                    self.inorder_traversal(node.children[i], result)
                result.append((node.keys[i], node.values[i]))
            if not node.leaf:
                self.inorder_traversal(node.children[i + 1], result)

    def get_all_entries(self):
        """Obtiene todas las entradas ordenadas"""
        result = []
        self.inorder_traversal(self.root, result)
        return result

    def get_height(self, node=None):
        """Calcula la altura del B-Tree"""
        if node is None:
            node = self.root

        if not node:
            return 0

        if node.leaf:
            return 1

        return 1 + self.get_height(node.children[0])

    def get_stats(self):
        """Obtiene estadísticas del B-Tree"""
        return {
            "order": self.order,
            "height": self.get_height(self.root),
            "nodes": self.nodes_count,
            "splits": self.splits,
            "merges": self.merges
        }

    def print_tree(self, node=None, level=0):
        """Imprime el B-Tree"""
        if node is None:
            node = self.root

        if node:
            print("  " * level + f"Node: {node.keys}")
            if not node.leaf:
                for i, child in enumerate(node.children):
                    print("  " * level + f"Child {i}:")
                    self.print_tree(child, level + 1)
