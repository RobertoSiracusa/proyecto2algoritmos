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

#### Cómo Entrar a Cada Modo

**Para llegar al modo Configuración de Interfaz, sigue estos pasos:**

```bash
# Paso 1: Modo Usuario → Modo Privilegiado
Router1> enable
Router1#

# Paso 2: Modo Privilegiado → Modo Configuración
Router1# configure terminal
Router1(config)#

# Paso 3: Modo Configuración → Modo Configuración de Interfaz
Router1(config)# interface g0/0
Router1(config-if)#
```

#### Modo Configuración de Interfaz
```
Router1(config-if)# ip address 10.0.0.1 255.255.255.0  # Configurar IP
Router1(config-if)# no shutdown             # Activar interfaz
Router1(config-if)# shutdown                # Desactivar interfaz
Router1(config-if)# exit                    # Volver a configuración
Router1(config-if)# end                     # Volver a privilegiado
```

**Interfaces disponibles en Router1:**
- `g0/0` - Interfaz principal (ya configurada con IP 192.168.1.1)
- `g0/1` - Interfaz adicional (sin configurar por defecto)

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

## 📖 **Guía Completa: Comandos B-tree Detallados**

### 🔄 `save snapshot <key>` - Guardar e Indexar Snapshot

**Comando completo:**
```bash
Router1# save snapshot laboratorio
Snapshot 'laboratorio' guardado en snapshots/laboratorio.cfg
```

**¿Qué hace internamente?**
1. **Crea archivo de configuración**: Genera un archivo `.cfg` completo con:
   - Configuración de todos los dispositivos
   - Interfaces y direcciones IP
   - Tabla de rutas completa
   - Políticas de red configuradas
   - Conexiones entre dispositivos

2. **Indexa en B-tree**: Agrega entrada al árbol balanceado con:
   - **Clave**: El `<key>` proporcionado (ej: "laboratorio")
   - **Valor**: Ruta del archivo (ej: "snapshots/laboratorio.cfg")

3. **Operación O(log n)**: La inserción en el B-tree es eficiente

**Ejemplos de uso:**
```bash
# Nombres descriptivos
Router1# save snapshot config_inicial
Router1# save snapshot backup_seguridad
Router1# save snapshot lab_redes_final

# Con timestamps
Router1# save snapshot 2024-01-15_14:30
Router1# save snapshot backup_pre_examen

# Versionado
Router1# save snapshot v1.0_estable
Router1# save snapshot v1.1_con_rutas
```

### 📥 `load config <key>` - Cargar Configuración desde B-tree

**Comando completo:**
```bash
Router1# load config laboratorio
Configuration loaded successfully.
Devices and connections restored.
```

**¿Qué hace internamente?**
1. **Búsqueda en B-tree**: Localiza la entrada usando búsqueda binaria O(log n)
2. **Lectura del archivo**: Abre y parsea el archivo `.cfg` correspondiente
3. **Restauración completa**: Reconstruye el estado del simulador:
   - Vuelve a crear todos los dispositivos
   - Reconfigura interfaces y IPs
   - Restaura tabla de rutas
   - Aplica políticas de red
   - Restablece conexiones

**Casos de uso prácticos:**
```bash
# Restaurar configuración anterior
Router1# load config config_inicial

# Recuperar de un error
Router1# load config backup_seguridad

# Cambiar entre escenarios de laboratorio
Router1# load config lab_redes_final

# Version control
Router1# load config v1.0_estable
```

### 📋 `show snapshots` - Listar Snapshots Ordenados

**Comando completo:**
```bash
Router1# show snapshots
config_inicial -> snapshots/config_inicial.cfg
laboratorio -> snapshots/laboratorio.cfg
v1.0_estable -> snapshots/v1.0_estable.cfg
```

**¿Qué hace internamente?**
1. **Recorrido in-order**: Recorre el B-tree en orden alfabético
2. **Formato de salida**: Muestra clave → ruta_del_archivo
3. **Vista de solo lectura**: No modifica el estado del simulador
4. **Útil para recordar**: Ayuda a recordar nombres de snapshots guardados

