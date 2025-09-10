"""
Implementación de la clase Network para el simulador
"""

from .device import Device
from data_structures import LinkedList, BTree
import time

class Network:
    """Clase principal que representa la red completa"""

    def __init__(self):
        self.devices = {}  # Diccionario de dispositivos por nombre
        self.connections = LinkedList()  # Lista de conexiones
        self.snapshots = BTree()  # B-Tree para snapshots de configuración
        self.current_device = None  # Dispositivo actual en la sesión CLI

    def add_device(self, name, device_type="router", error_logger=None):
        """Agrega un nuevo dispositivo a la red"""
        if name in self.devices:
            return False

        device = Device(name, device_type, error_logger)
        self.devices[name] = device

        # Agregar interfaces por defecto según el tipo
        if device_type == "router":
            device.add_interface("g0/0")
            device.add_interface("g0/1")
        elif device_type == "switch":
            for i in range(8):  # 8 puertos por defecto
                device.add_interface(f"g0/{i}")
        elif device_type == "host":
            device.add_interface("eth0")

        return True

    def remove_device(self, name):
        """Remueve un dispositivo de la red"""
        if name not in self.devices:
            return False

        device = self.devices[name]

        # Remover todas las conexiones del dispositivo
        for interface_name, interface in device.interfaces.items():
            if interface.connected_to:
                self.disconnect(interface_name, *interface.connected_to)

        del self.devices[name]
        return True

    def get_device(self, name):
        """Obtiene un dispositivo por nombre"""
        return self.devices.get(name)

    def list_devices(self):
        """Lista todos los dispositivos"""
        return list(self.devices.keys())

    def set_device_status(self, device_name, status):
        """Cambia el estado de un dispositivo"""
        device = self.get_device(device_name)
        if device:
            device.set_status(status)
            return True
        return False

    def connect(self, iface1, device2, iface2):
        """Conecta dos interfaces de dispositivos diferentes"""
        # iface1 debe ser del dispositivo actual o especificar dispositivo
        if "." in iface1:
            dev1_name, iface1_name = iface1.split(".")
        else:
            if not self.current_device:
                return False
            dev1_name = self.current_device.name
            iface1_name = iface1

        dev1 = self.get_device(dev1_name)
        dev2 = self.get_device(device2)

        if not dev1 or not dev2:
            return False

        if dev1_name == device2:
            return False  # No conectar dispositivo consigo mismo

        iface1_obj = dev1.get_interface(iface1_name)
        iface2_obj = dev2.get_interface(iface2)

        if not iface1_obj or not iface2_obj:
            return False

        # Verificar que ambas interfaces estén down antes de conectar
        if iface1_obj.is_up() or iface2_obj.is_up():
            return False

        # Establecer conexión
        iface1_obj.connect_to(device2, iface2)
        iface2_obj.connect_to(dev1_name, iface1_name)

        # Agregar a lista de conexiones
        connection = {
            "device1": dev1_name,
            "iface1": iface1_name,
            "device2": device2,
            "iface2": iface2
        }
        self.connections.append(connection)

        # Agregar vecinos
        iface1_obj.add_neighbor(device2)
        iface2_obj.add_neighbor(dev1_name)

        return True

    def disconnect(self, iface1, device2, iface2):
        """Desconecta dos interfaces"""
        if "." in iface1:
            dev1_name, iface1_name = iface1.split(".")
        else:
            if not self.current_device:
                return False
            dev1_name = self.current_device.name
            iface1_name = iface1

        dev1 = self.get_device(dev1_name)
        dev2 = self.get_device(device2)

        if not dev1 or not dev2:
            return False

        iface1_obj = dev1.get_interface(iface1_name)
        iface2_obj = dev2.get_interface(iface2)

        if not iface1_obj or not iface2_obj:
            return False

        # Remover conexión
        iface1_obj.disconnect()
        iface2_obj.disconnect()

        # Remover de lista de conexiones
        for i in range(len(self.connections)):
            conn = self.connections.get(i)
            if (conn["device1"] == dev1_name and conn["iface1"] == iface1_name and
                conn["device2"] == device2 and conn["iface2"] == iface2):
                self.connections.remove_at(i)
                break

        # Remover vecinos
        iface1_obj.remove_neighbor(device2)
        iface2_obj.remove_neighbor(dev1_name)

        return True

    def tick(self):
        """Avanza un paso de simulación (procesa todas las colas)"""
        for device in self.devices.values():
            device.process_queues()

    def send_packet(self, source_ip, dest_ip, message, ttl=64):
        """Envía un paquete desde una IP fuente a una IP destino"""
        # Encontrar dispositivo fuente
        source_device = None
        source_interface = None

        for device in self.devices.values():
            for iface_name, interface in device.interfaces.items():
                if interface.ip_address == source_ip:
                    source_device = device
                    source_interface = interface
                    break
            if source_device:
                break

        if not source_device:
            return False, "IP fuente no encontrada"

        # Crear paquete
        from .packet import Packet
        packet = Packet(source_ip, dest_ip, message, ttl)

        # Agregar a la cola de salida del dispositivo fuente
        source_interface.output_queue.enqueue(packet)

        return True, "Paquete encolado para envío"

    def get_network_stats(self):
        """Obtiene estadísticas globales de la red"""
        total_packets_sent = 0
        total_packets_received = 0
        total_packets_dropped = 0
        total_hops = 0
        packet_count = 0

        for device in self.devices.values():
            stats = device.get_statistics()
            total_packets_sent += stats["packets_sent"]
            total_packets_received += stats["packets_received"]
            total_packets_dropped += stats["packets_dropped"]

            # Calcular hops promedio
            for packet in device.get_history():
                total_hops += len(packet.path) - 1  # hops = saltos - 1
                packet_count += 1

        avg_hops = total_hops / packet_count if packet_count > 0 else 0

        # Encontrar dispositivo con más actividad
        top_talker = None
        max_packets = 0
        for name, device in self.devices.items():
            total_device_packets = (device.packets_sent + device.packets_received)
            if total_device_packets > max_packets:
                max_packets = total_device_packets
                top_talker = name

        return {
            "total_packets_sent": total_packets_sent,
            "total_packets_received": total_packets_received,
            "total_packets_dropped": total_packets_dropped,
            "average_hops": avg_hops,
            "top_talker": top_talker,
            "devices_online": len([d for d in self.devices.values() if d.is_online()]),
            "total_devices": len(self.devices)
        }

    def save_snapshot(self, key=None):
        """Guarda un snapshot de la configuración actual"""
        if not key:
            key = f"snapshot_{int(time.time())}"

        # Crear configuración en formato de texto
        config_lines = []

        # Guardar dispositivos y sus configuraciones
        for device_name, device in self.devices.items():
            config_lines.append(f"hostname {device_name}")
            config_lines.append(f"device-type {device.device_type}")

            # Interfaces
            for iface_name, interface in device.interfaces.items():
                config_lines.append(f"interface {iface_name}")
                if interface.ip_address:
                    config_lines.append(f"  ip address {interface.ip_address}")
                config_lines.append(f"  {'no ' if not interface.is_up() else ''}shutdown")
                config_lines.append("exit")

            # Rutas
            for route_key, route_value in device.get_routing_table():
                prefix, mask_len = route_key.split('/')
                config_lines.append(f"ip route {prefix} {route_value['mask']} via {route_value['next_hop']} metric {route_value['metric']}")

            config_lines.append("")

        # Guardar conexiones
        for i in range(len(self.connections)):
            conn = self.connections.get(i)
            config_lines.append(f"connect {conn['device1']} {conn['iface1']} {conn['device2']} {conn['iface2']}")

        config_content = "\n".join(config_lines)

        # Guardar en archivo
        filename = f"snapshots/{key}.cfg"
        try:
            with open(filename, 'w') as f:
                f.write(config_content)
        except:
            # Si no existe el directorio, crearlo
            import os
            os.makedirs("snapshots", exist_ok=True)
            with open(filename, 'w') as f:
                f.write(config_content)

        # Indexar en B-Tree
        self.snapshots.insert(key, filename)

        return True, filename

    def load_snapshot(self, key):
        """Carga un snapshot de configuración"""
        filename = self.snapshots.search(key)
        if not filename:
            return False, "Snapshot no encontrado"

        try:
            with open(filename, 'r') as f:
                config_content = f.read()

            # Parsear y aplicar configuración
            self._parse_config(config_content)
            return True, f"Configuración cargada desde {filename}"
        except FileNotFoundError:
            return False, "Archivo de snapshot no encontrado"
        except Exception as e:
            return False, f"Error al cargar snapshot: {e}"

    def _parse_config(self, config_content):
        """Parsea el contenido de configuración"""
        lines = config_content.strip().split('\n')
        current_device = None
        current_interface = None

        for line in lines:
            line = line.strip()
            if not line or line.startswith('#'):
                continue

            parts = line.split()

            if parts[0] == "hostname":
                device_name = parts[1]
                device_type = "router"  # default
                # Buscar el tipo en la siguiente línea si existe
                current_device = Device(device_name, device_type)
                self.devices[device_name] = current_device

            elif parts[0] == "device-type" and current_device:
                current_device.device_type = parts[1]

            elif parts[0] == "interface" and current_device:
                iface_name = parts[1]
                current_device.add_interface(iface_name)
                current_interface = current_device.get_interface(iface_name)

            elif parts[0] == "ip" and parts[1] == "address" and current_interface:
                ip = parts[2]
                mask = parts[3] if len(parts) > 3 else "255.255.255.0"
                current_interface.set_ip(ip, mask)

            elif parts[0] in ["shutdown", "no"] and current_interface:
                if parts[0] == "no":
                    current_interface.set_status("up")
                else:
                    current_interface.set_status("down")

            elif parts[0] == "connect":
                dev1, iface1, dev2, iface2 = parts[1], parts[2], parts[3], parts[4]
                self.connect(iface1, dev2, iface2)

            elif parts[0] == "ip" and parts[1] == "route" and current_device:
                prefix = parts[2]
                mask = parts[3]
                next_hop = parts[5]  # via
                metric = int(parts[7]) if len(parts) > 7 else 1
                current_device.add_route(prefix, mask, next_hop, metric)

    def get_snapshots(self):
        """Obtiene lista de snapshots disponibles"""
        return self.snapshots.get_all_entries()
