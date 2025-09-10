# Simulador de Red LAN - Proyecto 2 Algoritmos

Un simulador completo de red de área local (LAN) implementado en Python, con una interfaz de línea de comandos (CLI) inspirada en Cisco IOS. El proyecto implementa estructuras de datos avanzadas desde cero y proporciona una experiencia realista de configuración y administración de redes.

## 🚀 Características Principales

### 📊 Estructuras de Datos Implementadas
- **Lista Enlazada**: Para almacenamiento dinámico de vecinos y conexiones
- **Cola (Queue)**: Para gestión de paquetes entrantes/salientes
- **Pila (Stack)**: Para historial de paquetes recibidos
- **Árbol AVL**: Para tabla de rutas balanceada con O(log n) garantizado
- **B-Tree**: Para índice persistente de snapshots de configuración
- **Trie N-ario**: Para prefijos IP y políticas jerárquicas

### 🖥️ Dispositivos Soportados
- **Routers**: Enrutamiento completo con tabla de rutas AVL
- **Switches**: Conmutación a nivel 2
- **Hosts**: Dispositivos finales (computadoras)
- **Firewalls**: Con capacidades de filtrado (futuro)

### 🔧 Funcionalidades CLI
- **Modos múltiples**: Usuario, Privilegiado, Configuración Global, Configuración de Interfaz
- **Comandos completos**: Inspirados en Cisco IOS
- **Sistema de ayuda**: Ayuda contextual en cada modo
- **Validación de sintaxis**: Detección y reporte de errores

## 📁 Estructura del Proyecto

```
proyecto2algoritmos/
├── main.py                 # Archivo principal del simulador
├── test_structures.py      # Pruebas de estructuras de datos
├── simple_test.py         # Pruebas básicas
├── data_structures/       # Implementaciones de estructuras
│   ├── __init__.py
│   ├── linked_list.py     # Lista enlazada
│   ├── queue.py          # Cola FIFO
│   ├── stack.py          # Pila LIFO
│   ├── avl_tree.py       # Árbol AVL para rutas
│   ├── b_tree.py         # B-Tree para índices
│   └── trie.py           # Trie para prefijos IP
├── network/              # Lógica de red
│   ├── __init__.py
│   ├── device.py         # Clase Device e Interface
│   ├── network.py        # Clase Network
│   └── packet.py         # Clase Packet
├── cli/                  # Interfaz de comandos
│   ├── __init__.py
│   └── cli_parser.py     # Parser CLI con modos
└── utils/                # Utilidades
    ├── __init__.py
    └── error_logger.py   # Sistema de logging de errores
```

## 🎯 Uso del Simulador

### Inicio Rápido

```bash
# Ejecutar el simulador
python main.py
```

Al iniciar, el simulador crea automáticamente:
- **Router1** con IP 192.168.1.1
- **Switch1** (switch básico)
- **PC1** con IP 192.168.1.10
- **PC2** con IP 192.168.1.20
- **Conexiones**: Router1 ↔ PC1, Router1 ↔ PC2
- **Rutas pre-configuradas** en Router1:
  - 10.0.0.0/24 via 192.168.1.100 metric 10
  - 172.16.0.0/16 via 192.168.1.200 metric 5
  - 192.168.2.0/24 via 192.168.1.50 metric 15
  - 0.0.0.0/0 via 192.168.1.254 metric 100 (default)

### Comandos Básicos

#### Modo Usuario
```
Router1> enable              # Entrar a modo privilegiado
Router1> ping 192.168.1.10   # Enviar ping
Router1> send 192.168.1.1 192.168.1.10 "Hola"  # Enviar mensaje
Router1> help                # Ver ayuda
Router1> exit                # Salir
```

#### Modo Privilegiado
```
Router1# configure terminal           # Entrar a configuración
Router1# show history                 # Ver historial de paquetes
Router1# show statistics              # Ver estadísticas de red
Router1# show error-log               # Ver registro de errores
Router1# show ip route                # Ver tabla de rutas
Router1# show route avl-stats         # Ver estadísticas del AVL
Router1# show ip route-tree           # Ver árbol AVL visualmente
Router1# connect g0/0 PC1 eth0        # Conectar interfaces
Router1# list_devices                 # Listar dispositivos
Router1# tick                         # Avanzar simulación
Router1# disable                      # Volver a modo usuario
```