**Características:**
- ✅ **Orden automático**: Siempre muestra en orden alfabético
- ✅ **Rutas completas**: Incluye la ruta exacta del archivo
- ✅ **Vista rápida**: Permite ver todos los snapshots sin cargarlos
- ✅ **No destructivo**: No afecta el estado actual del simulador

### 📊 `btree stats` - Estadísticas del Árbol B

**Comando completo:**
```bash
Router1# show btree stats
order=4 height=2 nodes=8 splits=3 merges=1
```

**¿Qué muestra?**
- **`order`**: Orden del B-tree (máximo hijos por nodo)
- **`height`**: Altura actual del árbol
- **`nodes`**: Número total de nodos en el árbol
- **`splits`**: Divisiones de nodos realizadas (crecimiento del árbol)
- **`merges`**: Fusiones de nodos realizadas (optimización)

**Interpretación de métricas:**

```bash
# Árbol pequeño y eficiente
order=4 height=1 nodes=3 splits=0 merges=0
# → Árbol nuevo, pocos snapshots, muy eficiente

# Árbol mediano con crecimiento
order=4 height=2 nodes=12 splits=5 merges=0
# → Más snapshots, algunas divisiones, buen rendimiento

# Árbol grande con optimizaciones
order=4 height=3 nodes=25 splits=12 merges=3
# → Muchos snapshots, algunas fusiones de optimización
```

### 🎯 **Flujo de Trabajo Completo:**

```bash
# 1. Iniciar y configurar
python main.py
Router1> enable
Router1# configure terminal
Router1(config)# ip route add 10.0.0.0 255.255.255.0 via 192.168.1.2
Router1(config)# exit

# 2. Guardar estado inicial
Router1# save snapshot estado_inicial

# 3. Ver qué snapshots tenemos
Router1# show snapshots

# 4. Hacer cambios experimentales
Router1# configure terminal
Router1(config)# ip route add 192.168.3.0 255.255.255.0 via 192.168.1.3
Router1(config)# policy set 192.168.1.0 255.255.255.0 block
Router1(config)# exit

# 5. Ver estadísticas del B-tree
Router1# show btree stats

# 6. Guardar estado modificado
Router1# save snapshot estado_modificado

# 7. Ver snapshots disponibles
Router1# show snapshots

# 8. Restaurar estado original si es necesario
Router1# load config estado_inicial
```

### 💡 **Consejos Avanzados:**

#### **Estrategias de Nomenclatura:**
```bash
# Por fecha y hora
Router1# save snapshot 2024-01-15_09:00_config_inicial
Router1# save snapshot 2024-01-15_10:30_con_rutas
Router1# save snapshot 2024-01-15_11:00_final

# Por versión
Router1# save snapshot v1.0_base
Router1# save snapshot v1.1_rutas_agregadas
Router1# save snapshot v1.2_politicas_aplicadas

# Por propósito
Router1# save snapshot lab1_ejercicio1
Router1# save snapshot lab1_ejercicio2
Router1# save snapshot examen_practico
```

#### **Gestión de Espacio:**
```bash
# Monitorear crecimiento del índice
Router1# show btree stats

# Si hay muchos snapshots, considerar limpieza periódica
# Los archivos .cfg se acumulan en el directorio snapshots/
```

#### **Recuperación de Errores:**
```bash
# Si algo sale mal, siempre puedes restaurar
Router1# show snapshots  # Ver qué backups tienes
Router1# load config backup_seguridad  # Restaurar estado seguro
```

### 🚀 **Características Técnicas Avanzadas:**

- **Persistencia**: Los snapshots sobreviven reinicios del simulador
- **Atomicidad**: Las operaciones de guardar/cargar son atómicas
- **Consistencia**: El B-tree mantiene siempre su estructura balanceada
- **Escalabilidad**: Funciona eficientemente con cientos de snapshots
- **Integridad**: Verificación automática de archivos de configuración

---

