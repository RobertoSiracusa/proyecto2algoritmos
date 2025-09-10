# Explicación Detallada de las Estructuras de Datos

Este documento explica las estructuras de datos implementadas desde cero en el simulador de red LAN, con énfasis en las decisiones de diseño y complejidades algorítmicas.

## 📊 Estructuras Básicas

### Lista Enlazada (LinkedList)

**Implementación**: Lista simplemente enlazada con nodos que contienen `data` y `next`.

**Complejidad**:
- Inserción al inicio/fin: O(1)
- Inserción en posición específica: O(n)
- Búsqueda: O(n)
- Eliminación: O(n)

**Uso en el simulador**:
- Almacenamiento de vecinos de cada interfaz
- Lista de conexiones en la red
- Historial de errores (aunque para esto sería mejor una cola)

**Ventajas**:
- Inserción/eliminación eficiente en extremos
- Memoria dinámica
- Fácil implementación

### Cola (Queue)

**Implementación**: Cola FIFO usando lista enlazada internamente.

**Complejidad**:
- Enqueue (insertar): O(1)
- Dequeue (extraer): O(1)
- Peek: O(1)
- Size: O(1)

**Uso en el simulador**:
- Cola de paquetes entrantes de cada interfaz
- Cola de paquetes salientes de cada dispositivo
- Sistema de logging de errores (cola de errores por orden de llegada)

**Ventajas**:
- Operaciones O(1) eficientes
- Gestión automática de memoria
- Ideal para procesamiento de paquetes en orden

### Pila (Stack)

**Implementación**: Pila LIFO usando lista enlazada.

**Complejidad**:
- Push: O(1)
- Pop: O(1)
- Peek: O(1)
- Size: O(1)

**Uso en el simulador**:
- Historial de paquetes recibidos por dispositivo
- Seguimiento de modos en la CLI (aunque no implementado así)

**Ventajas**:
- Último en entrar, primero en salir
- Eficiente para acceso LIFO
- Memoria dinámica

## 🌳 Estructuras Avanzadas

### Árbol AVL (AVLTree)

**Implementación**: Árbol binario de búsqueda balanceado que mantiene altura O(log n).

**Propiedades**:
- Balance factor: |altura(izq) - altura(der)| ≤ 1
- Rotaciones: LL, LR, RL, RR para mantener balance
- Altura máxima: ≈ 1.44 log₂(n+2)

**Complejidad**:
- Inserción: O(log n)
- Búsqueda: O(log n)
- Eliminación: O(log n)
- Balance: O(1) por rotación

**Uso en el simulador**:
- Tabla de rutas de cada router
- Índice por prefijo IP + máscara + métrica
- Búsqueda de rutas más específicas (longest prefix match aproximado)

**Ventajas**:
- Garantiza O(log n) en todas las operaciones
- Balance automático
- Eficiente para búsquedas frecuentes

**Rotaciones implementadas**:
- **LL**: Rotación simple derecha
- **LR**: Rotación doble (izquierda-derecha)
- **RL**: Rotación doble (derecha-izquierda)
- **RR**: Rotación simple izquierda

### B-Tree (BTree)

**Implementación**: Árbol balanceado de orden variable optimizado para disco.

**Propiedades**:
- Orden (t): Número máximo de hijos por nodo
- Nodo interno: Entre t-1 y 2t-1 claves
- Nodo hoja: Entre t-1 y 2t-1 claves
- Altura: O(log_t n)

**Complejidad**:
- Inserción: O(t log_t n)
- Búsqueda: O(t log_t n)
- Eliminación: O(t log_t n)
- Split/Merge: O(t)

**Uso en el simulador**:
- Índice persistente de snapshots de configuración
- Búsqueda por nombre de snapshot o timestamp
- Almacenamiento eficiente en disco

**Ventajas**:
- Optimizado para acceso a disco
- Mantiene balance con bajo número de operaciones
- Eficiente para grandes volúmenes de datos

**Operaciones implementadas**:
- Split: Divide nodos cuando se llenan
- Merge: Fusiona nodos cuando quedan vacíos
- Borrow: Toma prestado de hermanos para evitar fusiones