#### Modo Configuración
```
Router1(config)# hostname RouterCentral   # Cambiar nombre
Router1(config)# interface g0/1          # Configurar interfaz
Router1(config)# ip route add 10.0.0.0 255.255.255.0 via 192.168.1.2  # Agregar ruta
Router1(config)# policy set 192.168.1.0 255.255.255.0 block  # Establecer política
Router1(config)# exit                     # Volver a privilegiado
Router1(config)# end                      # Volver a privilegiado
```

#### Modo Configuración de Interfaz
```
Router1(config-if)# ip address 10.0.0.1 255.255.255.0  # Configurar IP
Router1(config-if)# no shutdown             # Activar interfaz
Router1(config-if)# shutdown                # Desactivar interfaz
Router1(config-if)# exit                    # Volver a configuración
Router1(config-if)# end                     # Volver a privilegiado
```

## 🔍 Estructuras de Datos Detalladas

### Lista Enlazada
```python
from data_structures import LinkedList

ll = LinkedList()
ll.append("A")
ll.append("B")
ll.prepend("Z")  # Z -> A -> B
print(ll)  # [Z -> A -> B]
```

### Cola (Queue)
```python
from data_structures import Queue

q = Queue()
q.enqueue("primero")
q.enqueue("segundo")
print(q.dequeue())  # "primero"
```

### Pila (Stack)
```python
from data_structures import Stack

s = Stack()
s.push("primero")
s.push("segundo")
print(s.pop())  # "segundo"
```

### Árbol AVL
```python
from data_structures import AVLTree

avl = AVLTree()
avl.insert_key("10.0.0.0/24", {"next_hop": "192.168.1.2", "metric": 10})
print(avl.get_stats())  # {"nodes": 1, "height": 1, "rotations": {...}}
```

### B-Tree
```python
from data_structures import BTree

bt = BTree(order=4)
bt.insert("snapshot_001", "config1.txt")
bt.insert("lab_grupoA", "lab_config.txt")
print(bt.get_stats())  # {"order": 4, "height": 1, "nodes": 1, ...}
```

### Trie N-ario
```python
from data_structures import Trie

trie = Trie()
trie.insert("192.168.1.0", "255.255.255.0", {"block": True})
prefix, policy = trie.search_longest_prefix("192.168.1.10")
print(f"{prefix} -> {policy}")  # "192.168.1.0/24 -> {'block': True}"
```

### Políticas de Red con Trie
```python
# El trie se integra automáticamente en el dispositivo
device = network.get_device("Router1")

# Políticas se aplican automáticamente antes del reenvío
route = device.find_route("192.168.1.10")  # Consulta trie primero

# Si hay política de bloqueo, retorna None
# Si hay política ttl-min, se verifica antes de enviar
```

### B-Tree para Snapshots
```python
from data_structures import BTree

# El B-tree se usa internamente en la clase Network
btree = BTree(order=4)  # Orden 4 (máximo 4 hijos por nodo)
btree.insert("laboratorio", "snapshots/laboratorio.cfg")
btree.insert("2025-08-12T09:30", "snapshots/2025-08-12T09:30.cfg")

# Recorrer todos los snapshots en orden
for key, filename in btree.get_all_entries():
    print(f"{key} -> {filename}")

# Obtener estadísticas
stats = btree.get_stats()
print(f"Orden: {stats['order']}, Altura: {stats['height']}")
print(f"Splits: {stats['splits']}, Merges: {stats['merges']}")
```

## 📈 Estadísticas y Monitoreo

### Estadísticas de Red
```
Router1# show statistics
Total packets sent: 15
Total packets received: 13
Packets dropped: 2
Average hops: 2.1
Top talker: Router1 (processed 20 packets)
Devices online: 4/4
```

### Estadísticas de Rutas AVL
```
Router1# show route avl-stats
nodes=4 height=3 rotations: LL=1 LR=0 RL=0 RR=1
```

