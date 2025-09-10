"""
Interfaz de línea de comandos para el simulador de red
Implementa diferentes modos y parsing de comandos
"""

class CLIParser:
    """Parser de comandos CLI con modos múltiples"""

    MODES = {
        "USER": ">",
        "PRIVILEGED": "#",
        "CONFIG": "(config)#",
        "INTERFACE": "(config-if)#"
    }

    def __init__(self, network, error_logger):
        self.network = network
        self.error_logger = error_logger
        self.current_mode = "USER"
        # Configurar dispositivo actual por defecto
        self.current_device = self.network.get_device("Router1")
        self.current_interface = None
        self.hostname = "Router1"

    def get_prompt(self):
        """Obtiene el prompt actual según el modo"""
        base_prompt = self.hostname
        if self.current_device:
            base_prompt = self.current_device.name

        return f"{base_prompt}{self.MODES[self.current_mode]}"

    def run(self):
        """Ejecuta el loop principal de la CLI"""
        print("Bienvenido al Simulador de Red LAN")
        print("Escribe 'help' para ver comandos disponibles")
        print("Escribe 'exit' para salir")
        print()

        while True:
            try:
                prompt = self.get_prompt()
                command = input(f"{prompt} ").strip()

                if not command:
                    continue

                if command.lower() in ["exit", "quit"]:
                    if self.current_mode == "USER":
                        print("Saliendo del simulador...")
                        break
                    else:
                        self._handle_exit()
                        continue

                result = self.parse_command(command)
                if result:
                    print(result)

            except KeyboardInterrupt:
                print("\nSaliendo del simulador...")
                break
            except EOFError:
                print("\nSaliendo del simulador...")
                break
            except Exception as e:
                self.error_logger.log_error("SYSTEM", "CRITICAL", f"Error en CLI: {str(e)}", "")
                print(f"Error: {e}")

    def parse_command(self, command):
        """Parsea y ejecuta un comando"""
        parts = command.split()
        if not parts:
            return ""

        cmd = parts[0].lower()

        # Comandos disponibles en cada modo
        if self.current_mode == "USER":
            return self._handle_user_mode(cmd, parts)
        elif self.current_mode == "PRIVILEGED":
            return self._handle_privileged_mode(cmd, parts)
        elif self.current_mode == "CONFIG":
            return self._handle_config_mode(cmd, parts)
        elif self.current_mode == "INTERFACE":
            return self._handle_interface_mode(cmd, parts)

        return self._command_not_found(cmd)

    def _handle_user_mode(self, cmd, parts):
        """Maneja comandos en modo usuario"""
        if cmd == "enable":
            self.current_mode = "PRIVILEGED"
            return ""
        elif cmd == "ping":
            return self._handle_ping(parts)
        elif cmd == "send":
            return self._handle_send(parts)
        elif cmd == "show":
            return self._handle_show_user(parts)
        elif cmd == "help":
            return self._show_help_user()
        else:
            return self._command_not_found(cmd)

    def _handle_privileged_mode(self, cmd, parts):
        """Maneja comandos en modo privilegiado"""
        if cmd == "configure":
            if len(parts) > 1 and parts[1].lower() == "terminal":
                self.current_mode = "CONFIG"
                return ""
        elif cmd == "show":
            return self._handle_show_privileged(parts)
        elif cmd == "ping":
            return self._handle_ping(parts)
        elif cmd == "send":
            return self._handle_send(parts)
        elif cmd == "connect":
            return self._handle_connect(parts)
        elif cmd == "disconnect":
            return self._handle_disconnect(parts)
        elif cmd == "list_devices":
            return self._handle_list_devices()
        elif cmd == "set_device_status":
            return self._handle_set_device_status(parts)
        elif cmd == "tick":
            return self._handle_tick()
        elif cmd == "process":
            return self._handle_tick()  # alias
        elif cmd == "save":
            return self._handle_save(parts)
        elif cmd == "load":
            return self._handle_load(parts)
        elif cmd == "help":
            return self._show_help_privileged()
        elif cmd == "disable":
            self.current_mode = "USER"
            return ""
        else:
            return self._command_not_found(cmd)

    def _handle_config_mode(self, cmd, parts):
        """Maneja comandos en modo configuración global"""
        if cmd == "hostname":
            return self._handle_hostname(parts)
        elif cmd == "interface":
            return self._handle_interface(parts)
        elif cmd == "ip":
            return self._handle_ip_route(parts)
        elif cmd == "policy":
            return self._handle_policy(parts)
        elif cmd == "exit":
            self.current_mode = "PRIVILEGED"
            return ""
        elif cmd == "end":
            self.current_mode = "PRIVILEGED"
            return ""
        elif cmd == "help":
            return self._show_help_config()
        else:
            return self._command_not_found(cmd)

    def _handle_interface_mode(self, cmd, parts):
        """Maneja comandos en modo configuración de interfaz"""
        if cmd == "ip":
            return self._handle_ip_address(parts)
        elif cmd == "shutdown":
            return self._handle_shutdown()
        elif cmd == "no":
            return self._handle_no_shutdown(parts)
        elif cmd == "exit":
            self.current_mode = "CONFIG"
            return ""
        elif cmd == "end":
            self.current_mode = "PRIVILEGED"
            return ""
        elif cmd == "help":
            return self._show_help_interface()
        else:
            return self._command_not_found(cmd)

    # Implementación de comandos específicos
    def _handle_enable(self):
        """Habilita modo privilegiado"""
        self.current_mode = "PRIVILEGED"
        return ""

    def _handle_hostname(self, parts):
        """Cambia el nombre del dispositivo"""
        if len(parts) < 2:
            self.error_logger.log_error("SyntaxError", "ERROR", "Falta nombre del host", "hostname")
            return "Error: Falta nombre del host"

        new_hostname = parts[1]
        if self.current_device:
            self.current_device.name = new_hostname
        self.hostname = new_hostname
        return ""

    def _handle_interface(self, parts):
        """Entra en modo configuración de interfaz"""
        if len(parts) < 2:
            self.error_logger.log_error("SyntaxError", "ERROR", "Falta nombre de interfaz", "interface")
            return "Error: Falta nombre de interfaz"

        iface_name = parts[1]

        if not self.current_device:
            self.error_logger.log_error("CommandDisabled", "ERROR", "No hay dispositivo actual", "interface")
            return "Error: No hay dispositivo actual"

        if not self.current_device.get_interface(iface_name):
            self.current_device.add_interface(iface_name)

        self.current_interface = iface_name
        self.current_mode = "INTERFACE"
        return ""

    def _handle_ip_address(self, parts):
        """Configura dirección IP en interfaz"""
        if not self.current_device or not self.current_interface:
            self.error_logger.log_error("CommandDisabled", "ERROR", "No hay interfaz actual", "ip address")
            return "Error: No hay interfaz actual"

        if len(parts) < 3:
            self.error_logger.log_error("SyntaxError", "ERROR", "Sintaxis: ip address <ip> [mask]", "ip address")
            return "Error: Sintaxis incorrecta"

        ip = parts[2]
        mask = parts[3] if len(parts) > 3 else "255.255.255.0"

        interface = self.current_device.get_interface(self.current_interface)
        interface.set_ip(ip, mask)
        return ""

    def _handle_shutdown(self):
        """Desactiva interfaz"""
        if not self.current_device or not self.current_interface:
            return "Error: No hay interfaz actual"

        interface = self.current_device.get_interface(self.current_interface)
        interface.set_status("down")
        return ""

    def _handle_no_shutdown(self, parts):
        """Activa interfaz"""
        if not self.current_device or not self.current_interface:
            return "Error: No hay interfaz actual"

        if len(parts) > 1 and parts[1] == "shutdown":
            interface = self.current_device.get_interface(self.current_interface)
            interface.set_status("up")
            return ""
        else:
            return "Comando no reconocido"

    def _handle_connect(self, parts):
        """Conecta dos interfaces"""
        if len(parts) < 4:
            self.error_logger.log_error("SyntaxError", "ERROR", "Sintaxis: connect <iface1> <device2> <iface2>", "connect")
            return "Error: Sintaxis incorrecta"

        iface1 = parts[1]
        device2 = parts[2]
        iface2 = parts[3]

        if self.network.connect(iface1, device2, iface2):
            return "Conexión establecida"
        else:
            self.error_logger.log_error("ConnectionError", "ERROR", "No se pudo establecer conexión", "connect")
            return "Error: No se pudo establecer conexión"

    def _handle_disconnect(self, parts):
        """Desconecta dos interfaces"""
        if len(parts) < 4:
            self.error_logger.log_error("SyntaxError", "ERROR", "Sintaxis: disconnect <iface1> <device2> <iface2>", "disconnect")
            return "Error: Sintaxis incorrecta"

        iface1 = parts[1]
        device2 = parts[2]
        iface2 = parts[3]

        if self.network.disconnect(iface1, device2, iface2):
            return "Conexión removida"
        else:
            self.error_logger.log_error("ConnectionError", "ERROR", "No se pudo remover conexión", "disconnect")
            return "Error: No se pudo remover conexión"

    def _handle_list_devices(self):
        """Lista todos los dispositivos"""
        devices = self.network.list_devices()
        if not devices:
            return "No hay dispositivos en la red"

        result = "Devices in network:\n"
        for device_name in devices:
            device = self.network.get_device(device_name)
            status = "online" if device.is_online() else "offline"
            result += f" - {device_name} ({status})\n"
        return result.strip()

    def _handle_set_device_status(self, parts):
        """Cambia estado de dispositivo"""
        if len(parts) < 3:
            self.error_logger.log_error("SyntaxError", "ERROR", "Sintaxis: set_device_status <device> <online|offline>", "set_device_status")
            return "Error: Sintaxis incorrecta"

        device_name = parts[1]
        status = parts[2]

        if self.network.set_device_status(device_name, status):
            return f"Estado de {device_name} cambiado a {status}"
        else:
            self.error_logger.log_error("CommandDisabled", "ERROR", f"Dispositivo {device_name} no encontrado", "set_device_status")
            return f"Error: Dispositivo {device_name} no encontrado"

    def _handle_send(self, parts):
        """Envía un paquete"""
        if len(parts) < 4:
            self.error_logger.log_error("SyntaxError", "ERROR", "Sintaxis: send <source_ip> <dest_ip> <message> [ttl]", "send")
            return "Error: Sintaxis incorrecta"

        source_ip = parts[1]
        dest_ip = parts[2]
        message = " ".join(parts[3:-1]) if len(parts) > 4 else parts[3]
        ttl = int(parts[-1]) if len(parts) > 4 and parts[-1].isdigit() else 64

        success, msg = self.network.send_packet(source_ip, dest_ip, message, ttl)
        if success:
            return msg
        else:
            self.error_logger.log_error("NetworkError", "ERROR", msg, "send")
            return f"Error: {msg}"

    def _handle_ping(self, parts):
        """Simula ping (envía mensaje especial)"""
        if len(parts) < 2:
            self.error_logger.log_error("SyntaxError", "ERROR", "Sintaxis: ping <destination_ip>", "ping")
            return "Error: Sintaxis incorrecta"

        dest_ip = parts[1]
        message = "PING"

        # Encontrar IP fuente del dispositivo actual
        source_ip = None
        if self.current_device:
            for interface in self.current_device.interfaces.values():
                if interface.ip_address and interface.is_up():
                    source_ip = interface.ip_address
                    break

        if not source_ip:
            self.error_logger.log_error("NetworkError", "ERROR", "No hay IP fuente disponible", "ping")
            return "Error: No hay IP fuente disponible"

        success, msg = self.network.send_packet(source_ip, dest_ip, message, 64)
        if success:
            return f"Ping enviado a {dest_ip}"
        else:
            self.error_logger.log_error("NetworkError", "ERROR", msg, "ping")
            return f"Error: {msg}"

    def _handle_tick(self):
        """Avanza un paso de simulación"""
        self.network.tick()
        return "[Tick] Procesamiento completado"

    def _handle_show_user(self, parts):
        """Maneja comandos show en modo usuario"""
        if len(parts) < 2:
            return "Comandos show disponibles: history, queue, statistics, error-log, ip route, ip prefix-tree, route avl-stats, snapshots, btree stats"

        subcmd = parts[1].lower()

        if subcmd == "history":
            device = parts[2] if len(parts) > 2 else None
            return self._show_history(device)
        elif subcmd == "queue":
            device = parts[2] if len(parts) > 2 else None
            return self._show_queue(device)
        elif subcmd == "statistics":
            return self._show_statistics()
        elif subcmd == "error-log":
            limit = int(parts[2]) if len(parts) > 2 and parts[2].isdigit() else None
            return self._show_error_log(limit)
        elif subcmd == "ip" and len(parts) > 2:
            if parts[2] == "route":
                if len(parts) > 3 and parts[3] == "tree":
                    return self._handle_show_ip_route_tree(parts)
                else:
                    return self._handle_show_ip_route(parts)
            elif parts[2] == "prefix-tree":
                return self._handle_show_ip_prefix_tree(parts)
        elif subcmd == "route" and len(parts) > 2 and parts[2] == "avl-stats":
            return self._handle_show_route_avl_stats(parts)
        elif subcmd == "snapshots":
            return self._handle_show_snapshots()
        elif subcmd == "btree" and len(parts) > 2 and parts[2] == "stats":
            return self._handle_show_btree_stats()
        else:
            return f"Comando show '{subcmd}' no reconocido"

    def _handle_show_privileged(self, parts):
        """Maneja comandos show en modo privilegiado"""
        return self._handle_show_user(parts)

    def _show_history(self, device_name=None):
        """Muestra historial de paquetes"""
        if device_name:
            device = self.network.get_device(device_name)
            if not device:
                return f"Dispositivo {device_name} no encontrado"
            history = device.get_history()
        else:
            # Mostrar historial de todos los dispositivos
            history = []
            for device in self.network.devices.values():
                device_history = device.get_history()
                history.extend([(device.name, packet) for packet in device_history])

        if not history:
            return "No hay paquetes en el historial"

        result = "Historial de paquetes:\n"
        for i, item in enumerate(history[-10:], 1):  # Últimos 10
            if isinstance(item, tuple):
                device_name, packet = item
                result += f"{i}) [{device_name}] {packet}\n"
            else:
                result += f"{i}) {item}\n"

        return result.strip()

    def _show_queue(self, device_name=None):
        """Muestra colas de dispositivos"""
        if device_name:
            device = self.network.get_device(device_name)
            if not device:
                return f"Dispositivo {device_name} no encontrado"

            result = f"Colas de {device_name}:\n"
            for iface_name, interface in device.interfaces.items():
                result += f"  {iface_name}: {interface.input_queue.size()} entrada, {interface.output_queue.size()} salida\n"
            return result.strip()

        # Mostrar colas de todos los dispositivos
        result = "Colas de red:\n"
        for device_name, device in self.network.devices.items():
            result += f"{device_name}:\n"
            for iface_name, interface in device.interfaces.items():
                result += f"  {iface_name}: {interface.input_queue.size()} entrada, {interface.output_queue.size()} salida\n"
        return result.strip()

    def _show_statistics(self):
        """Muestra estadísticas de red"""
        stats = self.network.get_network_stats()

        result = "Estadísticas de red:\n"
        result += f"Total packets sent: {stats['total_packets_sent']}\n"
        result += f"Total packets received: {stats['total_packets_received']}\n"
        result += f"Packets dropped: {stats['total_packets_dropped']}\n"
        result += f"Average hops: {stats['average_hops']:.1f}\n"
        result += f"Top talker: {stats['top_talker'] or 'None'}\n"
        result += f"Devices online: {stats['devices_online']}/{stats['total_devices']}"

        return result

    def _show_error_log(self, limit=None):
        """Muestra el registro de errores"""
        errors = self.error_logger.get_recent_errors(limit)

        if not errors:
            return "No hay errores registrados"

        result = "Registro de errores:\n"
        for error in errors:
            result += f"  {error}\n"

        return result.strip()

    def _handle_save(self, parts):
        """Guarda configuración"""
        if len(parts) < 2:
            return "Sintaxis: save running-config"

        if parts[1] == "running-config":
            success, filename = self.network.save_snapshot()
            if success:
                return f"Configuración guardada en {filename}"
            else:
                return "Error al guardar configuración"
        elif parts[1] == "snapshot":
            if len(parts) < 3:
                return "Sintaxis: save snapshot <key>"
            key = parts[2]
            success, filename = self.network.save_snapshot(key)
            if success:
                return f"Snapshot '{key}' guardado en {filename}"
            else:
                return "Error al guardar snapshot"
        else:
            return "Comando save no reconocido"

    def _handle_load(self, parts):
        """Carga configuración"""
        if len(parts) < 3:
            return "Sintaxis: load config <key>"

        if parts[1] == "config":
            key = parts[2]
            success, msg = self.network.load_snapshot(key)
            if success:
                return msg
            else:
                return f"Error: {msg}"
        else:
            return "Comando load no reconocido"

    def _handle_ip_route(self, parts):
        """Maneja comandos de rutas IP"""
        if len(parts) < 2:
            return "Sintaxis: ip route add <prefix> <mask> via <next-hop> [metric N]"

        if parts[1] == "route":
            if len(parts) < 7:
                return "Sintaxis: ip route add <prefix> <mask> via <next-hop> [metric N]"

            if parts[2] == "add":
                prefix = parts[3]
                mask = parts[4]
                next_hop = parts[6]
                metric = int(parts[8]) if len(parts) > 8 and parts[7] == "metric" else 1

                if not self.current_device:
                    return "Error: No hay dispositivo actual"

                self.current_device.add_route(prefix, mask, next_hop, metric)
                return "Ruta agregada"
            elif parts[2] == "del":
                prefix = parts[3]
                mask = parts[4]

                if not self.current_device:
                    return "Error: No hay dispositivo actual"

                self.current_device.remove_route(prefix, mask)
                return "Ruta removida"
            else:
                return "Comando ip route no reconocido"
        else:
            return "Comando ip no reconocido"

    def _handle_policy(self, parts):
        """Maneja comandos de políticas"""
        if len(parts) < 4:
            return "Sintaxis: policy set <prefix> <mask> ttl-min <N> | policy set <prefix> <mask> block | policy unset <prefix> <mask>"

        if parts[1] == "set":
            if len(parts) < 5:
                return "Sintaxis: policy set <prefix> <mask> ttl-min <N> | policy set <prefix> <mask> block"

            prefix = parts[2]
            mask = parts[3]
            policy_type = parts[4]

            if policy_type == "ttl-min":
                if len(parts) < 6:
                    return "Sintaxis: policy set <prefix> <mask> ttl-min <N>"
                try:
                    value = int(parts[5])
                except ValueError:
                    return "Error: El valor de TTL debe ser un número"
            elif policy_type == "block":
                value = True  # Para bloqueo, el valor es True
            else:
                return f"Error: Tipo de política desconocido '{policy_type}'. Use 'ttl-min' o 'block'"

            if not self.current_device:
                return "Error: No hay dispositivo actual"

            self.current_device.set_policy(prefix, mask, policy_type, value)
            return "Política establecida"
        elif parts[1] == "unset":
            if len(parts) < 4:
                return "Sintaxis: policy unset <prefix> <mask>"

            prefix = parts[2]
            mask = parts[3]

            if not self.current_device:
                return "Error: No hay dispositivo actual"

            self.current_device.remove_policy(prefix, mask)
            return "Política removida"
        else:
            return "Comando policy no reconocido"

    def _handle_exit(self):
        """Maneja comando exit según el modo actual"""
        if self.current_mode == "INTERFACE":
            self.current_mode = "CONFIG"
            self.current_interface = None
        elif self.current_mode == "CONFIG":
            self.current_mode = "PRIVILEGED"
            self.current_device = None
        elif self.current_mode == "PRIVILEGED":
            self.current_mode = "USER"

    def _handle_show_ip_route(self, parts):
        """Muestra la tabla de rutas"""
        if not self.current_device:
            return "Error: No hay dispositivo actual"

        routes = self.current_device.get_routing_table()

        if not routes:
            return "No hay rutas configuradas\nDefault: none"

        result = ""
        for route_key, route_value in routes:
            result += f"{route_key}  via {route_value['next_hop']}  metric {route_value['metric']}\n"

        result += "Default: none"
        return result

    def _handle_show_route_avl_stats(self, parts):
        """Muestra estadísticas del árbol AVL de rutas"""
        if not self.current_device:
            return "Error: No hay dispositivo actual"

        stats = self.current_device.routing_table.get_stats()

        result = f"nodes={stats['nodes']} height={stats['height']} "
        result += f"rotations: LL={stats['rotations']['LL']} LR={stats['rotations']['LR']} "
        result += f"RL={stats['rotations']['RL']} RR={stats['rotations']['RR']}"

        return result

    def _handle_show_ip_route_tree(self, parts):
        """Muestra el árbol AVL de rutas en formato visual"""
        if not self.current_device:
            return "Error: No hay dispositivo actual"

        routes = self.current_device.get_routing_table()

        if not routes:
            return "Árbol vacío"

        # Mostrar el árbol usando el método print_tree del AVL
        print("\n=== ÁRBOL AVL DE RUTAS ===")
        self.current_device.routing_table.print_tree()
        print("=" * 30)

        return ""

    def _handle_show_ip_prefix_tree(self, parts):
        """Muestra el trie de prefijos IP en formato visual"""
        if not self.current_device:
            return "Error: No hay dispositivo actual"

        prefixes = self.current_device.policy_trie.get_all_prefixes()

        if not prefixes:
            return "No hay prefijos configurados en el trie"

        # Mostrar el trie usando el método print_trie
        print("\n=== TRIE DE PREFIJOS IP ===")
        self.current_device.policy_trie.print_trie()
        print("=" * 30)

        return ""

    def _handle_show_snapshots(self):
        """Muestra todos los snapshots disponibles"""
        snapshots = self.network.get_snapshots()

        if not snapshots:
            return "No hay snapshots guardados"

        result = "Snapshots disponibles:\n"
        for key, filename in snapshots:
            result += f"  {key} -> {filename}\n"

        return result.strip()

    def _handle_show_btree_stats(self):
        """Muestra estadísticas del B-tree de snapshots"""
        stats = self.network.snapshots.get_stats()

        result = f"order={stats['order']} height={stats['height']} "
        result += f"nodes={stats['nodes']} splits={stats['splits']} merges={stats['merges']}"

        return result

    def _command_not_found(self, cmd):
        """Maneja comando no encontrado"""
        self.error_logger.log_error("CommandNotFound", "WARNING", f"Comando '{cmd}' no reconocido", cmd)
        return f"Comando '{cmd}' no encontrado. Escribe 'help' para ver comandos disponibles."

    # Funciones de ayuda
    def _show_help_user(self):
        """Muestra ayuda en modo usuario"""
        help_text = """
Comandos disponibles en modo Usuario:
  enable                    - Entra en modo privilegiado
  ping <dest_ip>           - Envía ping a dirección IP
  send <src> <dst> <msg>   - Envía mensaje
  show history [device]    - Muestra historial de paquetes
  show queue [device]      - Muestra colas de dispositivos
  show statistics          - Muestra estadísticas de red
  show error-log [n]       - Muestra registro de errores
  show ip route            - Muestra tabla de rutas
  show ip prefix-tree      - Muestra trie de prefijos IP
  show route avl-stats     - Muestra estadísticas del AVL
  show snapshots           - Muestra snapshots guardados
  show btree stats         - Muestra estadísticas del B-tree
  help                     - Muestra esta ayuda
  exit                     - Sale del simulador
        """
        return help_text.strip()

    def _show_help_privileged(self):
        """Muestra ayuda en modo privilegiado"""
        help_text = """
Comandos disponibles en modo Privilegiado:
  configure terminal       - Entra en modo configuración
  show ...                 - Comandos show (igual que modo usuario)
  connect <i1> <d2> <i2>   - Conecta interfaces
  disconnect <i1> <d2> <i2>- Desconecta interfaces
  list_devices             - Lista dispositivos
  set_device_status <d> <s>- Cambia estado de dispositivo
  tick                     - Avanza simulación
  process                  - Alias para tick
  save running-config      - Guarda configuración
  save snapshot <key>      - Guarda snapshot nombrado
  load config <key>        - Carga configuración por clave
  disable                  - Vuelve a modo usuario
  exit                     - Vuelve a modo usuario
        """
        return help_text.strip()

    def _show_help_config(self):
        """Muestra ayuda en modo configuración"""
        help_text = """
Comandos disponibles en modo Configuración:
  hostname <name>          - Cambia nombre del dispositivo
  interface <name>         - Configura interfaz
  ip route add ...         - Agrega ruta
  ip route del ...         - Elimina ruta
  policy set <p> <m> ttl-min <N> - Establece límite TTL
  policy set <p> <m> block      - Bloquea prefijo
  policy unset <p> <m>          - Remueve política
  exit                     - Vuelve a modo privilegiado
  end                      - Vuelve a modo privilegiado
        """
        return help_text.strip()

    def _show_help_interface(self):
        """Muestra ayuda en modo configuración de interfaz"""
        help_text = """
Comandos disponibles en modo Configuración de Interfaz:
  ip address <ip> [mask]   - Configura dirección IP
  shutdown                 - Desactiva interfaz
  no shutdown              - Activa interfaz
  exit                     - Vuelve a modo configuración
  end                      - Vuelve a modo privilegiado
        """
        return help_text.strip()
