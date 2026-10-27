# INDEX — estado del desarrollo

Tablero mantenido por el agente. **No sustituye a la verificación del repo real**: si algo aquí contradice el código o git, manda el repo y se corrige este archivo.

**Última actualización:** 2026-03-04

## Contenido

1. [Activo ahora](#1-activo-ahora)
2. [Catálogo de guías](#2-catálogo-de-guías)
3. [Tasks](#3-tasks)
4. [Bugs](#4-bugs)
5. [Backlog](#5-backlog)

## 1. Activo ahora

| Campo | Valor |
|---|---|
| Task o bug en curso | [task-1-listado-tareas](./work/tasks/task-1-listado-tareas/README.md) |
| Siguiente subtask | [subtask-2-filtros](./work/tasks/task-1-listado-tareas/subtask-2-filtros.md) (en curso) |
| Rama y repos | `feat/listado-tareas` (en `back/` y `front/`) |
| Última sesión (fecha y resumen) | 2026-03-04 · subtask 2 iniciada: filtro por estado hecho en la API; falta filtro por texto |
| Pendiente al reanudar | Filtro por texto en `repository.py`; ampliar pruebas; decidir el manejo de acentos (valor por defecto: no normalizar) |

## 2. Catálogo de guías

Elige por la columna «cuándo». Archivo: `method/playbooks/<playbook>.md`. Skill: `dev-<playbook>` si la herramienta las tiene.

| Playbook | Qué hace | Cuándo usarla | Skill |
|---|---|---|---|
| `start-session` | Resuelve la frase de entrada, lee lo mínimo y verifica el repo. | «continúa task-N», «siguiente», «bug-N», brief adjunto. | `dev-start-session` |
| `close-session` | Lista única de cierre; cierra, archiva y anota la retro de una task en `RETRO.md`. | Al terminar o interrumpir una subtask; al cerrar una task. | `dev-close-session` |
| `write-task` | Planifica una task y redacta README y briefs de subtask. | Planificar un desarrollo; crear o editar subtasks; cambiar estados. | `dev-write-task` |
| `write-report` | Report, changelog derivado y plan-vs-actual. | Cerrar una subtask; terminar una investigación. | `dev-write-report` |
| `update-docs` | Dónde va cada conocimiento; páginas de docs con frescura. | Tocar un área documentada; cambiar comportamiento; cerrar un cambio. | `dev-update-docs` |
| `fix-bug` | Brief y reglas de bugfix con prueba que falla antes. | Corregir un error en código existente. | `dev-fix-bug` |
| `develop-code` | Código limpio, arquitectura, testing y stacks activos. | Escribir, modificar o probar código. | `dev-develop-code` |
| `record-decision` | Decisiones por task y promoción a ADR. | Aprobar o tomar por defecto una decisión; cerrar una task. | `dev-record-decision` |
| `commit-pr` | Mensaje de commit por subtask e informe de PR por task. | Cerrar subtask o task; pedir commit. | `dev-commit-pr` |
| `diagnose` | Ejecuta `check.py`, interpreta los hallazgos y propone arreglos. | «Diagnostica dev/»; al cerrar una task; tras actualizar el paquete. | `dev-diagnose` |

## 3. Tasks

| Task | Estado | Subtasks hechas / total | Último report | Siguiente paso | Retro pendiente |
|---|---|---|---|---|---|
| [task-1-listado-tareas](./work/tasks/task-1-listado-tareas/README.md) | en curso | 1 / 3 | [subtask 1](./work/reports/task-1-listado-tareas/subtask-1-api-crud.md) y [parcial de la 2](./work/reports/task-1-listado-tareas/subtask-2-filtros.md) | Terminar el filtro por texto (subtask 2) | no |

## 4. Bugs

| Bug | Estado | Subtasks hechas / total | Último report | Siguiente paso |
|---|---|---|---|---|
| — | — | — | — | — |

## 5. Backlog

| Ítem | Origen | Nota |
|---|---|---|
| Etiquetas por tarea | Conversación con el desarrollador, 2026-03-01 | Fuera de la task 1; se redacta cuando se cierre. |

Docs técnicos: [docs/README.md](./docs/README.md).