### Visualización del Árbol AVL
```
Router1# show ip route-tree
=== ÁRBOL AVL DE RUTAS ===
            [172.16.0.0/16]
        /                       \
[10.0.0.0/24]                [192.168.2.0/24]
                            /                \
                [192.168.1.0/24]        [0.0.0.0/0]
==============================

### Estadísticas de Estructuras
```python
# Estadísticas AVL
stats = device.routing_table.get_stats()
print(f"Nodos: {stats['nodes']}, Altura: {stats['height']}")
print(f"Rotaciones: LL={stats['rotations']['LL']}, LR={stats['rotations']['LR']}")

# Estadísticas B-Tree de snapshots
stats = network.snapshots.get_stats()
print(f"Orden: {stats['order']}, Altura: {stats['height']}")
print(f"Splits: {stats['splits']}, Merges: {stats['merges']}")
```

### Gestión de Snapshots con B-Tree
```
Router1# save snapshot laboratorio
Snapshot 'laboratorio' guardado en snapshots/laboratorio.cfg

Router1# show snapshots
laboratorio -> snapshots/laboratorio.cfg

Router1# show btree stats
order=4 height=1 nodes=1 splits=0 merges=0

Router1# load config laboratorio
Configuration loaded successfully.
Devices and connections restored.
```

## 💾 Persistencia de Configuración

### Guardar Configuración
```
Router1# save running-config          # Guardar como running-config.txt
Router1# save snapshot laboratorio    # Guardar snapshot nombrado
```

### Cargar Configuración
```
Router1# load config laboratorio      # Cargar snapshot
Configuration loaded successfully.
Devices and connections restored.
```

### Formato de Archivo de Configuración
```
hostname Router1
interface g0/0
  ip address 192.168.1.1
  no shutdown
exit
interface g0/1
  ip address 10.0.0.1
exit

hostname PC1
interface eth0
  ip address 192.168.1.10
exit

connect Router1 g0/0 PC1 eth0
connect Router1 g0/1 PC2 eth0

ip route add 10.0.0.0 255.255.255.0 via 192.168.1.2 metric 10
policy set 192.168.1.0 255.255.255.0 ttl-min 5
```

## 🐛 Sistema de Registro de Errores

### Ver Errores
```
Router1# show error-log        # Ver todos los errores
Router1# show error-log 5      # Ver últimos 5 errores
```

### Tipos de Errores Registrados
- **SyntaxError**: Errores de sintaxis en comandos
- **ConnectionError**: Errores de conexión entre dispositivos
- **CommandDisabled**: Comando no disponible en modo actual
- **NetworkError**: Errores de red (IP no encontrada, etc.)
- **PolicyViolation**: Paquetes descartados por violar políticas
- **NoRouteToHost**: No se encontró ruta para el destino
- **TTLExpired**: TTL expiró durante el tránsito
- **SystemError**: Errores del sistema

### Flujo de Procesamiento con Logging
```
Paquete llega → Lookup en Trie de políticas
    ↓
Si viola política → Descartar + Log PolicyViolation
    ↓
Si pasa → Lookup en tabla AVL
    ↓
Si no hay ruta → Descartar + Log NoRouteToHost
    ↓
Si hay ruta → Validar con ARP
    ↓
Enviar paquete → Decrementar TTL
    ↓
Si TTL ≤ 0 → Descartar + Log TTLExpired
```

## 🎯 Ejemplos de Uso Completo

### Sesión Completa con Rutas Pre-configuradas
```
=== Simulador de Red LAN ===
Inspirado en Cisco IOS

Dispositivos inicializados:
- Router1 (router) con IP 192.168.1.1
- PC1 (host) con IP 192.168.1.10
- PC2 (host) con IP 192.168.1.20

Rutas configuradas en Router1:
- 10.0.0.0/24 via 192.168.1.100 metric 10
- 172.16.0.0/16 via 192.168.1.200 metric 5
- 192.168.2.0/24 via 192.168.1.50 metric 15
- 0.0.0.0/0 via 192.168.1.254 metric 100 (default)

Router1> enable
Router1# show ip route
10.0.0.0/24 via 192.168.1.100 metric 10
172.16.0.0/16 via 192.168.1.200 metric 5
192.168.2.0/24 via 192.168.1.50 metric 15
0.0.0.0/0 via 192.168.1.254 metric 100
Default: none

Router1# show route avl-stats
nodes=4 height=3 rotations: LL=1 LR=0 RL=0 RR=1

Router1# show ip route-tree
=== ÁRBOL AVL DE RUTAS ===
            [172.16.0.0/16]
        /                       \
