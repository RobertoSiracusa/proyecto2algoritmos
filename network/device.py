"""
Implementación de la clase Device para el simulador de red
"""

from data_structures import LinkedList, Queue, Stack, AVLTree, Trie

class Interface:
    """Representa una interfaz de red de un dispositivo"""

    def __init__(self, name):
        self.name = name
        self.ip_address = None
        self.mask = None
        self.status = "down"  # "up" o "down"
        self.connected_to = None  # (device_name, interface_name)
        self.neighbors = LinkedList()  # Lista de dispositivos conectados
        self.input_queue = Queue()  # Cola de paquetes entrantes
        self.output_queue = Queue()  # Cola de paquetes salientes

    def set_ip(self, ip, mask=None):
        """Configura la dirección IP de la interfaz"""
        self.ip_address = ip
        self.mask = mask or "255.255.255.0"

    def set_status(self, status):
        """Cambia el estado de la interfaz"""
        if status in ["up", "down"]:
            self.status = status

    def is_up(self):
        """Verifica si la interfaz está activa"""
        return self.status == "up"

    def connect_to(self, device_name, interface_name):
        """Conecta esta interfaz a otra"""
        self.connected_to = (device_name, interface_name)

    def disconnect(self):
        """Desconecta esta interfaz"""
        self.connected_to = None

    def add_neighbor(self, neighbor_device):
        """Agrega un dispositivo vecino"""
        if not self.neighbors.contains(neighbor_device):
            self.neighbors.append(neighbor_device)

    def remove_neighbor(self, neighbor_device):
        """Remueve un dispositivo vecino"""
        if self.neighbors.contains(neighbor_device):
            index = self.neighbors.index_of(neighbor_device)
            self.neighbors.remove_at(index)

    def __str__(self):
        status = "UP" if self.is_up() else "DOWN"
        ip_info = f"{self.ip_address}" if self.ip_address else "No IP"
        return f"{self.name}: {ip_info} ({status})"