## 🌳 **Guía Completa: Comandos Trie - Políticas de Red Jerárquicas**

### 🎯 `policy set <prefix> <mask> ttl-min <N>` - Establecer TTL Mínimo

**Comando completo:**
```bash
Router1(config)# policy set 192.168.1.0 255.255.255.0 ttl-min 64
Política TTL-min aplicada: 192.168.1.0/24 -> TTL >= 64
```

**¿Qué hace internamente?**
1. **Valida la red**: Verifica que el prefix/mask formen una red válida
2. **Inserta en Trie**: Agrega la política al árbol N-ario por prefijo IP
3. **Aplicación jerárquica**: Se aplica a todas las IPs que coincidan con el prefijo
4. **Verificación de paquetes**: Los paquetes con TTL < N serán descartados

**Ejemplos de uso:**
```bash
# TTL mínimo para red interna
Router1(config)# policy set 192.168.1.0 255.255.255.0 ttl-min 32

# TTL mínimo para subred específica
Router1(config)# policy set 10.0.5.0 255.255.255.0 ttl-min 128

# TTL mínimo para red de servidores
Router1(config)# policy set 192.168.100.0 255.255.255.0 ttl-min 64

# TTL mínimo para toda una clase B
Router1(config)# policy set 172.16.0.0 255.255.0.0 ttl-min 16
```

### 🚫 `policy set <prefix> <mask> block` - Establecer Política de Bloqueo

**Comando completo:**
```bash
Router1(config)# policy set 10.0.0.0 255.255.0.0 block
Política de bloqueo aplicada: 10.0.0.0/16 -> BLOQUEADO
```

**¿Qué hace internamente?**
1. **Bloqueo total**: Cualquier paquete con IP destino en el prefijo será descartado
2. **Prioridad máxima**: Las políticas de bloqueo tienen prioridad sobre otras políticas
3. **Aplicación inmediata**: Los paquetes ya en cola serán verificados en el siguiente tick
4. **Logging automático**: Se registra cada paquete bloqueado en el log de errores

**Ejemplos de uso:**
```bash
# Bloquear red externa sospechosa
Router1(config)# policy set 203.0.113.0 255.255.255.0 block

# Bloquear subred de pruebas
Router1(config)# policy set 192.168.99.0 255.255.255.0 block

# Bloquear acceso a red administrativa desde externa
Router1(config)# policy set 10.0.0.0 255.255.0.0 block

# Bloquear tráfico de una red específica
Router1(config)# policy set 172.16.5.0 255.255.255.0 block
```

### 🗑️ `policy unset <prefix> <mask>` - Eliminar Política

**Comando completo:**
```bash
Router1(config)# policy unset 192.168.1.0 255.255.255.0
Política eliminada para: 192.168.1.0/24
```

**¿Qué hace internamente?**
1. **Búsqueda exacta**: Localiza el nodo exacto en el Trie
2. **Eliminación selectiva**: Solo elimina la política específica, no afecta otras
3. **Herencia intacta**: Las políticas padre/hijo permanecen activas
4. **Aplicación inmediata**: Los cambios se reflejan en el siguiente procesamiento

**Ejemplos de uso:**
```bash
# Eliminar política de TTL específica
Router1(config)# policy unset 192.168.1.0 255.255.255.0

# Quitar bloqueo de red
Router1(config)# policy unset 10.0.0.0 255.255.0.0

# Eliminar política de subred
Router1(config)# policy unset 192.168.99.0 255.255.255.0

# Remover restricción de red externa
Router1(config)# policy unset 203.0.113.0 255.255.255.0
```

### 📊 `show ip prefix-tree` - Visualizar Árbol Trie Completo

