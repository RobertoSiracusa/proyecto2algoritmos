#!/usr/bin/env python3
"""Prueba de la corrección del ping"""

from cli import CLIParser
from network import Network
from utils import ErrorLogger

def test_ping_fix():
    """Prueba que el ping ahora funciona correctamente"""

    # Configurar red como en main.py
    network = Network()
    error_logger = ErrorLogger()

    network.add_device('Router1', 'router')
    network.add_device('Switch1', 'switch')
    network.add_device('PC1', 'host')
    network.add_device('PC2', 'host')

    router1 = network.get_device('Router1')
    pc1 = network.get_device('PC1')
    pc2 = network.get_device('PC2')

    router1.configure_interface('g0/0', '192.168.1.1', '255.255.255.0', 'up')
    pc1.configure_interface('eth0', '192.168.1.10', '255.255.255.0', 'up')
    pc2.configure_interface('eth0', '192.168.1.20', '255.255.255.0', 'up')

    network.connect('g0/0', 'PC1', 'eth0')
    network.connect('g0/0', 'PC2', 'eth0')

    # Probar CLI
    cli = CLIParser(network, error_logger)

    print("=== PRUEBA DE CORRECCIÓN ===")
    print(f"Dispositivo actual: {cli.current_device.name if cli.current_device else 'None'}")

    if cli.current_device:
        print("Interfaces del dispositivo actual:")
        for iface_name, interface in cli.current_device.interfaces.items():
            if interface.ip_address:
                print(f"  {iface_name}: {interface.ip_address} ({'UP' if interface.is_up() else 'DOWN'})")

        # Probar ping
        print("\nProbando ping...")
        result = cli._handle_ping(["ping", "192.168.1.10"])
        print(f"Resultado: {result}")

    print("\n=== FIN DE PRUEBA ===")

if __name__ == "__main__":
    test_ping_fix()
