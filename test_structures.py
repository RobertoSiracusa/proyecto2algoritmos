#!/usr/bin/env python3
"""
Script de prueba para las estructuras de datos
"""

from data_structures import LinkedList, Queue, Stack, AVLTree, BTree, Trie

def test_linked_list():
    """Prueba LinkedList"""
    print("=== Probando LinkedList ===")
    ll = LinkedList()

    # Agregar elementos
    ll.append("A")
    ll.append("B")
    ll.append("C")
    print(f"Lista: {ll}")

    # Insertar en posición
    ll.insert_at(1, "X")
    print(f"Después de insertar X en posición 1: {ll}")

    # Remover elemento
    removed = ll.remove_at(2)
    print(f"Elemento removido: {removed}, Lista: {ll}")

    print("LinkedList funcionando correctamente\n")

def test_queue():
    """Prueba Queue"""
    print("=== Probando Queue ===")
    q = Queue()

    # Enqueue
    q.enqueue("Primer")
    q.enqueue("Segundo")
    q.enqueue("Tercer")
    print(f"Cola después de enqueue: {q}")

    # Dequeue
    first = q.dequeue()
    print(f"Primer elemento: {first}, Cola: {q}")

    # Peek
    peek = q.peek()
    print(f"Elemento del frente: {peek}")

    print("Queue funcionando correctamente\n")

def test_stack():
    """Prueba Stack"""
    print("=== Probando Stack ===")
    s = Stack()

    # Push
    s.push("Primero")
    s.push("Segundo")
    s.push("Tercero")
    print(f"Pila después de push: {s}")

    # Pop
    top = s.pop()
    print(f"Elemento del tope: {top}, Pila: {s}")

    # Peek
    peek = s.peek()
    print(f"Elemento del tope (sin remover): {peek}")

    print("Stack funcionando correctamente\n")

def test_avl_tree():
    """Prueba AVL Tree"""
    print("=== Probando AVL Tree ===")
    try:
        avl = AVLTree()
        print("AVL Tree creado")

        # Insertar elementos
        routes = [
            ("10.0.0.0/24", {"next_hop": "192.168.1.2", "metric": 10}),
            ("192.168.1.0/24", {"next_hop": "10.0.0.1", "metric": 5}),
            ("172.16.0.0/16", {"next_hop": "192.168.1.3", "metric": 15}),
        ]

        print("Insertando rutas...")
        for route_key, route_value in routes:
            print(f"  Insertando {route_key}")
            avl.insert_key(route_key, route_value)

        print("Rutas insertadas:")
        all_routes = avl.get_all_routes()
        print(f"  Número de rutas: {len(all_routes)}")
        for route_key, route_value in all_routes:
            print(f"  {route_key} -> {route_value}")

        print("Obteniendo estadísticas...")
        stats = avl.get_stats()
        print(f"Estadísticas AVL: {stats}")
        print("AVL Tree funcionando correctamente\n")
    except Exception as e:
        print(f"Error en AVL Tree: {e}")
        import traceback
        traceback.print_exc()

def test_b_tree():
    """Prueba B-Tree"""
    print("=== Probando B-Tree ===")
    bt = BTree(order=4)

    # Insertar elementos
    snapshots = [
        ("snapshot_001", "config1.txt"),
        ("snapshot_002", "config2.txt"),
        ("lab_grupoA", "lab_config.txt"),
        ("backup_2024", "backup.txt"),
    ]

    for key, value in snapshots:
        bt.insert(key, value)

    print("Snapshots insertados:")
    for key, value in bt.get_all_entries():
        print(f"  {key} -> {value}")

    print(f"Estadísticas B-Tree: {bt.get_stats()}")
    print("B-Tree funcionando correctamente\n")

def test_trie():
    """Prueba Trie"""
    print("=== Probando Trie ===")
    trie = Trie()

    # Insertar prefijos con políticas
    policies = [
        ("192.168.1.0", "255.255.255.0", {"ttl-min": 5}),
        ("10.0.0.0", "255.255.0.0", {"block": True}),
        ("172.16.0.0", "255.255.0.0", {"ttl-min": 3}),
    ]

    for prefix, mask, policy in policies:
        trie.insert(prefix, mask, policy)

    print("Políticas insertadas:")
    for prefix, policy in trie.get_all_prefixes():
        print(f"  {prefix} -> {policy}")

    # Buscar longest prefix match
    test_ips = ["192.168.1.10", "10.0.5.100", "172.16.1.1", "8.8.8.8"]

    print("\nLongest Prefix Match:")
    for ip in test_ips:
        prefix, policy = trie.search_longest_prefix(ip)
        print(f"  {ip} -> {prefix or 'No match'} -> {policy or 'No policy'}")

    print(f"Estadísticas Trie: {trie.get_stats()}")
    print("Trie funcionando correctamente\n")

def main():
    """Función principal de pruebas"""
    print("=== Pruebas de Estructuras de Datos ===\n")

    try:
        test_linked_list()
        test_queue()
        test_stack()
        test_avl_tree()
        test_b_tree()
        test_trie()

        print("=== Todas las pruebas pasaron exitosamente ===")

    except Exception as e:
        print(f"Error en las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
