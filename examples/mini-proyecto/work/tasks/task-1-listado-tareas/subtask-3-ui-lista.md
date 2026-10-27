# Subtask 3 — Pantalla web con lista, formulario y filtros

**Tipo:** funcionalidad
**Esfuerzo:** M
**Modelo sugerido:** intermedio
**Repos afectados:** `@front`

## Instrucciones para esta sesión

Lee antes de actuar:

1. [README de la task](./README.md) y [decisions.md](./decisions.md).
2. Reports de las subtasks 1 y 2 en `work/reports/task-1-listado-tareas/` (la 2 aún no existe: comprueba su estado real).
3. Docs: [api-tareas.md](../../../docs/contracts/api-tareas.md).
4. Guías: playbook `develop-code` y el stack TypeScript + React.

Contrasta este brief con el estado real del repositorio. Si la subtask 2 no está hecha, no inventes el resultado: avisa.

## Objetivo dentro de la task

Entregar la pantalla que cierra el objetivo de la task: ver, crear y filtrar tareas desde el navegador.

## Historia de usuario

Como usuario, quiero una página con mi lista y un formulario, para gestionar mis tareas sin la terminal.

## Contexto y decisiones aprobadas

- La UI solo dibuja; los filtros se piden a la API (T1-C1).
- El desarrollador no conoce React: el report explica *componente*, *hook* y *props* en lenguaje sencillo (fila «Tecnologías que NO conozco» de `DEV-PROFILE.md`).
- Pregunta abierta: diseño visual. Valor por defecto: tabla simple.

## Alcance, límites y exclusiones

- **Hacer:** componente de lista, formulario de alta, controles de filtro, hook que llama a la API.
- **No hacer:** cambios en `@back`, edición o borrado, estilos elaborados.
- **Repos afectados:** `@front`
- **Restricciones aplicables:** C1, C2, T1-C1.

## Trabajo

1. Leer el contrato de la API en docs.
2. Definir los tipos TypeScript de la respuesta.
3. Crear el hook de datos y los componentes.
4. Pruebas de las funciones puras que deciden qué mostrar.
5. Verificar en el navegador (comandos en `COMANDOS.md` §2).

## Resultado y criterios de aceptación

- La página muestra las tareas devueltas por `GET /tasks`.
- Crear una tarea desde el formulario la añade a la lista sin recargar.
- Los controles de estado y texto cambian la lista pidiendo los filtros a la API.
- Con la API caída aparece un mensaje claro, no una pantalla en blanco.
- Pruebas, lint y type-check pasan; captura de la pantalla en el report.

## Dependencias y siguiente paso

- **Necesita:** subtask 2.
- **Desbloquea:** cierre de la task.

## Fuera de alcance

- Estilos avanzados, edición, borrado.

## Impacto en docs

| Página de docs | Cambio esperado |
|---|---|
| ninguno | La UI no tiene contrato propio; el contrato de la API no cambia. |

## Entregables y cierre de sesión

- Código y pruebas: `@front/src/`
- Report: `work/reports/task-1-listado-tareas/subtask-3-ui-lista.md`
- Changelog: `work/changelogs/task-1-listado-tareas/subtask-3-ui-lista.md`
- Al cerrar la última subtask: informe de PR de la task y actualización de `INDEX.md`.
