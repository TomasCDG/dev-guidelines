# Task 1, subtask 2 — Filtros por estado y por texto (REPORT PARCIAL)

**Fecha:** 2026-03-04
**Rama / repos:** `feat/listado-tareas` en `@back`; cambios sin commitear
**Brief:** [subtask-2-filtros.md](../../tasks/task-1-listado-tareas/subtask-2-filtros.md)

> Report parcial: la subtask sigue `en curso`. Lo lee la sesión siguiente (playbook `start-session` §2, punto 5) para saber dónde quedó el trabajo.

## Contenido

1. [Hecho hasta ahora](#1-hecho-hasta-ahora)
2. [Falta](#2-falta)
3. [Siguiente paso](#3-siguiente-paso)

## 1. Hecho hasta ahora

| Tipo | Archivo (con alias) | Cambio |
|---|---|---|
| Cambiado | `@back/src/pendientes/main.py` | `GET /tasks` acepta `status` (`pending`/`done`); un valor desconocido devuelve 422. |
| Cambiado | `@back/src/pendientes/repository.py` | El filtro por estado se aplica en la consulta SQL. |
| Cambiado | `@back/tests/test_tasks.py` | Pruebas del filtro por estado. |

Verificación: pruebas del filtro por estado pasan; sin parámetros el resultado es idéntico (C3).

## 2. Falta

- Parámetro `q` (texto, sin distinguir mayúsculas, T1-D3).
- Combinar `status` y `q`.
- Actualizar `docs/contracts/api-tareas.md`.
- Pregunta abierta con valor por defecto: ¿se ignoran los acentos? Por defecto, no.

## 3. Siguiente paso

Implementar `q` en `repository.py`, ampliar las pruebas y cerrar la subtask con la lista de `close-session` §1.
