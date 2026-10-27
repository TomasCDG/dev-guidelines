# INDEX — estado del desarrollo

Tablero mantenido por el agente. **No sustituye a la verificación del repo real**: si algo aquí contradice el código o git, manda el repo y se corrige este archivo.

**Última actualización:** TODO

## Contenido

1. [Activo ahora](#1-activo-ahora)
2. [Catálogo de guías](#2-catálogo-de-guías)
3. [Tasks](#3-tasks)
4. [Bugs](#4-bugs)
5. [Backlog](#5-backlog)

## 1. Activo ahora

Con esta sección y el README de la task se retoma el trabajo.

| Campo | Valor |
|---|---|
| Task o bug en curso | — |
| Siguiente subtask | — |
| Rama y repos | — |
| Última sesión (fecha y resumen) | — |
| Pendiente al reanudar (parcial, bloqueos, preguntas) | — |

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

Estado de task: `borrador`, `en curso`, `pausada`, `hecha (archivada)`. Estado de subtask: ver el README de cada task. Al cerrar una task se mueve a `work/tasks/archive/` y aquí queda como `hecha (archivada)` con su ruta.

| Task | Estado | Subtasks hechas / total | Último report | Siguiente paso | Retro pendiente |
|---|---|---|---|---|---|
| — | — | — | — | — | — |

«Retro pendiente»: `sí` si la task cerró con una fila `pendiente` en [RETRO.md](./RETRO.md) aún sin procesar con `dev-feedback`.

## 4. Bugs

| Bug | Estado | Subtasks hechas / total | Último report | Siguiente paso |
|---|---|---|---|---|
| — | — | — | — | — |

## 5. Backlog

Pendientes que todavía no son tasks. Docs técnicos: [docs/README.md](./docs/README.md).

| Ítem | Origen | Nota |
|---|---|---|
| — | — | — |