class Device:
    """Representa un dispositivo en la red (router, switch, host, firewall)"""

    def __init__(self, name, device_type="router", error_logger=None):
        self.name = name
        self.device_type = device_type  # "router", "switch", "host", "firewall"
        self.status = "online"  # "online" o "offline"
        self.interfaces = {}  # Diccionario de interfaces por nombre
        self.routing_table = AVLTree()  # Tabla de rutas usando AVL
        self.policy_trie = Trie()  # Trie para políticas de prefijos IP
        self.arp_table = {}  # Tabla ARP simple (IP -> MAC/interface)
        self.history = Stack()  # Historial de paquetes recibidos
        self.packets_sent = 0
        self.packets_received = 0
        self.packets_dropped = 0
        self.error_logger = error_logger  # Sistema de logging de errores

    def add_interface(self, interface_name):
        """Agrega una nueva interfaz al dispositivo"""
        if interface_name not in self.interfaces:
            self.interfaces[interface_name] = Interface(interface_name)
            return True
        return False

    def get_interface(self, interface_name):
        """Obtiene una interfaz por nombre"""
        return self.interfaces.get(interface_name)

    def list_interfaces(self):
        """Lista todas las interfaces"""
        return list(self.interfaces.keys())

    def set_status(self, status):
        """Cambia el estado del dispositivo"""
        if status in ["online", "offline"]:
            self.status = status

    def is_online(self):
        """Verifica si el dispositivo está online"""
        return self.status == "online"

    def configure_interface(self, interface_name, ip_address=None, mask=None, status=None):
        """Configura una interfaz"""
        interface = self.get_interface(interface_name)
        if not interface:
            return False

        if ip_address:
            interface.set_ip(ip_address, mask)
        if status:
            interface.set_status(status)

        return True

    # Métodos de tabla de rutas (usando AVL)
    def add_route(self, prefix, mask, next_hop, metric=1):
        """Agrega una ruta a la tabla de rutas"""
        route_key = f"{prefix}/{self._mask_to_prefix_length(mask)}"
        route_value = {"next_hop": next_hop, "metric": metric, "mask": mask}
        self.routing_table.insert_key(route_key, route_value)

    def remove_route(self, prefix, mask):
        """Remueve una ruta de la tabla de rutas"""
        route_key = f"{prefix}/{self._mask_to_prefix_length(mask)}"
        self.routing_table.delete_key(route_key)

    def find_route(self, destination_ip):
        """Busca la mejor ruta para un destino (longest prefix match)"""
        # Primero buscar en el Trie de políticas
        prefix_match, policy = self.policy_trie.search_longest_prefix(destination_ip)

        # Si hay una política de bloqueo, retornar None
        if policy and policy.get("block"):
            return None

        # Buscar en la tabla de rutas AVL
        # Para simplificar, buscar el prefijo más largo posible
        ip_parts = destination_ip.split('.')
        for prefix_len in range(32, -1, -1):
            prefix = '.'.join(ip_parts[:prefix_len//8])
            if prefix_len % 8 != 0:
                # Manejar prefijos no alineados a octetos
                last_octet = int(ip_parts[prefix_len//8])
                mask_bits = prefix_len % 8
                mask = (0xFF << (8 - mask_bits)) & 0xFF
                prefix = f"{'.'.join(ip_parts[:prefix_len//8])}.{last_octet & mask}"

            route_key = f"{prefix}/{prefix_len}"
            route = self.routing_table.search_key(route_key)
            if route:
                return route

        return None

    def _mask_to_prefix_length(self, mask):
        """Convierte máscara a longitud de prefijo"""
        mask_parts = mask.split('.')
        length = 0
        for part in mask_parts:
            octet = int(part)
            while octet > 0:
                length += octet & 1
                octet >>= 1
        return length

    # Métodos de políticas (usando Trie)
    def set_policy(self, prefix, mask, policy_type, value=None):
        """Establece una política para un prefijo"""
        policy = {policy_type: value}
        self.policy_trie.insert(prefix, mask, policy)

    def remove_policy(self, prefix, mask):
        """Remueve una política para un prefijo"""
        self.policy_trie.delete(prefix, mask)

    # Métodos de manejo de paquetes
    def receive_packet(self, packet):
        """Recibe un paquete y lo procesa"""
        if not self.is_online():
            return False

        self.packets_received += 1

        # Agregar al historial
        self.history.push(packet)

        # Aquí iría la lógica de procesamiento del paquete
        # Por ahora, solo lo agregamos al historial

        return True

    def send_packet(self, packet):
        """Envía un paquete"""
        if not self.is_online():
            return False

        # Encontrar la mejor ruta
        route = self.find_route(packet.destination_ip)
        if not route:
            self.packets_dropped += 1
            return False

        # Encontrar la interfaz de salida
        next_hop = route["next_hop"]
        output_interface = None

        # Buscar interfaz que pueda alcanzar el next_hop
        for iface_name, interface in self.interfaces.items():
            if interface.is_up() and interface.connected_to:
                # Simplificación: asumir que podemos alcanzar el next_hop
                output_interface = interface
                break

        if not output_interface:
            self.packets_dropped += 1
            return False

        # Agregar paquete a la cola de salida
        output_interface.output_queue.enqueue(packet)
        self.packets_sent += 1

        return True

    def process_queues(self):
        """Procesa las colas de entrada y salida con flujo completo de enrutamiento"""
        if not self.is_online():
            return

        # Procesar colas de salida (enviar paquetes)
        for interface in self.interfaces.values():
            while not interface.output_queue.is_empty():
                packet = interface.output_queue.dequeue()

                # 1. Lookup de políticas en el trie n-ario
                prefix_match, policy = self.policy_trie.search_longest_prefix(packet.destination_ip)

                # 2. Verificar si el paquete viola alguna política
                packet_dropped = False
                drop_reason = ""

                if policy:
                    if policy.get("block"):
                        packet_dropped = True
                        drop_reason = f"Paquete bloqueado por política en prefijo {prefix_match}"
                    elif policy.get("ttl-min") and packet.ttl < policy["ttl-min"]:
                        packet_dropped = True
                        drop_reason = f"TTL {packet.ttl} insuficiente (mínimo {policy['ttl-min']}) para prefijo {prefix_match}"

                if packet_dropped:
                    self.packets_dropped += 1
                    # Registrar error en el log
                    if self.error_logger:
                        self.error_logger.log_error(
                            "PolicyViolation",
                            "WARNING",
                            drop_reason,
                            f"packet from {packet.source_ip} to {packet.destination_ip}"
                        )
                    continue

                # 3. Si pasa las políticas, consultar tabla AVL para elegir siguiente salto
                route = self.find_route(packet.destination_ip)

                if route:
                    # Encontrar interfaz de salida
                    next_hop = route["next_hop"]
                    output_interface = None

                    # Buscar interfaz que pueda alcanzar el next_hop
                    for iface_name, iface in self.interfaces.items():
                        if iface.is_up() and iface.connected_to:
                            # Para simplificar, asumir que podemos alcanzar el next_hop
                            output_interface = iface
                            break

                    if output_interface:
                        # 4. Para vecinos directos, validar mediante tabla ARP
                        if next_hop in self.arp_table:
                            # ARP hit - enviar directamente
                            self.packets_sent += 1
                            packet.ttl -= 1
                        else:
                            # ARP miss - aprender interfaz y enviar
                            self.arp_table[next_hop] = output_interface.name
                            self.packets_sent += 1
                            packet.ttl -= 1
                    else:
                        # No hay interfaz de salida disponible
                        self.packets_dropped += 1
                        if self.error_logger:
                            self.error_logger.log_error(
                                "NoRouteToHost",
                                "ERROR",
                                f"No hay ruta disponible para {packet.destination_ip}",
                                f"packet from {packet.source_ip}"
                            )
                else:
                    # No se encontró ruta en la tabla AVL
                    self.packets_dropped += 1
                    if self.error_logger:
                        self.error_logger.log_error(
                            "NoRouteToHost",
                            "ERROR",
                            f"No hay ruta disponible para {packet.destination_ip}",
                            f"packet from {packet.source_ip}"
                        )

                # Verificar TTL después del procesamiento
                if packet.ttl <= 0:
                    self.packets_dropped += 1
                    if self.error_logger:
                        self.error_logger.log_error(
                            "TTLExpired",
                            "INFO",
                            f"TTL expiró para paquete de {packet.source_ip} a {packet.destination_ip}",
                            ""
                        )

    # Métodos de consulta
    def get_routing_table(self):
        """Obtiene la tabla de rutas"""
        return self.routing_table.get_all_routes()

    def get_history(self, limit=None):
        """Obtiene el historial de paquetes"""
        history_list = []
        temp_stack = Stack()

        # Vaciar la pila para obtener los elementos en orden
        while not self.history.is_empty():
            packet = self.history.pop()
            history_list.append(packet)
            temp_stack.push(packet)

        # Restaurar la pila original
        while not temp_stack.is_empty():
            self.history.push(temp_stack.pop())

        # Aplicar límite si se especifica
        if limit:
            history_list = history_list[-limit:]

        return history_list

    def get_statistics(self):
        """Obtiene estadísticas del dispositivo"""
        return {
            "packets_sent": self.packets_sent,
            "packets_received": self.packets_received,
            "packets_dropped": self.packets_dropped,
            "routing_table_entries": len(self.routing_table.get_all_routes()),
            "interfaces_count": len(self.interfaces),
            "routing_stats": self.routing_table.get_stats()
        }

    def __str__(self):
        status = "ONLINE" if self.is_online() else "OFFLINE"
        return f"{self.name} ({self.device_type}) - {status}"