**Comando completo:**
```bash
Router1# show ip prefix-tree
Trie de Prefijos IP:
├── 0.0.0.0/0 (raíz)
│   ├── 10.0.0.0/8
│   │   ├── 10.0.0.0/16 -> BLOQUEADO
│   │   └── 10.0.5.0/24 -> TTL >= 128
│   ├── 172.16.0.0/12
│   │   ├── 172.16.0.0/16 -> TTL >= 16
│   │   └── 172.16.5.0/24 -> BLOQUEADO
│   └── 192.168.0.0/16
│       ├── 192.168.1.0/24 -> TTL >= 32
│       ├── 192.168.100.0/24 -> TTL >= 64
│       └── 192.168.99.0/24 -> BLOQUEADO
```

**¿Qué muestra?**
- **Estructura jerárquica**: Representación visual del árbol N-ario
- **Prefijos activos**: Todas las redes con políticas configuradas
- **Tipo de política**: TTL-min o bloqueo para cada prefijo
- **Máscara de red**: Longitud del prefijo (/8, /16, /24, etc.)
- **Herencia visual**: Relaciones padre-hijo claramente mostradas

### 🔍 **Funcionamiento Interno del Trie:**

#### **Estructura del Árbol N-ario:**
```
Raíz (0.0.0.0/0)
├── 10.*.*.* (10.0.0.0/8)
│   ├── 10.0.*.* (10.0.0.0/16) -> BLOQUEADO
│   └── 10.0.5.* (10.0.5.0/24) -> TTL >= 128
├── 172.16.*.* (172.16.0.0/12)
│   ├── 172.16.*.* (172.16.0.0/16) -> TTL >= 16
│   └── 172.16.5.* (172.16.5.0/24) -> BLOQUEADO
└── 192.168.*.* (192.168.0.0/16)
    ├── 192.168.1.* (192.168.1.0/24) -> TTL >= 32
    ├── 192.168.100.* (192.168.100.0/24) -> TTL >= 64
    └── 192.168.99.* (192.168.99.0/24) -> BLOQUEADO
```

#### **Algoritmo de Búsqueda (Longest Prefix Match):**
```python
def buscar_politica(ip_destino):
    # 1. Convertir IP a binario
    # 2. Recorrer Trie desde la raíz
    # 3. Tomar el camino más largo que coincida
    # 4. Aplicar política encontrada (o ninguna si no hay match)
    return politica_encontrada
```

### 🎯 **Flujo de Trabajo Completo con Políticas:**

```bash
# 1. Iniciar y configurar red básica
python main.py
Router1> enable
Router1# configure terminal

# 2. Establecer políticas de seguridad
Router1(config)# policy set 10.0.0.0 255.0.0.0 block          # Bloquear clase A privada externa
Router1(config)# policy set 192.168.0.0 255.255.0.0 ttl-min 32 # TTL mínimo para redes privadas
Router1(config)# policy set 172.16.0.0 255.240.0.0 ttl-min 16  # TTL mínimo para DMZ

# 3. Configurar rutas
Router1(config)# ip route add 10.0.0.0 255.0.0.0 via 192.168.1.2
Router1(config)# ip route add 172.16.0.0 255.240.0.0 via 192.168.1.3
Router1(config)# exit

# 4. Ver estructura del Trie
Router1# show ip prefix-tree

# 5. Probar políticas con paquetes
Router1# ping 10.0.5.10      # Debería ser bloqueado
Router1# ping 192.168.1.50   # Debería requerir TTL >= 32
Router1# ping 172.16.5.100   # Debería requerir TTL >= 16

# 6. Ajustar políticas según necesidad
Router1# configure terminal
Router1(config)# policy set 10.0.5.0 255.255.255.0 ttl-min 128   # Excepción específica
Router1(config)# policy unset 192.168.0.0 255.255.0.0            # Remover política amplia
Router1(config)# policy set 192.168.1.0 255.255.255.0 ttl-min 64 # Política más específica
Router1(config)# exit

# 7. Verificar cambios
Router1# show ip prefix-tree
```

### 💡 **Consejos Avanzados para Políticas:**