[10.0.0.0/24]                [192.168.2.0/24]
                            /                \
                [192.168.1.0/24]        [0.0.0.0/0]
==============================

Router1# ping 192.168.1.10
Ping enviado a 192.168.1.10

Router1# show statistics
Total packets sent: 1
Total packets received: 0
Packets dropped: 0
Average hops: 0.0
Top talker: Router1 (processed 1 packets)
Devices online: 3/3
```

### Configuración Básica de Red
```
Router1> enable
Router1# configure terminal
Router1(config)# hostname RouterCentral
Router1(config)# interface g0/0
Router1(config-if)# ip address 192.168.1.1 255.255.255.0
Router1(config-if)# no shutdown
Router1(config-if)# exit
Router1(config)# exit
Router1# show statistics
```

### Envío de Paquetes
```
Router1# send 192.168.1.1 192.168.1.10 "Hola desde Router1"
Message queued for delivery.

Router1# tick
[Tick] Router1 → PC1: packet received (TTL=63)

PC1# show history
1) From 192.168.1.1 to 192.168.1.10: "Hola desde Router1" | TTL at arrival: 63 | Path: Router1 → PC1
```

### Visualización de Rutas Pre-configuradas
```
Router1# show ip route
10.0.0.0/24 via 192.168.1.100 metric 10
172.16.0.0/16 via 192.168.1.200 metric 5
192.168.2.0/24 via 192.168.1.50 metric 15
0.0.0.0/0 via 192.168.1.254 metric 100
Default: none
```

### Estadísticas del Árbol AVL
```
Router1# show route avl-stats
nodes=4 height=3 rotations: LL=1 LR=0 RL=0 RR=1
```

### Configuración de Rutas Adicionales
```
Router1(config)# ip route add 10.0.0.0 255.255.255.0 via 192.168.1.2 metric 10
Router1(config)# ip route add 172.16.0.0 255.255.0.0 via 192.168.1.3 metric 5
Router1(config)# ip route del 192.168.2.0 255.255.255.0
```

### Configuración de Políticas con Trie
```
Router1(config)# policy set 192.168.1.0 255.255.255.0 block
Política establecida

Router1(config)# policy set 10.0.0.0 255.255.0.0 ttl-min 5
Política establecida

Router1# show ip prefix-tree
=== TRIE DE PREFIJOS IP ===
192.168.1.0/24 {'block': True}
├── 10.0.0.0/16 {'ttl-min': 5}
==============================

Router1(config)# policy unset 192.168.1.0 255.255.255.0
Política removida
```

### Gestión de Snapshots con B-Tree
```
Router1# save snapshot laboratorio
Snapshot 'laboratorio' guardado en snapshots/laboratorio.cfg

Router1# save snapshot 2025-08-12T09:30
Snapshot '2025-08-12T09:30' guardado en snapshots/2025-08-12T09:30.cfg

Router1# show snapshots
laboratorio -> snapshots/laboratorio.cfg
2025-08-12T09:30 -> snapshots/2025-08-12T09:30.cfg

Router1# show btree stats
order=4 height=1 nodes=2 splits=0 merges=0

