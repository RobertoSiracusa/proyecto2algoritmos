#!/usr/bin/env python3
"""Prueba del módulo de Índice Persistente con B-tree"""

from cli import CLIParser
from network import Network
from utils import ErrorLogger

def test_btree_module():
    """Prueba completa del módulo B-tree"""

    # Configurar red
    network = Network()
    error_logger = ErrorLogger()

    network.add_device("Router1", "router")
    router1 = network.get_device("Router1")
    router1.configure_interface("g0/0", "192.168.1.1", "255.255.255.0", "up")

    # Inicializar CLI
    cli = CLIParser(network, error_logger)

    print("=== PRUEBA DEL MÓDULO B-TREE ===\n")

    # Cambiar a modo privilegiado
    cli.current_mode = "PRIVILEGED"

    print("1. Guardando configuración básica...")
    result1 = cli.parse_command("save running-config")
    print(f"   Resultado: {result1}")

    print("\n2. Guardando snapshots nombrados...")
    result2 = cli.parse_command("save snapshot laboratorio")
    print(f"   Resultado: {result2}")

    result3 = cli.parse_command("save snapshot backup_2024")
    print(f"   Resultado: {result3}")

    print("\n3. Mostrando snapshots disponibles...")
    result4 = cli.parse_command("show snapshots")
    print(f"   {result4}")

    print("\n4. Mostrando estadísticas del B-tree...")
    result5 = cli.parse_command("show btree stats")
    print(f"   {result5}")

    print("\n5. Cargando snapshot por clave...")
    result6 = cli.parse_command("load config laboratorio")
    print(f"   Resultado: {result6}")

    print("\n=== PRUEBA COMPLETADA ===")

if __name__ == "__main__":
    test_btree_module()
