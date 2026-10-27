# Subtask 1 — API para crear y listar tareas con almacenamiento en SQLite

**Tipo:** marco
**Esfuerzo:** M
**Modelo sugerido:** el más capaz
**Repos afectados:** `@back`

## Instrucciones para esta sesión

Lee antes de actuar:

1. [README de la task](./README.md) y [decisions.md](./decisions.md).
2. [ADR-001](../../../docs/decisions/ADR-001-solo-localhost.md).
3. Docs: no existen páginas de contratos todavía; esta subtask las crea.
4. Guías: playbook `develop-code` y el stack Python.

Contrasta este brief con el estado real del repositorio.

## Objetivo dentro de la task

Entregar la base que usan las demás subtasks: una API con `POST /tasks` y `GET /tasks`, y el almacenamiento persistente.

## Historia de usuario

Como usuario, quiero crear tareas y ver mi lista, para no depender de la línea de comandos.

## Contexto y decisiones aprobadas

- Hoy existe un script que guarda tareas en un archivo de texto (`@back/tools/legacy_cli.py`).
- T1-D1 (solo localhost, ADR-001) y T1-D4 (SQLite).
- Supuesto no verificado: no hay datos reales que migrar del archivo de texto.

## Alcance, límites y exclusiones

- **Hacer:** modelo `Task`, repositorio SQLite, endpoints `POST /tasks` y `GET /tasks`.
- **No hacer:** filtros, edición, borrado, UI.
- **Repos afectados:** `@back`
- **Intocable:** `@back/migrations/` (solo añadir).
- **Restricciones aplicables:** C1, C2, C3.

## Trabajo

1. Inspeccionar `@back/tools/legacy_cli.py` para conservar los nombres de campo.
2. Definir el modelo y el repositorio (capa de acceso a datos aislada del endpoint).
3. Implementar los endpoints con validación en el borde.
4. Escribir las pruebas del núcleo mínimo.
5. Levantar la API y comprobar con `curl`.

## Resultado y criterios de aceptación

- `POST /tasks` con `{"title": "Comprar pan"}` devuelve 201 y la tarea con `id` y `status: "pending"`.
- `GET /tasks` devuelve las tareas creadas, de la más nueva a la más antigua.
- Un título vacío devuelve 422.
- Reiniciar la API conserva las tareas.
- Pruebas, lint y type-check pasan.

## Dependencias y siguiente paso

- **Necesita:** nada.
- **Desbloquea:** subtask 2.

## Fuera de alcance

- Autenticación y acceso remoto.

## Impacto en docs

| Página de docs | Cambio esperado |
|---|---|
| `docs/contracts/api-tareas.md` | Crear: endpoints y campos. |
| `docs/architecture/almacenamiento.md` | Crear: tabla y capa de datos. |

## Entregables y cierre de sesión

- Código y pruebas: `@back/src/pendientes/`, `@back/tests/`
- Docs: ver «Impacto en docs».
- Report: `work/reports/task-1-listado-tareas/subtask-1-api-crud.md`
- Changelog: `work/changelogs/task-1-listado-tareas/subtask-1-api-crud.md`
- Al cerrar: marca el estado en el README de la task, actualiza `INDEX.md` y deja mensaje de commit y siguiente paso en el report.
