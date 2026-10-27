# Subtask N — <!-- resultado en una frase -->

<!-- Plantilla de brief. Guía: method/playbooks/write-task.md §4. Copia a work/tasks/task-N-nombre/subtask-N-descripcion.md. Quita solo las secciones que claramente no correspondan y borra los comentarios. -->

**Tipo:** <!-- marco | funcionalidad | endurecimiento | investigación -->
**Esfuerzo:** <!-- S horas · M un día · L varios días -->
**Modelo sugerido:** <!-- opcional, texto libre; borra la línea si no aplica -->
**Repos afectados:** <!-- alias de PROJECT.md §1, p. ej. @back, @front -->

## Instrucciones para esta sesión

Lee antes de actuar:

1. <!-- README de la task y decisions.md -->
2. <!-- reports de las subtasks previas de las que depende -->
3. <!-- páginas de docs/ del área que vas a tocar -->
4. <!-- guías aplicables: playbook develop-code y stacks activos -->

Contrasta este brief con el estado real del repositorio: no des por hecha una subtask previa por su número. Si una dependencia no está lista, comprueba su estado y no inventes el resultado.

## Objetivo dentro de la task

<!-- Qué entrega esta subtask y por qué es necesaria para el objetivo mayor. Qué habilita después. -->

## Historia de usuario

<!-- Opcional. Como [rol], quiero [capacidad], para [beneficio]. No sustituye a los requisitos. -->

## Contexto y decisiones aprobadas

- <!-- Estado actual y fuentes canónicas, con rutas con alias: @repo/ruta/archivo:línea -->
- <!-- Decisiones por ID (T<N>-…, ADR) y sus motivos si no son obvios -->
- <!-- Supuestos no verificados y preguntas abiertas, marcados como tales -->
- <!-- Términos técnicos esenciales, explicados según «Tecnologías que NO conozco» de DEV-PROFILE.md -->

## Alcance, límites y exclusiones

- **Hacer:** <!-- lista concreta -->
- **No hacer:** <!-- lista concreta -->
- **Repos afectados:** <!-- alias -->
- **Intocable:** <!-- archivos, contratos o comportamientos; zonas de PROJECT.md §4 -->
- **Restricciones aplicables:** <!-- IDs: C1, C2 (proyecto), T<N>-C1 (task). Repite en una línea las críticas -->

## Trabajo

1. <!-- Inspeccionar el código y las fuentes relevantes -->
2. <!-- Paso concreto y comprobable -->
3. <!-- Verificar ejecutando (comandos en COMANDOS.md §2) -->

## Resultado y criterios de aceptación

<!-- Resultados observables y comprobables, no «funciona bien». Cubre lo aplicable: comportamiento y casos de uso, errores y límites, pruebas del núcleo mínimo, verificación manual o visual, validación de enlaces si es documental. -->

- <!-- Criterio 1 -->
- <!-- Criterio 2 -->

## Dependencias y siguiente paso

- **Necesita:** <!-- subtasks realmente necesarias -->
- **Desbloquea:** <!-- subtasks siguientes -->
- **En paralelo:** <!-- solo si no edita los mismos archivos -->

## Fuera de alcance

- <!-- Cambios o decisiones no autorizados -->

## Impacto en docs

| Página de docs | Cambio esperado |
|---|---|
| <!-- docs/área/página.md --> | <!-- qué se añade o corrige; o «ninguno» con el motivo --> |

## Entregables y cierre de sesión

- Código y pruebas: <!-- rutas con alias -->
- Docs: <!-- páginas a actualizar, ver «Impacto en docs» -->
- Report: `work/reports/task-N-nombre/subtask-N-descripcion.md` ([method/templates/report.md](./report.md))
- Changelog (solo si cambia código funcional): `work/changelogs/task-N-nombre/subtask-N-descripcion.md`
- Al cerrar: marca el estado de esta subtask en el README de la task, actualiza `INDEX.md` y deja en el report el mensaje de commit sugerido y el siguiente paso.
- Comunica: preguntas abiertas, limitaciones, evidencia de verificación y lo que no pudiste ejecutar.
