#!/usr/bin/env python3
"""Prueba de las rutas iniciales configuradas"""

from network import Network

def test_initial_routes():
    """Prueba que las rutas se configuran correctamente al inicio"""

    # Simular la configuración inicial del main.py
    network = Network()

    # Crear dispositivos
    network.add_device("Router1", "router")
    network.add_device("Switch1", "switch")
    network.add_device("PC1", "host")
    network.add_device("PC2", "host")

    # Configurar interfaces
    router1 = network.get_device("Router1")
    pc1 = network.get_device("PC1")
    pc2 = network.get_device("PC2")

    router1.configure_interface("g0/0", "192.168.1.1", "255.255.255.0", "up")
    pc1.configure_interface("eth0", "192.168.1.10", "255.255.255.0", "up")
    pc2.configure_interface("eth0", "192.168.1.20", "255.255.255.0", "up")

    # Conectar dispositivos
    network.connect("g0/0", "PC1", "eth0")
    network.connect("g0/0", "PC2", "eth0")

    # Configurar rutas (igual que en main.py)
    router1.add_route("10.0.0.0", "255.255.255.0", "192.168.1.100", 10)
    router1.add_route("172.16.0.0", "255.255.0.0", "192.168.1.200", 5)
    router1.add_route("192.168.2.0", "255.255.255.0", "192.168.1.50", 15)
    router1.add_route("0.0.0.0", "0.0.0.0", "192.168.1.254", 100)

    print("=== RUTAS CONFIGURADAS ===")
    print("Router1 - Tabla de rutas:")

    routes = router1.get_routing_table()
    if routes:
        for route_key, route_value in routes:
            print(f"  {route_key}  via {route_value['next_hop']}  metric {route_value['metric']}")
        print("  Default: none")
    else:
        print("  No hay rutas configuradas")

    print("\n=== ESTADÍSTICAS DEL AVL ===")
    stats = router1.routing_table.get_stats()
    print(f"Nodos: {stats['nodes']}")
    print(f"Altura: {stats['height']}")
    print(f"Rotaciones: LL={stats['rotations']['LL']} LR={stats['rotations']['LR']} RL={stats['rotations']['RL']} RR={stats['rotations']['RR']}")

    print("\n=== PRUEBA DE BÚSQUEDA ===")
    # Probar búsqueda de rutas
    test_ips = ["10.0.0.50", "172.16.5.100", "192.168.2.25", "8.8.8.8"]

    for ip in test_ips:
        route = router1.find_route(ip)
        if route:
            print(f"  {ip} -> {route}")
        else:
            print(f"  {ip} -> No route found")

    print("\n=== TEST COMPLETADO ===")

if __name__ == "__main__":
    test_initial_routes()