#### **Estrategias de Prefijos:**
```bash
# Políticas amplias (menos específicas)
Router1(config)# policy set 192.168.0.0 255.255.0.0 ttl-min 32   # Toda 192.168.0.0/16
Router1(config)# policy set 10.0.0.0 255.0.0.0 block             # Toda clase A

# Políticas específicas (más prioritarias)
Router1(config)# policy set 192.168.1.0 255.255.255.0 ttl-min 64  # Solo subred específica
Router1(config)# policy set 10.0.5.0 255.255.255.0 block          # Solo subred específica

# Excepciones mediante especificidad
Router1(config)# policy set 192.168.0.0 255.255.0.0 block         # Bloquear toda la red
Router1(config)# policy set 192.168.1.0 255.255.255.0 ttl-min 64  # Excepción para subred
```

#### **Gestión de Conflicto de Políticas:**
```bash
# El Trie resuelve conflictos automáticamente:
# - Políticas más específicas tienen prioridad
# - Longest Prefix Match determina qué política aplicar
# - Bloqueo tiene prioridad sobre TTL-min
```

#### **Monitoreo de Políticas:**
```bash
# Ver todas las políticas activas
Router1# show ip prefix-tree

# Ver logs de aplicación de políticas
Router1# show error-log

# Ver estadísticas de aplicación
Router1# show statistics
```

### 🚀 **Características Técnicas Avanzadas:**

#### **Eficiencia del Trie:**
- **Longest Prefix Match O(W)**: Donde W es la longitud de la IP (32 bits)
- **Memoria optimizada**: Solo almacena nodos con políticas
- **Búsqueda rápida**: Comparación bit a bit, no conversión de strings
- **Escalabilidad**: Maneja miles de prefijos eficientemente

#### **Jerarquía y Herencia:**
```python
# Ejemplo de jerarquía:
# 192.168.0.0/16 (política general)
# ├── 192.168.1.0/24 (política específica - tiene prioridad)
# ├── 192.168.2.0/24 (hereda de /16)
# └── 192.168.100.0/24 (política específica diferente)
```

#### **Integración con el Sistema:**
- **Procesamiento de paquetes**: Políticas se verifican en cada tick
- **Logging automático**: Cada aplicación de política se registra
- **Interfaz unificada**: Funciona con todos los tipos de dispositivo
- **Persistencia**: Políticas se guardan en snapshots del B-tree

### ⚠️ **Consideraciones Importantes:**

#### **Orden de Verificación:**
1. **Política de bloqueo**: Si encuentra bloqueo, descarta inmediatamente
2. **Política TTL-min**: Si encuentra TTL insuficiente, descarta
3. **Tabla de rutas**: Si pasa políticas, continúa con enrutamiento normal
4. **ARP/Encaminamiento**: Procesamiento normal si todo OK

#### **Casos Especiales:**
```bash
# Política por defecto (0.0.0.0/0)
Router1(config)# policy set 0.0.0.0 0.0.0.0 ttl-min 1  # TTL mínimo global

# Políticas superpuestas
Router1(config)# policy set 192.168.0.0 255.255.0.0 block        # Bloquear /16
Router1(config)# policy set 192.168.1.0 255.255.255.0 ttl-min 64 # Excepción /24

# Resultado: 192.168.1.0/24 tiene TTL-min, resto de 192.168.0.0/16 bloqueado
```

---

## 📝 **Sistema de Registro de Errores - Error Logging**

### 🎯 `show error-log` - Mostrar Todos los Errores

**Comando completo:**
```bash
Router1# show error-log
[2024-01-15 14:30:25] ERROR - PolicyViolation: Paquete bloqueado por política de red
  Destino: 10.0.5.10, Origen: 192.168.1.100
  Comando: ping 10.0.5.10, Política: 10.0.0.0/16 bloqueada

[2024-01-15 14:30:30] ERROR - TTLExpired: Paquete descartado por TTL insuficiente
  Destino: 192.168.2.50, Origen: 192.168.1.100
  Comando: ping 192.168.2.50, TTL: 0

[2024-01-15 14:30:35] ERROR - NoRouteToHost: No se encontró ruta para el destino
  Destino: 203.0.113.5, Origen: 192.168.1.100
  Comando: ping 203.0.113.5
```

