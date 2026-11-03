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
| Task o bug en curso | [task-1-listado-tareas](./tasks/task-1-listado-tareas/README.md) |
| Siguiente subtask | [subtask-2-ui-lista](./tasks/task-1-listado-tareas/subtask-2-ui-lista.md) (en curso) |
| Rama y repos | `feat/listado-tareas` (en `back/` y `front/`) |
| Última sesión (fecha y resumen) | 2026-03-04 · subtask 2 iniciada: la lista se ve en el navegador; faltan formulario y filtros |
| Pendiente al reanudar | Formulario de alta y controles de filtro en `@front`; mensaje con la API caída; diseño visual (valor por defecto: tabla simple) |

## 2. Catálogo de guías

Elige por la columna «cuándo». Archivo: `method/playbooks/<playbook>.md`. Skill: `dev-<playbook>` si la herramienta las tiene.

| Playbook | Qué hace | Cuándo usarla | Skill |
|---|---|---|---|
| `start-session` | Resuelve la frase de entrada, lee lo mínimo y verifica el repo. | «continúa task-N», «siguiente», «bug-N», brief adjunto. | `dev-start-session` |
| `close-session` | Lista única de cierre; cierra, archiva y anota la retro de una task en `RETRO.md`. | Al terminar o interrumpir una subtask; al cerrar una task. | `dev-close-session` |
| `write-task` | Planifica una task y redacta README y briefs de subtask. | Planificar un desarrollo; crear o editar subtasks; cambiar estados. | `dev-write-task` |
| `write-report` | Report, changelog derivado, plan-vs-actual e informe funcional. | Cerrar una subtask; terminar una investigación; explicar a un equipo no técnico qué se puede hacer. | `dev-write-report` |
| `update-docs` | Dónde va cada conocimiento; páginas de docs con frescura. | Tocar un área documentada; cambiar comportamiento; cerrar un cambio. | `dev-update-docs` |
| `fix-bug` | Brief y reglas de bugfix con prueba que falla antes. | Corregir un error en código existente. | `dev-fix-bug` |
| `develop-code` | Código limpio, arquitectura, testing y stacks activos. | Escribir, modificar o probar código. | `dev-develop-code` |
| `record-decision` | Decisiones por task y promoción a ADR. | Aprobar o tomar por defecto una decisión; cerrar una task. | `dev-record-decision` |
| `commit-pr` | Mensaje de commit por subtask e informe de PR por task. | Cerrar subtask o task; pedir commit. | `dev-commit-pr` |
| `diagnose` | Ejecuta `check.py`, interpreta los hallazgos y propone arreglos. | «Diagnostica dev/»; al cerrar una task; tras actualizar el paquete. | `dev-diagnose` |

## 3. Tasks

| Task | Estado | Subtasks hechas / total | Último report | Siguiente paso | Retro pendiente |
|---|---|---|---|---|---|
| [task-1-listado-tareas](./tasks/task-1-listado-tareas/README.md) | en curso | 1 / 2 | [subtask 1](./reports/task-1-listado-tareas/subtask-1-api.md) y [parcial de la 2](./reports/task-1-listado-tareas/subtask-2-ui-lista.md) | Formulario y filtros en la UI (subtask 2) | no |

## 4. Bugs

| Bug | Estado | Subtasks hechas / total | Último report | Siguiente paso |
|---|---|---|---|---|
| — | — | — | — | — |

## 5. Backlog

| Ítem | Origen | Nota |
|---|---|---|
| Etiquetas por tarea | Conversación con el desarrollador, 2026-03-01 | Fuera de la task 1; se redacta cuando se cierre. |

Docs técnicos: [docs/README.md](../docs/README.md).
