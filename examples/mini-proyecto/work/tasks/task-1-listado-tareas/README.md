# Task 1 — Listar, crear y filtrar tareas pendientes desde la web

**Fecha:** 2026-03-01
**Estado:** en curso (2026-03-04; subtask 1 hecha, subtask 2 en curso)
**Rama / repos:** `feat/listado-tareas` en `@back` y `@front`
**Origen:** solicitud del desarrollador, 2026-03-01.
**Tasks relacionadas:** ninguna

## Contenido

1. [Objetivo](#1-objetivo)
2. [Decisiones y restricciones](#2-decisiones-y-restricciones)
3. [Plan y dependencias](#3-plan-y-dependencias)
4. [Índice de subtasks](#4-índice-de-subtasks)
5. [Qué necesita del desarrollador](#5-qué-necesita-del-desarrollador)
6. [Backlog (no redactado)](#6-backlog-no-redactado)
7. [Entregables compartidos](#7-entregables-compartidos)

## 1. Objetivo

Hoy las tareas solo se manejan por línea de comandos. Al terminar, el usuario ve en el navegador la lista de tareas, puede crear una y filtrar por estado y por texto. La API en Python hace todo el cálculo; la UI solo dibuja.

## 2. Decisiones y restricciones

Decisiones de esta task: [decisions.md](./decisions.md). Decisiones de todo el proyecto: [ADR-001](../../../docs/decisions/ADR-001-solo-localhost.md).

| ID | Restricción | Origen |
|---|---|---|
| T1-C1 | El filtrado se calcula en la API, no en el navegador. | T1-D2 |
| C1 · C2 · C3 | Restricciones del proyecto ([PROJECT.md §3](../../../config/PROJECT.md#3-restricciones)). | Proyecto |

## 3. Plan y dependencias

```mermaid
flowchart TD
    s1["1 API de tareas con filtros (@back)"] --> s2["2 UI de la lista (@front)"]
```

**Figura 1.** Dependencias entre subtasks. Dos subtasks en serie; no hay paralelo.

1. La subtask 1 deja la API completa (crear, listar y filtrar); se demuestra con `curl`.
2. La subtask 2 construye la pantalla que consume esa API. Se separa porque `@front` se publica aparte de `@back` (D2) y el diseño visual lo aprueba el desarrollador (D3). Los filtros no se separan de la API: son el mismo repo y el mismo despliegue.

## 4. Índice de subtasks

Esfuerzo: S horas · M un día · L varios días.

| # | Subtask | Tipo | Resultado | Esfuerzo | Modelo sugerido | Depende de | Corte | Estado |
|---|---|---|---|---|---|---|---|---|
| 1 | [subtask-1-api](./subtask-1-api.md) | funcionalidad | `POST /tasks` y `GET /tasks` con filtros por estado y texto, en SQLite. | M | El más capaz | — | — | hecha (commit `a1b2c3d`) |
| 2 | [subtask-2-ui-lista](./subtask-2-ui-lista.md) | funcionalidad | Pantalla con lista, formulario y filtros. | M | Intermedio | 1 | D2, D3 | en curso |

## 5. Qué necesita del desarrollador

| Ítem | Necesario para | Valor por defecto del agente mientras tanto |
|---|---|---|
| ¿La búsqueda por texto distingue mayúsculas o acentos? | Subtask 1 (hecha con el valor por defecto) | No distingue mayúsculas (T1-D3); no ignora acentos. |
| Diseño visual de la lista | Subtask 2 | Tabla simple sin estilos especiales. |

## 6. Backlog (no redactado)

| Ítem | Nota |
|---|---|
| Etiquetas por tarea | No pedido en esta task. |
| Editar y borrar tareas | Fuera de alcance; la API solo crea y lista. |

## 7. Entregables compartidos

- Un report por subtask en `work/reports/task-1-listado-tareas/`.
- Docs técnicos actualizados en `docs/` en la misma subtask que cambia el comportamiento.
- Changelog en `work/changelogs/task-1-listado-tareas/` por cada subtask que cambia código funcional.
- Al cerrar la task: informe de PR y actualización de `INDEX.md`.
