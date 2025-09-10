#!/usr/bin/env python3
"""Prueba simple de estructuras"""

print("Importando estructuras...")
from data_structures import LinkedList, Queue, Stack

print("Probando LinkedList...")
ll = LinkedList()
ll.append("A")
ll.append("B")
print(f"LinkedList: {ll}")

print("Probando Queue...")
q = Queue()
q.enqueue("1")
q.enqueue("2")
print(f"Queue: {q}")

print("Probando Stack...")
s = Stack()
s.push("X")
s.push("Y")
print(f"Stack: {s}")

print("Pruebas simples completadas!")
