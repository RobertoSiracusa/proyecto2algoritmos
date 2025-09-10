"""
Sistema de registro de errores para el simulador
"""

from data_structures import Queue
from datetime import datetime

class ErrorEntry:
    """Representa una entrada de error en el log"""

    def __init__(self, error_type, severity, message, command=""):
        self.timestamp = datetime.now()
        self.error_type = error_type  # "SyntaxError", "ConnectionError", "CommandDisabled", etc.
        self.severity = severity  # "INFO", "WARNING", "ERROR", "CRITICAL"
        self.message = message
        self.command = command

    def __str__(self):
        time_str = self.timestamp.strftime("%Y-%m-%d %H:%M:%S")
        cmd_str = f" | Command: '{self.command}'" if self.command else ""
        return f"[{time_str}] {self.severity} - {self.error_type}: {self.message}{cmd_str}"

    def get_summary(self):
        """Obtiene un resumen de la entrada para reportes"""
        return {
            "timestamp": self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            "type": self.error_type,
            "severity": self.severity,
            "message": self.message,
            "command": self.command
        }

class ErrorLogger:
    """Sistema de logging de errores usando cola FIFO"""

    def __init__(self):
        self.error_queue = Queue()
        self.max_entries = 1000  # Límite máximo de entradas

    def log_error(self, error_type, severity, message, command=""):
        """Registra un nuevo error"""
        error_entry = ErrorEntry(error_type, severity, message, command)
        self.error_queue.enqueue(error_entry)

        # Mantener el límite de entradas
        if self.error_queue.size() > self.max_entries:
            self.error_queue.dequeue()  # Remover el más antiguo

    def get_recent_errors(self, limit=None):
        """Obtiene los errores más recientes"""
        errors = []
        temp_queue = Queue()

        # Vaciar la cola para obtener los elementos en orden
        while not self.error_queue.is_empty():
            error = self.error_queue.dequeue()
            errors.append(error)
            temp_queue.enqueue(error)

        # Restaurar la cola original
        while not temp_queue.is_empty():
            self.error_queue.enqueue(temp_queue.dequeue())

        # Aplicar límite si se especifica
        if limit:
            errors = errors[-limit:]

        return errors

    def get_errors_by_type(self, error_type):
        """Obtiene errores de un tipo específico"""
        errors = []
        temp_queue = Queue()

        # Recorrer la cola
        while not self.error_queue.is_empty():
            error = self.error_queue.dequeue()
            if error.error_type == error_type:
                errors.append(error)
            temp_queue.enqueue(error)

        # Restaurar la cola original
        while not temp_queue.is_empty():
            self.error_queue.enqueue(temp_queue.dequeue())

        return errors

    def get_errors_by_severity(self, severity):
        """Obtiene errores de una severidad específica"""
        errors = []
        temp_queue = Queue()

        # Recorrer la cola
        while not self.error_queue.is_empty():
            error = self.error_queue.dequeue()
            if error.severity == severity:
                errors.append(error)
            temp_queue.enqueue(error)

        # Restaurar la cola original
        while not temp_queue.is_empty():
            self.error_queue.enqueue(temp_queue.dequeue())

        return errors

    def clear_errors(self):
        """Limpia todos los errores"""
        self.error_queue.clear()

    def get_error_counts(self):
        """Obtiene conteo de errores por tipo y severidad"""
        type_counts = {}
        severity_counts = {}
        temp_queue = Queue()

        # Recorrer la cola
        while not self.error_queue.is_empty():
            error = self.error_queue.dequeue()

            # Contar por tipo
            if error.error_type not in type_counts:
                type_counts[error.error_type] = 0
            type_counts[error.error_type] += 1

            # Contar por severidad
            if error.severity not in severity_counts:
                severity_counts[error.severity] = 0
            severity_counts[error.severity] += 1

            temp_queue.enqueue(error)

        # Restaurar la cola original
        while not temp_queue.is_empty():
            self.error_queue.enqueue(temp_queue.dequeue())

        return {
            "by_type": type_counts,
            "by_severity": severity_counts,
            "total": self.error_queue.size()
        }

    def __len__(self):
        """Retorna el número de errores registrados"""
        return self.error_queue.size()
