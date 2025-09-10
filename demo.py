#!/usr/bin/env python3
"""
Demostración del Simulador de Red LAN
Muestra las funcionalidades principales del sistema
"""

from cli import CLIParser
from network import Network
from utils import ErrorLogger

def demo_basico():
    """Demostración básica del funcionamiento"""
    print("=== DEMO: Funcionamiento Básico ===\n")

    # Inicializar componentes
    network = Network()
    error_logger = ErrorLogger()

    # Crear dispositivos
    network.add_device("Router1", "router")
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

    print("Red configurada:")
    print("- Router1 (192.168.1.1)")
    print("- PC1 (192.168.1.10)")
    print("- PC2 (192.168.1.20)")
    print("- Conexiones: Router1 ↔ PC1, Router1 ↔ PC2")
    print()

    # Enviar paquetes
    print("Enviando paquetes...")
    success1, msg1 = network.send_packet("192.168.1.10", "192.168.1.20", "Hola PC2!", 64)
    success2, msg2 = network.send_packet("192.168.1.20", "192.168.1.10", "Hola PC1!", 64)

    print(f"PC1 → PC2: {msg1}")
    print(f"PC2 → PC1: {msg2}")
    print()

    # Procesar colas
    print("Procesando simulación...")
    network.tick()
    print("Tick completado")
    print()

    # Mostrar estadísticas
    stats = network.get_network_stats()
    print("Estadísticas finales:")
    print(f"- Paquetes enviados: {stats['total_packets_sent']}")
    print(f"- Paquetes recibidos: {stats['total_packets_received']}")
    print(f"- Dispositivos online: {stats['devices_online']}/{stats['total_devices']}")
    print()

def demo_avl_tree():
    """Demostración del Árbol AVL para rutas"""
    print("=== DEMO: Árbol AVL para Tabla de Rutas ===\n")

    from data_structures import AVLTree

    # Crear tabla de rutas
    routing_table = AVLTree()

    rutas = [
        ("10.0.0.0/24", {"next_hop": "192.168.1.2", "metric": 10}),
        ("192.168.1.0/24", {"next_hop": "10.0.0.1", "metric": 5}),
        ("172.16.0.0/16", {"next_hop": "192.168.1.3", "metric": 15}),
        ("10.1.0.0/24", {"next_hop": "172.16.0.2", "metric": 8}),
        ("192.168.2.0/24", {"next_hop": "10.0.0.3", "metric": 12}),
    ]

    print("Insertando rutas en el árbol AVL...")
    for ruta, datos in rutas:
        routing_table.insert_key(ruta, datos)
        print(f"  ✓ Insertada: {ruta}")

    print("\nTabla de rutas ordenada:")
    for ruta, datos in routing_table.get_all_routes():
        print(f"  {ruta} → {datos['next_hop']} (métrica: {datos['metric']})")

    print("\nEstadísticas del AVL:")
    stats = routing_table.get_stats()
    print(f"  - Nodos: {stats['nodes']}")
    print(f"  - Altura: {stats['height']}")
    print(f"  - Rotaciones: {stats['rotations']}")
    print()

def demo_trie():
    """Demostración del Trie para prefijos IP"""
    print("=== DEMO: Trie para Prefijos IP ===\n")

    from data_structures import Trie

    # Crear trie de políticas
    trie = Trie()

    politicas = [
        ("192.168.1.0", "255.255.255.0", {"ttl-min": 5}),
        ("10.0.0.0", "255.255.0.0", {"block": True}),
        ("172.16.0.0", "255.255.0.0", {"ttl-min": 3}),
        ("192.168.2.0", "255.255.255.0", {"block": True}),
    ]

    print("Insertando políticas en el Trie...")
    for prefix, mask, policy in politicas:
        trie.insert(prefix, mask, policy)
        print(f"  ✓ Insertada: {prefix}/{trie._get_prefix_length(mask)} -> {policy}")

    print("\nBuscando longest prefix match para diferentes IPs:")
    test_ips = ["192.168.1.10", "10.0.5.100", "172.16.1.1", "192.168.2.50", "8.8.8.8"]

    for ip in test_ips:
        prefix, policy = trie.search_longest_prefix(ip)
        if prefix:
            print(f"  {ip} → {prefix} -> {policy}")
        else:
            print(f"  {ip} → No match")

    print("\nEstadísticas del Trie:")
    stats = trie.get_stats()
    print(f"  - Nodos: {stats['nodes']}")
    print(f"  - Prefijos: {stats['prefixes']}")
    print()

def demo_error_logging():
    """Demostración del sistema de logging de errores"""
    print("=== DEMO: Sistema de Logging de Errores ===\n")

    error_logger = ErrorLogger()

    # Simular diferentes tipos de errores
    errores = [
        ("SyntaxError", "ERROR", "Comando 'invalid_command' no reconocido", "invalid_command"),
        ("ConnectionError", "WARNING", "No se pudo conectar a dispositivo inexistente", "connect g0/0 DeviceX g0/0"),
        ("NetworkError", "ERROR", "IP de destino no encontrada en la red", "ping 192.168.999.1"),
        ("CommandDisabled", "INFO", "Comando no disponible en modo usuario", "configure terminal"),
    ]

    print("Registrando errores...")
    for error_type, severity, message, command in errores:
        error_logger.log_error(error_type, severity, message, command)
        print(f"  ✓ {severity}: {message}")

    print("\nÚltimos errores registrados:")
    recent_errors = error_logger.get_recent_errors(3)
    for i, error in enumerate(recent_errors, 1):
        print(f"  {i}. {error}")

    print("\nConteo por tipo:")
    counts = error_logger.get_error_counts()
    for error_type, count in counts["by_type"].items():
        print(f"  {error_type}: {count}")

    print(f"\nTotal de errores: {counts['total']}")
    print()

def main():
    """Función principal de demostración"""
    print("🚀 DEMOSTRACIÓN DEL SIMULADOR DE RED LAN 🚀")
    print("=" * 50)
    print()

    try:
        demo_basico()
        demo_avl_tree()
        demo_trie()
        demo_error_logging()

        print("✅ DEMOSTRACIÓN COMPLETADA EXITOSAMENTE")
        print("\nPara usar el simulador completo, ejecuta:")
        print("  python main.py")
        print("\nPara ver ayuda en cualquier momento:")
        print("  Router1> help")

    except Exception as e:
        print(f"❌ Error en la demostración: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
