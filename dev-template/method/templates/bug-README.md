# Bug N — <!-- síntoma en una frase -->

<!-- Plantilla de README de bug. Guía: method/playbooks/fix-bug.md y write-task.md §3. Copia a work/bugs/bug-N-nombre/README.md. -->

**Fecha:** <!-- AAAA-MM-DD -->
**Estado:** <!-- borrador | en curso | hecho | pausado -->
**Rama / repos:** <!-- rama y alias de repos afectados -->
**Origen:** <!-- quién lo detectó, dónde, versión o commit -->

## Contenido

1. [Síntoma](#1-síntoma)
2. [Reproducción](#2-reproducción)
3. [Esperado frente a observado](#3-esperado-frente-a-observado)
4. [Causa raíz](#4-causa-raíz)
5. [Decisiones y restricciones](#5-decisiones-y-restricciones)
6. [Índice de subtasks](#6-índice-de-subtasks)
7. [Qué necesita del desarrollador](#7-qué-necesita-del-desarrollador)
8. [Entregables](#8-entregables)

## 1. Síntoma

<!-- Qué ve el usuario o el sistema. Con evidencia: captura, log, mensaje de error. -->

## 2. Reproducción

1. <!-- Paso reproducible -->
2. <!-- Paso reproducible -->

## 3. Esperado frente a observado

| | Comportamiento |
|---|---|
| Esperado | <!-- --> |
| Observado | <!-- --> |

## 4. Causa raíz

<!-- Escribe «Confirmada» o «Hipótesis» al inicio. Si es hipótesis, indica cómo confirmarla. Rutas con alias: @repo/ruta/archivo:línea -->

## 5. Decisiones y restricciones

- Restricciones del proyecto: `PROJECT.md` §3 (`C1…`). Aplicables aquí: <!-- IDs -->
- **Cambio mínimo necesario.** No mezclar con funcionalidad nueva; si el arreglo la exige, abrir una task aparte y enlazarla.
- <!-- Decisiones propias del bug (IDs B<N>-…) -->

## 6. Índice de subtasks

Estado: `pendiente` · `en curso` · `hecha` (sin commit) · `hecha (commit <hash>)`. El agente actualiza la columna al cerrar y refleja el resumen en `INDEX.md`.

| # | Subtask | Resultado | Esfuerzo | Modelo sugerido | Depende de | Estado |
|---|---|---|---|---|---|---|
| 1 | [subtask-1-descripcion](./subtask-1-descripcion.md) | <!-- --> | <!-- S/M/L --> | <!-- opcional --> | — | pendiente |

## 7. Qué necesita del desarrollador

| Ítem | Necesario para | Valor por defecto del agente mientras tanto |
|---|---|---|
| <!-- --> | <!-- --> | <!-- --> |

## 8. Entregables

- Reports en `work/reports/bug-N-nombre/`.
- Changelog en `work/changelogs/bug-N-nombre/` solo si cambia código funcional.
- Docs corregidos si el bug revela un hecho mal documentado.
