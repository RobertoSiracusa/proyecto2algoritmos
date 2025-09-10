"""
Implementación de Trie N-ario desde cero para prefijos IP y políticas
"""

class TrieNode:
    """Nodo del Trie"""
    def __init__(self):
        self.children = {}  # Diccionario para hijos (0-255 para IPv4)
        self.is_end_of_prefix = False
        self.policy = None  # Política asociada al prefijo
        self.prefix = None  # Prefijo completo para este nodo

class Trie:
    """Trie N-ario para prefijos IP y políticas jerárquicas"""

    def __init__(self):
        self.root = TrieNode()
        self.nodes_count = 1

    def _ip_to_parts(self, ip):
        """Convierte IP string a lista de octetos"""
        return [int(x) for x in ip.split('.')]

    def _parts_to_ip(self, parts):
        """Convierte lista de octetos a IP string"""
        return '.'.join(str(x) for x in parts)

    def _get_prefix_length(self, mask):
        """Calcula la longitud del prefijo de la máscara"""
        mask_parts = self._ip_to_parts(mask)
        length = 0
        for octet in mask_parts:
            if octet == 255:
                length += 8
            else:
                # Contar bits en el último octeto
                while octet > 0:
                    length += octet & 1
                    octet >>= 1
                break
        return length

    def insert(self, prefix_ip, mask, policy=None):
        """Inserta un prefijo IP con su política"""
        prefix_parts = self._ip_to_parts(prefix_ip)
        mask_parts = self._ip_to_parts(mask)
        prefix_length = self._get_prefix_length(mask)

        current = self.root

        # Construir el camino según la máscara
        for i in range(len(prefix_parts)):
            octet = prefix_parts[i]
            mask_octet = mask_parts[i]

            # Solo considerar bits según la máscara
            masked_octet = octet & mask_octet

            if masked_octet not in current.children:
                current.children[masked_octet] = TrieNode()
                self.nodes_count += 1

            current = current.children[masked_octet]

            # Si hemos alcanzado la longitud del prefijo, marcar el final
            if i == len(prefix_parts) - 1:
                current.is_end_of_prefix = True
                current.policy = policy
                current.prefix = f"{prefix_ip}/{prefix_length}"

    def search_exact(self, ip):
        """Busca un prefijo exacto"""
        ip_parts = self._ip_to_parts(ip)
        current = self.root

        for octet in ip_parts:
            if octet not in current.children:
                return None
            current = current.children[octet]

        if current.is_end_of_prefix:
            return current.policy
        return None

    def search_longest_prefix(self, ip):
        """Busca el prefijo más largo que coincida (longest prefix match)"""
        ip_parts = self._ip_to_parts(ip)
        current = self.root
        best_match = None
        best_policy = None

        for octet in ip_parts:
            if octet not in current.children:
                break

            current = current.children[octet]

            # Actualizar mejor coincidencia si este es un prefijo válido
            if current.is_end_of_prefix:
                best_match = current.prefix
                best_policy = current.policy

        return best_match, best_policy

    def delete(self, prefix_ip, mask):
        """Elimina un prefijo del Trie"""
        prefix_parts = self._ip_to_parts(prefix_ip)
        mask_parts = self._ip_to_parts(mask)

        def _delete_recursive(node, parts, mask_parts, depth=0):
            if depth == len(parts):
                if node.is_end_of_prefix:
                    node.is_end_of_prefix = False
                    node.policy = None
                    node.prefix = None
                    return len(node.children) == 0
                return False

            octet = parts[depth]
            mask_octet = mask_parts[depth]
            masked_octet = octet & mask_octet

            if masked_octet not in node.children:
                return False

            should_delete_child = _delete_recursive(
                node.children[masked_octet],
                parts,
                mask_parts,
                depth + 1
            )

            if should_delete_child:
                del node.children[masked_octet]
                self.nodes_count -= 1
            else:
                return False

            # Si este nodo ya no tiene hijos y no es fin de prefijo, puede eliminarse
            return len(node.children) == 0 and not node.is_end_of_prefix

        _delete_recursive(self.root, prefix_parts, mask_parts)

    def get_all_prefixes(self):
        """Obtiene todos los prefijos en el Trie"""
        result = []

        def traverse(node, current_path):
            if node.is_end_of_prefix:
                result.append((node.prefix, node.policy))

            for octet, child in node.children.items():
                traverse(child, current_path + [octet])

        traverse(self.root, [])
        return result

    def get_stats(self):
        """Obtiene estadísticas del Trie"""
        return {
            "nodes": self.nodes_count,
            "prefixes": len(self.get_all_prefixes())
        }

    def print_trie(self, node=None, level=0, prefix=""):
        """Imprime el Trie en forma jerárquica"""
        if node is None:
            node = self.root

        indent = "  " * level

        if node.is_end_of_prefix:
            policy_str = f" {{{node.policy}}}" if node.policy else ""
            print(f"{indent}{node.prefix}{policy_str}")

        for octet in sorted(node.children.keys()):
            child = node.children[octet]
            if child.is_end_of_prefix:
                policy_str = f" {{{child.policy}}}" if child.policy else ""
                print(f"{indent}├── {octet}/8{policy_str}")
                self.print_trie(child, level + 1, f"{prefix}.{octet}")
            else:
                print(f"{indent}├── {octet}")
                self.print_trie(child, level + 1, f"{prefix}.{octet}")

    def clear(self):
        """Limpia el Trie"""
        self.root = TrieNode()
        self.nodes_count = 1
