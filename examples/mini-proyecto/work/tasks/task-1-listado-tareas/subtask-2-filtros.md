# Subtask 2 — Filtrar tareas por estado y por texto en la API

**Tipo:** funcionalidad
**Esfuerzo:** S
**Modelo sugerido:** intermedio
**Repos afectados:** `@back`

## Instrucciones para esta sesión

Lee antes de actuar:

1. [README de la task](./README.md) y [decisions.md](./decisions.md).
2. [Report de la subtask 1](../../reports/task-1-listado-tareas/subtask-1-api-crud.md) (sección «Siguiente paso»).
3. Docs: [api-tareas.md](../../../docs/contracts/api-tareas.md) y [almacenamiento.md](../../../docs/architecture/almacenamiento.md).
4. Guías: playbook `develop-code` y el stack Python.

Contrasta este brief con el estado real del repositorio: la subtask 1 debe estar hecha.

## Objetivo dentro de la task

Que `GET /tasks` acepte filtros, para que la UI de la subtask 3 solo dibuje el resultado (T1-C1).

## Historia de usuario

Como usuario, quiero ver solo las tareas pendientes o las que contienen una palabra, para encontrar rápido lo que busco.

## Contexto y decisiones aprobadas

- Estado actual: `GET /tasks` devuelve todo (`@back/src/pendientes/main.py`).
- T1-D2: el filtrado vive en la API. T1-D3: la búsqueda por texto no distingue mayúsculas (decisión del agente, a confirmar).
- Pregunta abierta: ¿se filtran también los acentos? Valor por defecto: no.

## Alcance, límites y exclusiones

- **Hacer:** parámetros `status` (`pending`/`done`) y `q` (texto) en `GET /tasks`.
- **No hacer:** paginación, orden configurable, cambios de campos existentes (C3).
- **Repos afectados:** `@back`
- **Intocable:** `@back/migrations/`.
- **Restricciones aplicables:** C1, C2, C3, T1-C1. Las críticas, en una línea: solo `127.0.0.1` (C1), sin dependencias nuevas (C2), cambios aditivos en la API: sin parámetros el resultado no cambia (C3), el filtrado se calcula en la API (T1-C1).

## Trabajo

1. Leer la página de contratos y el repositorio actual.
2. Añadir los parámetros con validación (un `status` desconocido devuelve 422).
3. Implementar el filtro en la consulta SQL, no en Python sobre la lista completa.
4. Pruebas del núcleo mínimo.
5. Probar con `curl`.

## Resultado y criterios de aceptación

- `GET /tasks?status=pending` devuelve solo pendientes.
- `GET /tasks?q=pan` devuelve las tareas cuyo título contiene «pan», sin distinguir mayúsculas.
- Combinar ambos parámetros aplica los dos filtros.
- `GET /tasks?status=otro` devuelve 422.
- Sin parámetros, el resultado es idéntico al de antes (C3).

## Dependencias y siguiente paso

- **Necesita:** subtask 1 (hecha).
- **Desbloquea:** subtask 3.

## Fuera de alcance

- Paginación y ordenación.

## Impacto en docs

| Página de docs | Cambio esperado |
|---|---|
| `docs/contracts/api-tareas.md` | Añadir los parámetros `status` y `q` y los errores 422. |

## Entregables y cierre de sesión

- Código y pruebas: `@back/src/pendientes/`, `@back/tests/`
- Docs: ver «Impacto en docs».
- Report: `work/reports/task-1-listado-tareas/subtask-2-filtros.md`
- Changelog: `work/changelogs/task-1-listado-tareas/subtask-2-filtros.md`
- Al cerrar: marca el estado en el README de la task, actualiza `INDEX.md` y deja mensaje de commit y siguiente paso en el report.
