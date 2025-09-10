"""
Implementación de Árbol AVL desde cero para tabla de rutas
"""

class AVLNode:
    """Nodo del árbol AVL"""
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    """Árbol AVL balanceado para tabla de rutas"""

    def __init__(self):
        self.root = None
        self.rotations = {"LL": 0, "LR": 0, "RL": 0, "RR": 0}
        self.nodes_count = 0

    def get_height(self, node):
        """Obtiene la altura de un nodo"""
        if not node:
            return 0
        return node.height

    def get_balance(self, node):
        """Obtiene el factor de balance de un nodo"""
        if not node:
            return 0
        return self.get_height(node.left) - self.get_height(node.right)

    def update_height(self, node):
        """Actualiza la altura de un nodo"""
        if node:
            node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def rotate_right(self, y):
        """Rotación simple a la derecha (LL)"""
        x = y.left
        T2 = x.right

        x.right = y
        y.left = T2

        self.update_height(y)
        self.update_height(x)

        self.rotations["LL"] += 1
        return x

    def rotate_left(self, x):
        """Rotación simple a la izquierda (RR)"""
        y = x.right
        T2 = y.left

        y.left = x
        x.right = T2

        self.update_height(x)
        self.update_height(y)

        self.rotations["RR"] += 1
        return y

    def rotate_left_right(self, node):
        """Rotación doble izquierda-derecha (LR)"""
        node.left = self.rotate_left(node.left)
        result = self.rotate_right(node)
        self.rotations["LR"] += 1
        return result

    def rotate_right_left(self, node):
        """Rotación doble derecha-izquierda (RL)"""
        node.right = self.rotate_right(node.right)
        result = self.rotate_left(node)
        self.rotations["RL"] += 1
        return result

    def balance(self, node):
        """Balancea el árbol después de inserción/eliminación"""
        if not node:
            return node

        self.update_height(node)
        balance = self.get_balance(node)

        # Caso LL
        if balance > 1 and self.get_balance(node.left) >= 0:
            return self.rotate_right(node)

        # Caso LR
        if balance > 1 and self.get_balance(node.left) < 0:
            return self.rotate_left_right(node)

        # Caso RR
        if balance < -1 and self.get_balance(node.right) <= 0:
            return self.rotate_left(node)

        # Caso RL
        if balance < -1 and self.get_balance(node.right) > 0:
            return self.rotate_right_left(node)

        return node

    def insert(self, root, key, value=None):
        """Inserta un nodo en el árbol AVL"""
        if not root:
            self.nodes_count += 1
            return AVLNode(key, value)

        if key < root.key:
            root.left = self.insert(root.left, key, value)
        elif key > root.key:
            root.right = self.insert(root.right, key, value)
        else:
            # Actualizar valor si la clave ya existe
            root.value = value
            return root

        return self.balance(root)

    def insert_key(self, key, value=None):
        """Método público para insertar"""
        self.root = self.insert(self.root, key, value)

    def get_min_value_node(self, node):
        """Encuentra el nodo con valor mínimo"""
        current = node
        while current.left:
            current = current.left
        return current

    def delete(self, root, key):
        """Elimina un nodo del árbol AVL"""
        if not root:
            return root

        if key < root.key:
            root.left = self.delete(root.left, key)
        elif key > root.key:
            root.right = self.delete(root.right, key)
        else:
            # Nodo encontrado
            self.nodes_count -= 1

            # Caso 1: Nodo hoja o con un hijo
            if not root.left:
                return root.right
            elif not root.right:
                return root.left

            # Caso 2: Nodo con dos hijos
            temp = self.get_min_value_node(root.right)
            root.key = temp.key
            root.value = temp.value
            root.right = self.delete(root.right, temp.key)

        return self.balance(root)

    def delete_key(self, key):
        """Método público para eliminar"""
        self.root = self.delete(self.root, key)

    def search(self, root, key):
        """Busca un nodo en el árbol"""
        if not root or root.key == key:
            return root

        if key < root.key:
            return self.search(root.left, key)
        return self.search(root.right, key)

    def search_key(self, key):
        """Método público para buscar"""
        return self.search(self.root, key)

    def inorder_traversal(self, node, result):
        """Recorrido inorder del árbol"""
        if node:
            self.inorder_traversal(node.left, result)
            result.append((node.key, node.value))
            self.inorder_traversal(node.right, result)

    def get_all_routes(self):
        """Obtiene todas las rutas ordenadas"""
        result = []
        self.inorder_traversal(self.root, result)
        return result

    def get_tree_height(self):
        """Obtiene la altura del árbol"""
        return self.get_height(self.root)

    def get_stats(self):
        """Obtiene estadísticas del árbol"""
        return {
            "nodes": self.nodes_count,
            "height": self.get_tree_height(),
            "rotations": self.rotations.copy()
        }

    def print_tree(self, node=None, level=0, prefix="Root: "):
        """Imprime el árbol en forma visual"""
        if node is None:
            node = self.root

        if node:
            print("  " * level + prefix + f"[{node.key}]")
            if node.left:
                self.print_tree(node.left, level + 1, "L: ")
            if node.right:
                self.print_tree(node.right, level + 1, "R: ")

    def clear_rotations(self):
        """Reinicia el contador de rotaciones"""
        self.rotations = {"LL": 0, "LR": 0, "RL": 0, "RR": 0}
