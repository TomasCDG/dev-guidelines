# Changelog — Task 1, subtask 1: API para crear, listar y filtrar tareas

**Fecha:** 2026-03-03
**Report:** [subtask-1-api.md](../../reports/task-1-listado-tareas/subtask-1-api.md)

## Contenido

1. [2026-03-03 — API para crear, listar y filtrar tareas](#2026-03-03--api-para-crear-listar-y-filtrar-tareas)

## 2026-03-03 — API para crear, listar y filtrar tareas

**User story:** Como usuario, quiero crear tareas, ver mi lista y filtrarla, para no depender de la línea de comandos.
**Commit:** `a1b2c3d`

| Tipo | Archivo (con alias) | Cambio |
|---|---|---|
| Nuevo | `@back/src/pendientes/models.py` | Modelo `Task` y validación del título. |
| Nuevo | `@back/src/pendientes/repository.py` | Acceso a SQLite aislado de los endpoints; filtros `status` y `q` en la consulta. |
| Cambiado | `@back/src/pendientes/main.py` | Endpoints `POST /tasks` y `GET /tasks` (con `status` y `q`); enlace a `127.0.0.1`. |
| Nuevo | `@back/tests/test_tasks.py` | 7 pruebas del núcleo mínimo. |
