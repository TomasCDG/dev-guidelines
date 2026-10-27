# API de tareas

**Fecha:** 2026-03-03
**Estado:** vigente
**Verificado contra:** `a1b2c3d`
**Código relacionado:** `@back/src/pendientes/main.py`, `@back/src/pendientes/models.py`

## Contenido

1. [Endpoints](#1-endpoints)
2. [Campos de una tarea](#2-campos-de-una-tarea)
3. [Errores](#3-errores)

## 1. Endpoints

La API escucha solo en `127.0.0.1:8000` ([ADR-001](../decisions/ADR-001-solo-localhost.md)).

| Método y ruta | Entrada | Respuesta | Código |
|---|---|---|---|
| `POST /tasks` | `{"title": "texto"}` | La tarea creada | 201 |
| `GET /tasks` | — | Lista de tareas, de la más nueva a la más antigua | 200 |

## 2. Campos de una tarea

| Campo | Tipo | Significado | Fuente |
|---|---|---|---|
| `id` | entero | Identificador asignado por la API. | `@back/src/pendientes/models.py` |
| `title` | texto | Título; no puede estar vacío. | `@back/src/pendientes/models.py` |
| `status` | `"pending"` o `"done"` | Estado; una tarea nueva es `pending`. | `@back/src/pendientes/models.py` |
| `created_at` | fecha ISO 8601 | Momento de creación. | `@back/src/pendientes/models.py` |

## 3. Errores

| Caso | Resultado |
|---|---|
| `title` vacío o ausente en `POST /tasks` | 422 con el detalle del campo |
