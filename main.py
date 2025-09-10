#!/usr/bin/env python3
"""
Simulador de Red LAN - Proyecto 2 Algoritmos
Interfaz CLI inspirada en Cisco IOS
"""

from cli import CLIParser
from network import Network
from utils import ErrorLogger

def main():
    """Función principal del simulador"""
    print("=== Simulador de Red LAN ===")
    print("Inspirado en Cisco IOS")
    print("Escribe 'help' para ver comandos disponibles")
    print("Escribe 'exit' para salir")
    print()

    # Inicializar componentes del simulador
    network = Network()
    error_logger = ErrorLogger()

    # Crear dispositivos por defecto para testing
    network.add_device("Router1", "router", error_logger)
    network.add_device("Switch1", "switch", error_logger)
    network.add_device("PC1", "host", error_logger)
    network.add_device("PC2", "host", error_logger)

    # Configurar algunas interfaces por defecto
    router1 = network.get_device("Router1")
    pc1 = network.get_device("PC1")
    pc2 = network.get_device("PC2")

    router1.configure_interface("g0/0", "192.168.1.1", "255.255.255.0", "up")
    pc1.configure_interface("eth0", "192.168.1.10", "255.255.255.0", "up")
    pc2.configure_interface("eth0", "192.168.1.20", "255.255.255.0", "up")

    # Conectar dispositivos
    network.connect("g0/0", "PC1", "eth0")
    network.connect("g0/0", "PC2", "eth0")

    # Configurar rutas de ejemplo en Router1
    print("Configurando rutas de ejemplo...")
    router1.add_route("10.0.0.0", "255.255.255.0", "192.168.1.100", 10)  # Red externa 1
    router1.add_route("172.16.0.0", "255.255.0.0", "192.168.1.200", 5)   # Red externa 2
    router1.add_route("192.168.2.0", "255.255.255.0", "192.168.1.50", 15) # Otra subred
    router1.add_route("0.0.0.0", "0.0.0.0", "192.168.1.254", 100)        # Ruta por defecto
    print("Rutas configuradas en Router1")

    print("\nDispositivos inicializados:")
    print("- Router1 (router) con IP 192.168.1.1")
    print("- Switch1 (switch)")
    print("- PC1 (host) con IP 192.168.1.10")
    print("- PC2 (host) con IP 192.168.1.20")
    print("\nConexiones:")
    print("- Router1 <-> PC1")
    print("- Router1 <-> PC2")
    print("\nRutas configuradas en Router1:")
    print("- 10.0.0.0/24 via 192.168.1.100 metric 10")
    print("- 172.16.0.0/16 via 192.168.1.200 metric 5")
    print("- 192.168.2.0/24 via 192.168.1.50 metric 15")
    print("- 0.0.0.0/0 via 192.168.1.254 metric 100 (default)")
    print()

    # Inicializar CLI
    cli = CLIParser(network, error_logger)

    # Ejecutar el loop principal
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\nSaliendo del simulador...")
    except Exception as e:
        error_logger.log_error("SYSTEM", "CRITICAL", f"Error crítico del sistema: {str(e)}", "")
        print(f"Error crítico: {e}")

if __name__ == "__main__":
    main()