### Trie N-ario (Trie)

**Implementación**: Árbol de prefijos para direcciones IP con nodos que representan octetos.

**Propiedades**:
- Nodo raíz: Representa prefijo vacío
- Nodos internos: Representan octetos (0-255)
- Nodos hoja: Contienen políticas completas
- Herencia: Políticas se aplican a subprefijos

**Complejidad**:
- Inserción: O(longitud_prefijo)
- Búsqueda exacta: O(longitud_prefijo)
- Longest prefix match: O(longitud_prefijo)
- Eliminación: O(longitud_prefijo)

**Uso en el simulador**:
- Políticas de red por prefijos IP
- Longest prefix match para enrutamiento
- Herencia de políticas (ej: bloqueo de rangos)

**Ventajas**:
- Muy eficiente para longest prefix match
- Memoria compartida entre prefijos
- Soporte natural para jerarquías

**Características especiales**:
- Políticas heredadas por subprefijos
- Soporte para múltiples tipos de política (block, ttl-min, etc.)
- Visualización jerárquica del árbol

## 🔄 Algoritmos de Balance

### AVL - Rotaciones

```python
def rotate_right(y):
    x = y.left
    T2 = x.right
    x.right = y
    y.left = T2
    # Actualizar alturas
    return x

def rotate_left_right(node):
    node.left = rotate_left(node.left)
    return rotate_right(node)
```

### B-Tree - Split y Merge

```python
def split_child(parent, child_index):
    child = parent.children[child_index]
    mid_key = child.keys[order // 2]
    # Crear nuevo nodo
    # Mover claves y hijos
    # Actualizar punteros padre
```

## 📈 Complejidades Comparadas

| Operación | LinkedList | AVL Tree | B-Tree | Trie |
|-----------|------------|----------|--------|------|
| Inserción | O(n) | O(log n) | O(log n) | O(L) |
| Búsqueda | O(n) | O(log n) | O(log n) | O(L) |
| Eliminación | O(n) | O(log n) | O(log n) | O(L) |
| Memoria | O(n) | O(n) | O(n) | O(n) |

Donde:
- L = longitud del prefijo (máximo 32 para IPv4)
- n = número de elementos

## 🎯 Decisiones de Diseño

### Elección de Estructuras

1. **AVL para rutas**: Garantiza O(log n) y es simple de implementar
2. **B-Tree para índices**: Optimizado para persistencia y búsquedas por clave
3. **Trie para prefijos**: Ideal para longest prefix match y jerarquías
4. **Queue para paquetes**: FIFO natural para procesamiento de red
5. **Stack para historial**: LIFO para acceso al último paquete recibido

### Optimizaciones Implementadas

1. **Lazy deletion en Trie**: Solo elimina nodos cuando quedan vacíos
2. **Contadores de rotaciones**: Para análisis de rendimiento
3. **Herencia de políticas**: Aplicación automática a subprefijos
4. **Balance automático**: Mantenimiento transparente del balance
5. **Memoria compartida**: En Trie para prefijos comunes

### Limitaciones

1. **Trie**: Solo IPv4 (podría extenderse a IPv6)
2. **B-Tree**: Orden fijo (podría ser dinámico)
3. **AVL**: No optimizado para disco (uso B-Tree en su lugar)
4. **LinkedList**: Búsqueda O(n) (aceptable para pequeños datasets)

## 🧪 Casos de Prueba Importantes

### AVL Tree
- Inserción que causa rotaciones dobles
- Eliminación del nodo raíz
- Búsqueda en árbol vacío
- Balance después de múltiples inserciones

### B-Tree
- Split en raíz
- Merge de nodos hermanos
- Inserción en orden inverso
- Eliminación masiva

### Trie
- Prefijos anidados
- Políticas heredadas
- Longest prefix match con múltiples candidatos
- Eliminación de prefijos intermedios

Este diseño proporciona un balance óptimo entre simplicidad, eficiencia y funcionalidad para el simulador de red.