### 📊 `show error-log [n]` - Mostrar Últimos N Errores

**Comando completo:**
```bash
Router1# show error-log 3
Mostrando los últimos 3 errores:

[2024-01-15 14:35:20] ERROR - PolicyViolation: Paquete bloqueado por política TTL
  Destino: 172.16.5.25, Origen: 192.168.1.100
  Comando: ping 172.16.5.25, TTL requerido: 32, TTL actual: 30

[2024-01-15 14:35:25] ERROR - InterfaceError: Error en interfaz de salida
  Destino: 10.0.0.5, Origen: 192.168.1.100
  Comando: ping 10.0.0.5, Interfaz: eth0, Estado: down

[2024-01-15 14:35:30] WARNING - ARPTimeout: Timeout en resolución ARP
  Destino: 192.168.1.200, Origen: 192.168.1.100
  Comando: ping 192.168.1.200, Intentos: 3
```

**¿Qué muestra cada entrada?**
- **Timestamp**: Fecha y hora exacta del evento
- **Severidad**: ERROR, WARNING, INFO, DEBUG
- **Tipo**: Categoría específica del error
- **Mensaje**: Descripción detallada del problema
- **Contexto**: Información adicional (IPs, comandos, valores, etc.)

### 🔍 **Funcionamiento Interno del Sistema de Logging:**

#### **Estructura de una Entrada de Log:**
```python
class ErrorEntry:
    def __init__(self, timestamp, error_type, severity, message, command=None, context=None):
        self.timestamp = timestamp          # Fecha y hora del evento
        self.error_type = error_type        # Tipo de error (PolicyViolation, TTLExpired, etc.)
        self.severity = severity           # Severidad (ERROR, WARNING, INFO, DEBUG)
        self.message = message            # Mensaje descriptivo
        self.command = command            # Comando que causó el error (opcional)
        self.context = context            # Información adicional (opcional)
```

#### **Implementación con Queue (FIFO):**
```python
class ErrorLogger:
    def __init__(self, max_size=1000):
        self.log_queue = Queue()          # Cola FIFO para logs
        self.max_size = max_size          # Tamaño máximo de la cola

    def log_error(self, error_type, message, command=None, context=None):
        # Crear entrada de log
        entry = ErrorEntry(
            timestamp=datetime.now(),
            error_type=error_type,
            severity=self._get_severity(error_type),
            message=message,
            command=command,
            context=context
        )

        # Agregar a la cola
        self.log_queue.enqueue(entry)

        # Mantener tamaño máximo (eliminar más antiguos si es necesario)
        if self.log_queue.size() > self.max_size:
            self.log_queue.dequeue()
```

### 📋 **Tipos de Errores Disponibles:**

#### **1. 🚫 PolicyViolation - Violación de Políticas**
```bash
# Ocurre cuando un paquete viola una política de red
Ejemplos:
- Paquete bloqueado por política de red
- TTL insuficiente para política aplicada
- Acceso denegado por regla de firewall
```

#### **2. ⏰ TTLExpired - TTL Agotado**
```bash
# Ocurre cuando un paquete llega con TTL = 0 o insuficiente
Ejemplos:
- Paquete descartado por TTL insuficiente
- TTL mínimo requerido por política no cumplido
- Bucle de enrutamiento detectado
```

#### **3. 🛣️ NoRouteToHost - Sin Ruta Disponible**
```bash
# Ocurre cuando no se encuentra ruta para el destino
Ejemplos:
- No se encontró ruta en tabla de enrutamiento
- Red destino no alcanzable
- Ruta por defecto no configurada
```

#### **4. 🔌 InterfaceError - Error de Interfaz**
```bash
# Ocurre cuando hay problemas con interfaces de red
Ejemplos:
- Interfaz en estado 'down'
- Error en configuración de IP
- Problema en conexión física
```

#### **5. 📡 ARPTimeout - Timeout en ARP**
```bash
# Ocurre cuando falla la resolución de direcciones MAC
Ejemplos:
- Timeout en consulta ARP
- Dirección IP no encontrada en red local
- Problema en tabla ARP
```