Router1# load config laboratorio
Configuration loaded successfully.
Devices and connections restored.
```

### Políticas de Red
```
Router1(config)# policy set 192.168.2.0 255.255.255.0 block
Router1(config)# policy set 10.0.0.0 255.255.0.0 ttl-min 5
Router1# show ip prefix-tree
192.168.2.0/24 {block}
└── 10.0.0.0/16 {ttl-min=5}
```

## 🔧 Requisitos del Sistema

- **Python**: 3.6+
- **SO**: Windows, Linux, macOS
- **Memoria**: 128MB mínimo
- **Espacio**: 10MB para configuraciones y logs

## 📝 Notas de Implementación

### Configuración Automática
- **Rutas pre-configuradas**: 4 rutas de ejemplo se configuran automáticamente al iniciar
- **Topología básica**: Router1 conectado a PC1 y PC2 con IPs realistas
- **Demostración inmediata**: Todos los comandos de rutas funcionan sin configuración adicional

### Índice Persistente con B-Tree
- **Snapshots de configuración**: Cada `save snapshot` crea un archivo y lo indexa en B-tree
- **Claves flexibles**: Soporta timestamps (2025-08-12T09:30) o nombres ("lab-grupoA")
- **Búsqueda O(log n)**: Inserciones y búsquedas eficientes incluso con muchos snapshots
- **Persistencia en disco**: Los archivos se guardan en directorio `snapshots/`
- **Recorrido ordenado**: `show snapshots` muestra todos los snapshots en orden

### Árboles Balanceados
- **AVL**: Garantiza O(log n) para inserción, búsqueda y eliminación
- **B-Tree**: Optimizado para almacenamiento en disco con operaciones split/merge
- **Trie**: Eficiente para longest-prefix matching

### Complejidad Algorítmica
- **Inserción/Búsqueda AVL**: O(log n)
- **Inserción/Búsqueda B-Tree**: O(log n) con operaciones split/merge
- **Longest Prefix Match Trie**: O(longitud_prefijo)
- **Procesamiento de colas**: O(1) por operación

### Limitaciones
- Simulación simplificada (no hay colisiones reales de red)
- IPv4 únicamente
- No hay soporte completo para protocolos de red reales
- Memoria limitada para entornos de producción
- Rutas pre-configuradas son ejemplos (no rutas "reales")
- Snapshots se almacenan localmente (no en base de datos distribuida)

## 🤝 Contribución

Para contribuir al proyecto:
1. Fork el repositorio
2. Crea una rama para tu feature
3. Implementa tus cambios
4. Agrega pruebas
5. Envía un pull request

## 📄 Licencia

Este proyecto es parte del curso de Algoritmos y Estructuras de Datos.

---

## 🔍 Módulo B-Tree: Índice Persistente de Configuraciones

### Descripción
Este módulo implementa un **B-Tree balanceado** como índice persistente para snapshots de configuración y logs. Cada snapshot se guarda como archivo en disco y se indexa en el B-tree para búsquedas eficientes.

### Características Técnicas
- **Orden configurable**: Por defecto orden 4 (máximo 4 hijos por nodo)
- **Claves flexibles**: Soporta strings, timestamps, nombres descriptivos
- **Valores**: Punteros a archivos de configuración en disco
- **Operaciones O(log n)**: Inserción, búsqueda y eliminación
- **Auto-balance**: Operaciones split/merge automáticas

### Comandos Implementados
```bash
# Guardar snapshots
save running-config          # Guarda configuración actual
save snapshot <key>          # Guarda snapshot con clave específica

# Cargar snapshots
load config <key>            # Carga configuración por clave

# Visualizar información
show snapshots               # Lista todos los snapshots
show btree stats             # Estadísticas del B-tree
```

### Ejemplo de Uso Completo
```
Router1# save snapshot laboratorio
Snapshot 'laboratorio' guardado en snapshots/laboratorio.cfg

Router1# save snapshot backup_2024
Snapshot 'backup_2024' guardado en snapshots/backup_2024.cfg

Router1# show snapshots
laboratorio -> snapshots/laboratorio.cfg
backup_2024 -> snapshots/backup_2024.cfg

Router1# show btree stats
order=4 height=1 nodes=2 splits=0 merges=0

Router1# load config laboratorio
Configuration loaded successfully.
Devices and connections restored.
```

### Estructura de Archivos
```
proyecto2algoritmos/
├── snapshots/
│   ├── laboratorio.cfg
│   ├── backup_2024.cfg
│   └── 2025-08-12T09:30.cfg
└── data_structures/
    └── b_tree.py  # Implementación del B-tree
```

### Ventajas del Diseño
- ✅ **Eficiencia**: Búsquedas O(log n) incluso con miles de snapshots
- ✅ **Persistencia**: Los archivos se mantienen en disco
- ✅ **Flexibilidad**: Claves pueden ser cualquier string
- ✅ **Escalabilidad**: Maneja grandes volúmenes de snapshots
- ✅ **Integridad**: Auto-balance garantiza rendimiento consistente

---

## 🔍 Módulo Trie: Políticas Jerárquicas de Prefijos IP

### Descripción
Este módulo implementa un **Trie N-ario** para la gestión eficiente de prefijos IP y políticas de red. Cada nodo del trie representa un octeto (0-255) del prefijo IP, permitiendo búsquedas de longest-prefix match en O(longitud_prefijo).

### Características Técnicas
- **Estructura jerárquica**: Cada nodo representa un octeto IP (0-255)
- **Longest prefix match**: Encuentra el prefijo más específico que coincide
- **Políticas heredadas**: Las políticas se aplican automáticamente a subprefijos
- **Consulta integrada**: Se ejecuta automáticamente antes del reenvío de paquetes
- **Tipos de políticas**: Bloqueo de tráfico y límites de TTL

### Comandos Implementados
```bash
# Configuración de políticas
policy set <prefix> <mask> ttl-min <N>    # Límite de TTL
policy set <prefix> <mask> block          # Bloquear tráfico
policy unset <prefix> <mask>              # Remover política

