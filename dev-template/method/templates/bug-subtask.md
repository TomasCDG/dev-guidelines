# Subtask N — <!-- arreglo en una frase -->

<!-- Plantilla de brief de bug. Guía: method/playbooks/fix-bug.md. Copia a work/bugs/bug-N-nombre/subtask-N-descripcion.md. Misma estructura que subtask.md más las secciones propias del bug. -->

**Esfuerzo:** <!-- S horas · M un día · L varios días -->
**Modelo sugerido:** <!-- opcional, texto libre; borra la línea si no aplica -->
**Repos afectados:** <!-- alias de PROJECT.md §1 -->

## Instrucciones para esta sesión

Lee antes de actuar:

1. <!-- README del bug -->
2. <!-- página de docs/ del área afectada -->
3. <!-- guías aplicables: playbooks develop-code, fix-bug y stacks activos -->

Contrasta con el estado real del repositorio: confirma que el bug sigue reproduciéndose antes de arreglarlo.

## Objetivo

<!-- Qué comportamiento queda corregido. -->

## Síntoma y reproducción

- **Síntoma:** <!-- -->
- **Pasos para reproducirlo:** <!-- 1. … 2. … -->

## Esperado frente a observado

| | Comportamiento |
|---|---|
| Esperado | <!-- --> |
| Observado | <!-- --> |

## Causa raíz

<!-- «Confirmada» o «Hipótesis» (marca cuál). Si es hipótesis, primer paso del trabajo: confirmarla. Rutas con alias: @repo/ruta/archivo:línea -->

## Alcance, límites y exclusiones

- **Cambio mínimo necesario.** No refactorices ni añadas funcionalidad nueva.
- **Intocable:** <!-- archivos o contratos; zonas de PROJECT.md §4 -->
- **Restricciones aplicables:** <!-- IDs C1…, B<N>-… -->

## Trabajo

1. Escribe una prueba que reproduzca el bug y **falle** antes del arreglo.
2. <!-- Arreglo mínimo -->
3. Comprueba que la prueba pasa y que no se rompe nada existente (comandos en `COMANDOS.md` §2).

## Resultado y criterios de aceptación

- La prueba nueva falla antes del arreglo y pasa después.
- <!-- Verificación manual de que el síntoma ya no aparece -->
- <!-- Casos límite relacionados -->

## Fuera de alcance

- <!-- -->

## Impacto en docs

| Página de docs | Cambio esperado |
|---|---|
| <!-- --> | <!-- corrección si estaba mal documentado; o «ninguno» con el motivo --> |

## Entregables y cierre de sesión

- Código y prueba: <!-- rutas con alias -->
- Report: `work/reports/bug-N-nombre/subtask-N-descripcion.md` ([report.md](./report.md))
- Changelog (si cambia código funcional): `work/changelogs/bug-N-nombre/subtask-N-descripcion.md`
- Al cerrar: estado en el README del bug, `INDEX.md`, mensaje de commit y siguiente paso en el report.
