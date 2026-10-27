# Changelog — Task 1, subtask 1: API para crear y listar tareas

**Fecha:** 2026-03-03
**Report:** [subtask-1-api-crud.md](../../reports/task-1-listado-tareas/subtask-1-api-crud.md)

## Contenido

1. [2026-03-03 — API para crear y listar tareas](#2026-03-03--api-para-crear-y-listar-tareas)

## 2026-03-03 — API para crear y listar tareas

**User story:** Como usuario, quiero crear tareas y ver mi lista, para no depender de la línea de comandos.
**Commit:** `a1b2c3d`

| Tipo | Archivo (con alias) | Cambio |
|---|---|---|
| Nuevo | `@back/src/pendientes/models.py` | Modelo `Task` y validación del título. |
| Nuevo | `@back/src/pendientes/repository.py` | Acceso a SQLite aislado de los endpoints. |
| Cambiado | `@back/src/pendientes/main.py` | Endpoints `POST /tasks` y `GET /tasks`; enlace a `127.0.0.1`. |
| Nuevo | `@back/tests/test_tasks.py` | 4 pruebas del núcleo mínimo. |
