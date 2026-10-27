# Decisiones de la task 1 — Listar, crear y filtrar tareas

**Fecha:** 2026-03-04

## Contenido

1. [Decisiones](#1-decisiones)
2. [Restricciones de la task](#2-restricciones-de-la-task)

## 1. Decisiones

| ID | Decisión | Motivo | Fecha | Quién | Estado |
|---|---|---|---|---|---|
| T1-D1 | La API solo escucha en `127.0.0.1`. | No hay autenticación y los datos son personales. | 2026-03-01 | desarrollador | promovida a [ADR-001](../../../docs/decisions/ADR-001-solo-localhost.md) |
| T1-D2 | Los filtros se calculan en la API. | La UI no duplica lógica y los filtros se prueban en Python. | 2026-03-01 | desarrollador | vigente |
| T1-D3 | La búsqueda por texto no distingue mayúsculas. | Es lo habitual en un buscador simple. | 2026-03-04 | agente (valor por defecto) | vigente |
| T1-D4 | Las tareas se guardan en SQLite. | Un archivo, sin servidor; basta para uso personal. | 2026-03-02 | desarrollador | vigente |

## 2. Restricciones de la task

| ID | Restricción | Origen |
|---|---|---|
| T1-C1 | El filtrado se calcula en la API, no en el navegador. | T1-D2 |
