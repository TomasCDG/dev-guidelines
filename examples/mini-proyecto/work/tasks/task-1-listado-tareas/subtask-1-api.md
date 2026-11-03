# Subtask 1 — API para crear, listar y filtrar tareas con almacenamiento en SQLite

**Tipo:** funcionalidad
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

Entregar la API completa que consume la UI de la subtask 2: `POST /tasks`, `GET /tasks` con filtros por estado y por texto, y el almacenamiento persistente. La UI solo dibuja (T1-C1).

## Historia de usuario

Como usuario, quiero crear tareas, ver mi lista y filtrarla, para no depender de la línea de comandos.

## Contexto y decisiones aprobadas

- Hoy existe un script que guarda tareas en un archivo de texto (`@back/tools/legacy_cli.py`).
- T1-D1 (solo localhost, ADR-001), T1-D2 (el filtrado vive en la API) y T1-D4 (SQLite).
- T1-D3: la búsqueda por texto no distingue mayúsculas (decisión del agente, a confirmar).
- Supuesto no verificado: no hay datos reales que migrar del archivo de texto.
- Pregunta abierta: ¿se ignoran los acentos al buscar? Valor por defecto: no.

## Alcance, límites y exclusiones

- **Hacer:** modelo `Task`, repositorio SQLite, `POST /tasks` y `GET /tasks` con los parámetros `status` (`pending`/`done`) y `q` (texto).
- **No hacer:** paginación, orden configurable, edición, borrado, UI.
- **Repos afectados:** `@back`
- **Intocable:** `@back/migrations/` (solo añadir).
- **Restricciones aplicables:** C1, C2, C3, T1-C1. Las críticas, en una línea: solo `127.0.0.1` (C1), sin dependencias nuevas (C2), el filtrado se calcula en la API (T1-C1).

## Trabajo

**Herramientas:** API local en `http://127.0.0.1:8000/docs` para probar los endpoints (`ENTORNO.md` §1). Ninguna regla `E…` aplica: E1 es solo para `@front`.

1. Inspeccionar `@back/tools/legacy_cli.py` para conservar los nombres de campo.
2. Definir el modelo y el repositorio (capa de acceso a datos aislada del endpoint).
3. Implementar los endpoints con validación en el borde; un `status` desconocido devuelve 422.
4. Aplicar los filtros en la consulta SQL, no en Python sobre la lista completa.
5. Escribir las pruebas del núcleo mínimo.
6. Levantar la API y comprobar con `curl`.

## Resultado y criterios de aceptación

- `POST /tasks` con `{"title": "Comprar pan"}` devuelve 201 y la tarea con `id` y `status: "pending"`.
- `GET /tasks` devuelve las tareas creadas, de la más nueva a la más antigua.
- `GET /tasks?status=pending` devuelve solo pendientes; `GET /tasks?q=pan`, las que contienen «pan» sin distinguir mayúsculas; combinados aplican los dos filtros.
- Un título vacío o `status=otro` devuelven 422.
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
| `docs/contracts/api-tareas.md` | Crear: endpoints, parámetros de filtro, campos y errores. |
| `docs/architecture/almacenamiento.md` | Crear: tabla y capa de datos. |

## Entregables y cierre de sesión

- Código y pruebas: `@back/src/pendientes/`, `@back/tests/`
- Docs: ver «Impacto en docs».
- Report: `work/reports/task-1-listado-tareas/subtask-1-api.md`
- Changelog: `work/changelogs/task-1-listado-tareas/subtask-1-api.md`
- Al cerrar: marca el estado en el README de la task, actualiza `INDEX.md` y deja mensaje de commit y siguiente paso en el report.
