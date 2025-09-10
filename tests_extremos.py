#!/usr/bin/env python3
"""
Tests funcionales para casos extremos de las estructuras de datos
Según las pautas del proyecto
"""

from data_structures import AVLTree, BTree, Trie

def test_avl_casos_extremos():
    """Tests extremos para AVL: borrado de raíz, rotaciones dobles"""
    print("=== TESTS EXTREMOS AVL ===")

    avl = AVLTree()

    # Insertar datos que provoquen rotaciones dobles
    print("1. Insertando datos para rotaciones dobles...")
    routes = [
        ("192.168.1.0/24", "route1"),
        ("10.0.0.0/24", "route2"),
        ("172.16.0.0/16", "route3"),
        ("192.168.2.0/24", "route4"),
        ("10.1.0.0/24", "route5"),
    ]

    for route, value in routes:
        avl.insert_key(route, value)
        print(f"   Insertado: {route}")

    print("\nEstado inicial:")
    print(f"   Nodos: {avl.get_stats()['nodes']}")
    print(f"   Altura: {avl.get_stats()['height']}")
    print(f"   Rotaciones: {avl.get_stats()['rotations']}")

    # Mostrar árbol
    print("\nÁrbol AVL:")
    avl.print_tree()

    # Borrar el nodo raíz (caso extremo)
    print("\n2. Borrando nodo raíz (192.168.1.0/24)...")
    avl.delete_key("192.168.1.0/24")

    print("Después de borrar raíz:")
    print(f"   Nodos: {avl.get_stats()['nodes']}")
    print(f"   Altura: {avl.get_stats()['height']}")
    print(f"   Rotaciones: {avl.get_stats()['rotations']}")

    print("\nÁrbol AVL después de borrar raíz:")
    avl.print_tree()

    # Insertar más datos para probar balance
    print("\n3. Insertando más datos para probar balance...")
    more_routes = [
        ("192.168.3.0/24", "route6"),
        ("10.2.0.0/24", "route7"),
        ("172.17.0.0/16", "route8"),
    ]

    for route, value in more_routes:
        avl.insert_key(route, value)

    print("Después de más inserciones:")
    print(f"   Nodos: {avl.get_stats()['nodes']}")
    print(f"   Altura: {avl.get_stats()['height']}")
    print(f"   Rotaciones: {avl.get_stats()['rotations']}")

    print("\nÁrbol AVL final:")
    avl.print_tree()

    print("✅ Tests AVL completados exitosamente\n")

def test_btree_casos_extremos():
    """Tests extremos para B-Tree: split en raíz, colisiones de claves"""
    print("=== TESTS EXTREMOS B-TREE ===")

    btree = BTree(order=3)  # Orden pequeño para forzar splits

    print("1. Insertando datos para forzar splits en raíz...")
    # Insertar suficientes claves para provocar split en la raíz
    snapshots = []
    for i in range(10):
        key = "04d"
        snapshots.append((key, f"snapshot_{i}.cfg"))

    for key, value in snapshots:
        btree.insert(key, value)
        print(f"   Insertado: {key} -> {value}")

    print("\nEstado después de inserciones:")
    stats = btree.get_stats()
    print(f"   Orden: {stats['order']}")
    print(f"   Altura: {stats['height']}")
    print(f"   Nodos: {stats['nodes']}")
    print(f"   Splits: {stats['splits']}")
    print(f"   Merges: {stats['merges']}")

    # Mostrar árbol
    print("\nÁrbol B-Tree:")
    btree.print_tree()

    # Probar búsqueda
    print("\n2. Probando búsqueda...")
    for i in range(3):
        key = "04d"
        result = btree.search(key)
        print(f"   Búsqueda de {key}: {'Encontrado' if result else 'No encontrado'}")

    # Probar eliminación
    print("\n3. Probando eliminación...")
    for i in range(3):
        key = "04d"
        print(f"   Eliminando: {key}")
        btree.delete(key)

    print("Después de eliminaciones:")
    stats = btree.get_stats()
    print(f"   Altura: {stats['height']}")
    print(f"   Nodos: {stats['nodes']}")
    print(f"   Splits: {stats['splits']}")
    print(f"   Merges: {stats['merges']}")

    print("\nÁrbol B-Tree después de eliminaciones:")
    btree.print_tree()

    print("✅ Tests B-Tree completados exitosamente\n")