# Visualización
show ip prefix-tree                       # Estructura jerárquica del trie
```

### Aplicación Automática de Políticas
```python
# El trie se consulta automáticamente en el proceso de reenvío
def find_route(self, destination_ip):
    # 1. Buscar política en el trie (longest prefix match)
    prefix_match, policy = self.policy_trie.search_longest_prefix(destination_ip)

    # 2. Aplicar política si existe
    if policy and policy.get("block"):
        return None  # Bloquear el paquete

    # 3. Continuar con búsqueda en tabla de rutas AVL
    # ... búsqueda normal en AVL
```

### Ejemplo de Uso Completo
```
Router1(config)# policy set 192.168.1.0 255.255.255.0 block
Política establecida

Router1(config)# policy set 10.0.0.0 255.255.0.0 ttl-min 5
Política establecida

Router1# show ip prefix-tree
=== TRIE DE PREFIJOS IP ===
192.168.1.0/24 {'block': True}
├── 10.0.0.0/16 {'ttl-min': 5}
==============================

Router1# ping 192.168.1.10
Error: No hay ruta disponible (paquete bloqueado por política)
```

### Estructura de Archivos
```
proyecto2algoritmos/
├── data_structures/
│   └── trie.py              # Implementación completa del Trie
└── network/
    └── device.py            # Integración con policy_trie
```

### Ventajas del Diseño
- ✅ **Eficiencia O(W)**: Donde W es la longitud del prefijo (máximo 32 para IPv4)
- ✅ **Longest prefix match**: Encuentra automáticamente el prefijo más específico
- ✅ **Herencia automática**: Políticas se aplican a todos los subprefijos
- ✅ **Integración transparente**: Funciona automáticamente en el proceso de reenvío
- ✅ **Flexibilidad**: Soporta múltiples tipos de políticas (bloqueo, TTL, QoS)

---

## 🔍 Módulo B-Tree: Índice Persistente de Configuraciones

### Descripción
Este módulo implementa un **B-Tree balanceado** como índice persistente para snapshots de configuración y logs. Cada snapshot se guarda como archivo en disco y se indexa en el B-tree para búsquedas eficientes.

### Características Técnicas
- **Orden configurable**: Por defecto orden 4 (máximo 4 hijos por nodo)
- **Claves flexibles**: Soporta strings, timestamps, nombres descriptivos
- **Valores**: Punteros a archivos de configuración en disco
- **Operaciones O(log n)**: Inserción, búsqueda y eliminación
- **Auto-balance**: Operaciones split/merge automáticas

### Comandos Implementados
```bash
# Guardar snapshots
save running-config          # Guarda configuración actual
save snapshot <key>          # Guarda snapshot con clave específica

# Cargar snapshots
load config <key>            # Carga configuración por clave

# Visualizar información
show snapshots               # Lista todos los snapshots
show btree stats             # Estadísticas del B-tree
```

### Ejemplo de Uso Completo
```
Router1# save snapshot laboratorio
Snapshot 'laboratorio' guardado en snapshots/laboratorio.cfg

Router1# save snapshot backup_2024
Snapshot 'backup_2024' guardado en snapshots/backup_2024.cfg

Router1# show snapshots
laboratorio -> snapshots/laboratorio.cfg
backup_2024 -> snapshots/backup_2024.cfg

Router1# show btree stats
order=4 height=1 nodes=2 splits=0 merges=0