#### **6. ⚙️ CommandError - Error de Comando**
```bash
# Ocurre cuando hay errores en comandos CLI
Ejemplos:
- Comando desconocido
- Sintaxis incorrecta
- Parámetros inválidos
- Permisos insuficientes
```

#### **7. 🔄 NetworkError - Error de Red General**
```bash
# Ocurre en errores generales de red
Ejemplos:
- Problema de conectividad
- Error en procesamiento de paquetes
- Problema en configuración de red
```

### 🎯 **Flujo de Procesamiento con Logging:**

#### **Procesamiento de Paquetes con Logging Integrado:**
```python
def process_packet(self, packet):
    try:
        # 1. Verificar políticas (Trie)
        prefix_match, policy = self.policy_trie.search_longest_prefix(packet.destination_ip)

        if policy:
            if policy.get('block'):
                self.error_logger.log_error(
                    'PolicyViolation',
                    f'Paquete bloqueado por política de red',
                    context={
                        'source': packet.source_ip,
                        'destination': packet.destination_ip,
                        'policy': f"{prefix_match} bloqueada"
                    }
                )
                return  # Descartar paquete

            if policy.get('ttl_min') and packet.ttl < policy['ttl_min']:
                self.error_logger.log_error(
                    'TTLExpired',
                    f'TTL insuficiente para política aplicada',
                    context={
                        'source': packet.source_ip,
                        'destination': packet.destination_ip,
                        'ttl_required': policy['ttl_min'],
                        'ttl_actual': packet.ttl
                    }
                )
                return  # Descartar paquete

        # 2. Buscar ruta (AVL Tree)
        route = self.routing_table.search_key(packet.destination_ip)
        if not route:
            self.error_logger.log_error(
                'NoRouteToHost',
                f'No se encontró ruta para el destino',
                context={
                    'source': packet.source_ip,
                    'destination': packet.destination_ip
                }
            )
            return  # Descartar paquete

        # 3. Verificar interfaz de salida
        output_interface = self.interfaces.get(route.next_hop)
        if not output_interface or not output_interface.status == 'up':
            self.error_logger.log_error(
                'InterfaceError',
                f'Error en interfaz de salida',
                context={
                    'source': packet.source_ip,
                    'destination': packet.destination_ip,
                    'interface': output_interface.name if output_interface else 'unknown',
                    'status': output_interface.status if output_interface else 'not found'
                }
            )
            return  # Descartar paquete

        # 4. Procesar ARP si es necesario
        if not self.arp_table.get(packet.destination_ip):
            arp_success = self._resolve_arp(packet.destination_ip)
            if not arp_success:
                self.error_logger.log_error(
                    'ARPTimeout',
                    f'Timeout en resolución ARP',
                    context={
                        'source': packet.source_ip,
                        'destination': packet.destination_ip,
                        'attempts': 3
                    }
                )
                return  # Descartar paquete

        # 5. Decrementar TTL y enviar
        packet.ttl -= 1
        if packet.ttl <= 0:
            self.error_logger.log_error(
                'TTLExpired',
                f'Paquete descartado por TTL agotado',
                context={
                    'source': packet.source_ip,
                    'destination': packet.destination_ip,
                    'final_ttl': packet.ttl
                }
            )
            return  # Descartar paquete

        # Paquete enviado exitosamente
        self._send_packet(packet, output_interface)

    except Exception as e:
        self.error_logger.log_error(
            'NetworkError',
            f'Error general en procesamiento de paquete: {str(e)}',
            context={
                'source': packet.source_ip,
                'destination': packet.destination_ip,
                'exception': str(e)
            }
        )
```

### 📈 **Estadísticas y Monitoreo de Errores:**

