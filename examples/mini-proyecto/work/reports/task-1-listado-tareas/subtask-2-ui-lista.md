# Task 1, subtask 2 — Pantalla web con lista, formulario y filtros (REPORT PARCIAL)

**Fecha:** 2026-03-04
**Rama / repos:** `feat/listado-tareas` en `@front`; cambios sin commitear
**Brief:** [subtask-2-ui-lista.md](../../tasks/task-1-listado-tareas/subtask-2-ui-lista.md)

> Report parcial: la subtask sigue `en curso`. Lo lee la sesión siguiente (playbook `start-session` §2, punto 5) para saber dónde quedó el trabajo.

## Contenido

1. [Hecho hasta ahora](#1-hecho-hasta-ahora)
2. [Falta](#2-falta)
3. [Siguiente paso](#3-siguiente-paso)

## 1. Hecho hasta ahora

| Tipo | Archivo (con alias) | Cambio |
|---|---|---|
| Nuevo | `@front/src/api/tasks.ts` | Tipos de la respuesta y funciones que llaman a `GET /tasks` y `POST /tasks`. |
| Nuevo | `@front/src/hooks/useTasks.ts` | *Hook* (función de React que guarda datos y los recarga): pide la lista a la API. |
| Nuevo | `@front/src/components/TaskList.tsx` | *Componente* (pieza de pantalla reutilizable) que dibuja la lista en una tabla. |

Verificación: la lista se ve en http://localhost:5173 con las tareas creadas desde `/docs` (E1); pruebas y type-check pasan.

## 2. Falta

- Formulario de alta que añade la tarea sin recargar.
- Controles de estado y texto que piden los filtros a la API (T1-C1).
- Mensaje claro con la API caída.
- Pregunta abierta con valor por defecto: diseño visual. Por defecto, tabla simple.

## 3. Siguiente paso

Crear el formulario y los controles de filtro, verificar en pantalla y cerrar la subtask con la lista de `close-session` §1.