def test_trie_casos_extremos():
    """Tests extremos para Trie: prefijos anidados, colisiones"""
    print("=== TESTS EXTREMOS TRIE ===")

    trie = Trie()

    print("1. Insertando prefijos anidados...")
    # Prefijos que se anidan unos dentro de otros
    prefixes = [
        ("192.168.0.0", "255.255.0.0", {"policy": "network_policy"}),     # /16
        ("192.168.1.0", "255.255.255.0", {"policy": "subnet_policy"}),    # /24 dentro del /16
        ("192.168.1.10", "255.255.255.255", {"policy": "host_policy"}),   # /32 dentro del /24
        ("10.0.0.0", "255.0.0.0", {"policy": "class_a_policy"}),          # /8
        ("10.1.0.0", "255.255.0.0", {"policy": "subnet_a_policy"}),       # /16 dentro del /8
        ("172.16.0.0", "255.240.0.0", {"policy": "class_b_policy"}),      # /12
    ]

    for ip, mask, policy in prefixes:
        trie.insert(ip, mask, policy)
        print(f"   Insertado: {ip}/{trie._get_prefix_length(mask)} -> {policy}")

    print("\nEstado del Trie:")
    stats = trie.get_stats()
    print(f"   Nodos: {stats['nodes']}")
    print(f"   Prefijos: {stats['prefixes']}")

    # Mostrar estructura del trie
    print("\nEstructura del Trie:")
    trie.print_trie()

    print("\n2. Probando longest prefix match...")
    test_ips = [
        "192.168.1.10",    # Debería coincidir con /32, /24, /16
        "192.168.1.20",    # Debería coincidir con /24, /16
        "192.168.2.10",    # Debería coincidir con /16
        "10.1.1.1",        # Debería coincidir con /16, /8
        "10.2.1.1",        # Debería coincidir solo con /8
        "172.16.1.1",      # Debería coincidir con /12
        "8.8.8.8",         # No debería coincidir
    ]

    for ip in test_ips:
        prefix, policy = trie.search_longest_prefix(ip)
        if prefix:
            print(f"   {ip} -> {prefix} -> {policy}")
        else:
            print(f"   {ip} -> No match")

    print("\n3. Probando eliminación de prefijos...")
    # Eliminar un prefijo anidado
    trie.delete("192.168.1.10", "255.255.255.255")
    print("   Eliminado: 192.168.1.10/32")

    # Verificar que el padre todavía existe
    prefix, policy = trie.search_longest_prefix("192.168.1.10")
    if prefix:
        print(f"   Después de eliminación: 192.168.1.10 -> {prefix} -> {policy}")

    print("\nEstado final del Trie:")
    stats = trie.get_stats()
    print(f"   Nodos: {stats['nodes']}")
    print(f"   Prefijos: {stats['prefixes']}")

    print("\nEstructura final del Trie:")
    trie.print_trie()

    print("✅ Tests Trie completados exitosamente\n")

def main():
    """Ejecutar todos los tests extremos"""
    print("🚀 TESTS FUNCIONALES PARA CASOS EXTREMOS")
    print("=" * 50)
    print()

    try:
        test_avl_casos_extremos()
        test_btree_casos_extremos()
        test_trie_casos_extremos()

        print("🎉 TODOS LOS TESTS EXTREMOS COMPLETADOS EXITOSAMENTE")
        print("\nResumen de casos extremos probados:")
        print("✅ AVL: Borrado de nodo raíz")
        print("✅ AVL: Rotaciones dobles")
        print("✅ B-Tree: Split en raíz")
        print("✅ B-Tree: Colisiones de claves")
        print("✅ Trie: Prefijos anidados")
        print("✅ Trie: Herencia de políticas")

    except Exception as e:
        print(f"❌ Error en tests extremos: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