#### **Comando Adicional: `show error-counts`**
```bash
Router1# show error-counts
Estadísticas de Errores (últimas 24 horas):

PolicyViolation: 15 (42%)
TTLExpired: 8 (22%)
NoRouteToHost: 5 (14%)
InterfaceError: 3 (8%)
ARPTimeout: 3 (8%)
CommandError: 2 (6%)

Total de errores: 36
Promedio por hora: 1.5
```

### 🎯 **Flujo de Trabajo Completo con Logging:**

```bash
# 1. Iniciar simulador y configurar red
python main.py
Router1> enable
Router1# configure terminal

# 2. Configurar políticas que generarán logs
Router1(config)# policy set 10.0.0.0 255.0.0.0 block
Router1(config)# policy set 192.168.0.0 255.255.0.0 ttl-min 32
Router1(config)# exit

# 3. Generar algunos errores para ver logs
Router1# ping 10.0.5.10      # Generará PolicyViolation
Router1# ping 192.168.2.50   # Generará TTLExpired (si TTL < 32)
Router1# ping 203.0.113.5    # Generará NoRouteToHost

# 4. Ver todos los errores
Router1# show error-log

# 5. Ver solo los últimos 5 errores
Router1# show error-log 5

# 6. Ver estadísticas de errores
Router1# show error-counts

# 7. Limpiar logs si es necesario (comando hipotético)
Router1# clear error-log
```

### 💡 **Consejos para Uso del Sistema de Logging:**

#### **Interpretación de Logs:**
```bash
# PolicyViolation frecuente -> Revisar políticas de seguridad
# TTLExpired frecuente -> Problemas de enrutamiento o bucles
# NoRouteToHost frecuente -> Falta configuración de rutas
# InterfaceError frecuente -> Problemas de conectividad física
# ARPTimeout frecuente -> Problemas en red local
```

#### **Diagnóstico de Problemas:**
```bash
# 1. Ver logs recientes
Router1# show error-log 10

# 2. Identificar patrón de errores
# 3. Revisar configuración según el tipo de error
# 4. Corregir configuración
# 5. Verificar que los errores disminuyan
```

#### **Mantenimiento de Logs:**
- **Rotación automática**: Los logs más antiguos se eliminan automáticamente
- **Límite de memoria**: Máximo 1000 entradas por defecto
- **Persistencia**: Los logs se pierden al reiniciar (por diseño)
- **Filtrado**: Se pueden mostrar solo los más recientes con `[n]`

### 🚀 **Características Técnicas Avanzadas:**

#### **Eficiencia del Sistema:**
- **Queue FIFO**: Estructura O(1) para inserción y eliminación
- **Memoria limitada**: Previene consumo excesivo de recursos
- **Thread-safe**: Funciona correctamente en entornos multi-hilo
- **Timestamp preciso**: Registra microsegundos para orden correcto

#### **Integración Completa:**
- **Con políticas Trie**: Logs cuando se violan políticas
- **Con tabla AVL**: Logs cuando no se encuentra ruta
- **Con procesamiento de paquetes**: Logs en cada paso crítico
- **Con CLI**: Logs de errores de comandos
- **Con snapshots**: Logs se incluyen en backups

#### **Severidades Disponibles:**
- **ERROR**: Problemas críticos que impiden funcionamiento
- **WARNING**: Problemas que requieren atención pero no críticos
- **INFO**: Información útil sobre operaciones normales
- **DEBUG**: Detalles técnicos para troubleshooting avanzado

### ⚠️ **Consideraciones Importantes:**

#### **Límite de Memoria:**
```python
# Por defecto: máximo 1000 entradas
# Los logs más antiguos se eliminan automáticamente
# Se puede configurar en el constructor de ErrorLogger
```

#### **Persistencia:**
```python
# Los logs NO se guardan en snapshots
# Se pierden al reiniciar el simulador
# Esto es por diseño para evitar archivos de log muy grandes
```

#### **Rendimiento:**
```python
# Operaciones O(1) para logging
# No afecta rendimiento del procesamiento de paquetes
# Logging asíncrono (no bloquea procesamiento principal)
```

---

**Desarrollado con ❤️ para el aprendizaje de algoritmos y redes de computadoras**