Router1# load config laboratorio
Configuration loaded successfully.
Devices and connections restored.
```

### Estructura de Archivos
```
proyecto2algoritmos/
├── snapshots/
│   ├── laboratorio.cfg
│   ├── backup_2024.cfg
│   └── 2025-08-12T09:30.cfg
├── data_structures/
│   └── b_tree.py  # Implementación del B-tree
└── network/
    └── network.py # Integración con self.snapshots
```

### Ventajas del Diseño
- ✅ **Eficiencia**: Búsquedas O(log n) incluso con miles de snapshots
- ✅ **Persistencia**: Los archivos se mantienen en disco
- ✅ **Flexibilidad**: Claves pueden ser cualquier string
- ✅ **Escalabilidad**: Maneja grandes volúmenes de snapshots
- ✅ **Integridad**: Auto-balance garantiza rendimiento consistente

---

## 🔍 Módulo de Registro de Errores

### Descripción
Este módulo implementa un **sistema completo de logging de errores** usando una cola FIFO para almacenar errores en tiempo real durante la ejecución del simulador.

### Características Técnicas
- **Cola FIFO**: Errores se almacenan en orden cronológico
- **Límite máximo**: 1000 entradas para evitar consumo excesivo de memoria
- **Campos completos**: Timestamp, tipo, severidad, mensaje y comando relacionado
- **Consulta ordenada**: Los errores se muestran en orden de ocurrencia
- **Filtrado opcional**: Posibilidad de limitar número de errores mostrados

### Comandos Implementados
```bash
show error-log          # Mostrar todos los errores
show error-log [n]      # Mostrar últimos n errores
```

### Estructura de la Cola FIFO
```python
class ErrorLogger:
    def __init__(self):
        self.error_queue = Queue()  # Cola FIFO
        self.max_entries = 1000
    
    def log_error(self, error_type, severity, message, command):
        # Enqueue al final de la cola
        error_entry = ErrorEntry(error_type, severity, message, command)
        self.error_queue.enqueue(error_entry)
    
    def get_recent_errors(self, limit=None):
        # Dequeue desde el principio (más antiguos primero)
        # Aplicar límite si se especifica
        return errors[-limit:] if limit else errors
```

### Flujo de Procesamiento con Logging Completo
```
Paquete llega → Procesar en tick()
    ↓
1. Lookup en Trie de políticas
   → Si bloqueado: Log "PolicyViolation" + descartar
    ↓
2. Si pasa: Lookup en tabla AVL
   → Si no hay ruta: Log "NoRouteToHost" + descartar
    ↓
3. Si hay ruta: Validar con tabla ARP
   → Si ARP miss: Aprender interfaz
    ↓
4. Enviar paquete: Decrementar TTL
   → Si TTL ≤ 0: Log "TTLExpired" + descartar
    ↓
5. Comando ejecutado: Registrar errores de sintaxis/permisos
```

### Ejemplo de Uso Completo
```
Router1# policy set 192.168.1.0 255.255.255.0 block
Política establecida

Router1# ping 192.168.1.10
Error: No hay ruta disponible

Router1# show error-log
[2025-01-15 10:30:15] WARNING - PolicyViolation: Paquete bloqueado por política en prefijo 192.168.1.0/24 | Command: packet from 192.168.1.1 to 192.168.1.10
[2025-01-15 10:30:15] ERROR - NoRouteToHost: No hay ruta disponible para 192.168.1.10 | Command: packet from 192.168.1.1

Router1# show error-log 1
[2025-01-15 10:30:15] ERROR - NoRouteToHost: No hay ruta disponible para 192.168.1.10 | Command: packet from 192.168.1.1
```

### Estructura de Archivos
```
proyecto2algoritmos/
├── utils/
│   └── error_logger.py     # Implementación completa del logger
└── network/
    └── device.py           # Integración en process_queues()
```

### Ventajas del Diseño
- ✅ **Tiempo real**: Errores se registran inmediatamente cuando ocurren
- ✅ **Orden cronológico**: Cola FIFO garantiza orden de llegada
- ✅ **Consulta eficiente**: Búsqueda rápida con límite opcional
- ✅ **Información completa**: Timestamp, tipo, severidad y contexto
- ✅ **Integración completa**: Funciona en todo el flujo de procesamiento
- ✅ **Límite de memoria**: Previene consumo excesivo de recursos

---

**Desarrollado con ❤️ para el aprendizaje de algoritmos y redes de computadoras**
