"""
Implementación de la clase Packet para el simulador de red
"""

import uuid
from datetime import datetime

class Packet:
    """Representa un paquete de red en el simulador"""

    def __init__(self, source_ip, destination_ip, message="", ttl=64):
        self.id = str(uuid.uuid4())[:8]  # ID único corto
        self.source_ip = source_ip
        self.destination_ip = destination_ip
        self.message = message
        self.ttl = ttl  # Time To Live
        self.path = []  # Lista de dispositivos por los que ha pasado
        self.timestamp = datetime.now()
        self.arrival_time = None  # Timestamp de llegada al destino
        self.ttl_expired = False

    def add_to_path(self, device_name):
        """Agrega un dispositivo al camino del paquete"""
        if device_name not in self.path:
            self.path.append(device_name)

    def decrement_ttl(self):
        """Decrementa el TTL y marca si expiró"""
        self.ttl -= 1
        if self.ttl <= 0:
            self.ttl_expired = True
        return self.ttl > 0

    def mark_arrived(self):
        """Marca el paquete como llegado a destino"""
        self.arrival_time = datetime.now()

    def get_hops(self):
        """Obtiene el número de saltos realizados"""
        return len(self.path) - 1 if len(self.path) > 1 else 0

    def __str__(self):
        ttl_status = "EXPIRED" if self.ttl_expired else f"TTL={self.ttl}"
        hops = self.get_hops()
        path_str = " -> ".join(self.path) if self.path else "No path"
        return f"Packet {self.id}: {self.source_ip} -> {self.destination_ip} | {ttl_status} | Hops: {hops} | Path: {path_str}"

    def get_summary(self):
        """Obtiene un resumen del paquete para reportes"""
        return {
            "id": self.id,
            "source": self.source_ip,
            "destination": self.destination_ip,
            "message": self.message[:50] + "..." if len(self.message) > 50 else self.message,
            "ttl_at_arrival": self.ttl,
            "ttl_expired": self.ttl_expired,
            "hops": self.get_hops(),
            "path": self.path.copy(),
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        }
