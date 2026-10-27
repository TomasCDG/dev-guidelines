---
name: write-report
description: Redacta el report de una subtask, su changelog derivado y los planes-vs-realidad. Úsala cuando cierres una subtask, termines una investigación, necesites comparar el plan con lo construido o deban redactarse propuestas de desarrollo.
---

# Redactar reports y changelogs

Un **report** es para el desarrollador (historial legible). Lo que el agente reutiliza como verdad técnica va a `docs/` ([update-docs](./update-docs.md)).

## 1. Reports

Ubicación: `work/reports/task-N-nombre/subtask-N-descripcion.md` (o `bug-N-nombre`). Plantilla: [report](../templates/report.md).

- Arranca con **fecha de redacción** e **índice anidado**.
- Si la fila «Tecnologías que NO conozco» de `DEV-PROFILE.md` tiene alguna, añade un **glosario** justo después del índice.
- Usa **tablas** y gráficos. Diagramas en **mermaid** con colores mate, legibles y contrastados; cada diagrama lleva **epígrafe** y la descripción punto por punto del proceso.
- Bloques de código solo cuando sean imprescindibles.
- Capturas y evidencia en `work/reports/task-N-nombre/assets/` (el material de origen del brief va en `work/tasks/task-N-nombre/assets/`).
- Secciones fijas del cierre de una subtask:
  - **Qué cambió** (tabla; es la fuente del changelog).
  - **Verificación** realizada y lo que no se pudo verificar.
  - **Decisiones y desviaciones** respecto al brief (incluye correcciones de `INDEX.md`).
  - **Impacto en docs:** tabla `página → cambio`, o «ninguno» con motivo ([update-docs](./update-docs.md) §6).
  - **Siguiente paso:** para que la sesión siguiente se ubique.
  - **Mensaje de commit sugerido** ([commit-pr](./commit-pr.md)).
- Report **parcial** si la subtask no cierra: mismas secciones con lo hecho y lo que falta ([close-session](./close-session.md) §2).

## 2. Changelogs

Ubicación: `work/changelogs/task-N-nombre/subtask-N-descripcion.md`. Plantilla: [changelog](../templates/changelog.md).

- **Solo si cambia código funcional.** Docs, reports y otros documentos no cuentan.
- **Se deriva del report:** reproduce la tabla «Qué cambió» con fecha, título breve y user story o commit (si existe). No se redacta una versión distinta.
- Fecha e índice al inicio.

## 3. Plan frente a realidad

Antes o después de una task grande, compara lo planeado con lo construido y con el estado real: [plan-vs-actual](../templates/plan-vs-actual.md). Guárdalo como `work/reports/task-N-nombre/00-plan-vs-actual.md`.

## 4. Propuestas de desarrollo

Al final de una task o cambio, redáctalas con descripción, alcance, ventajas, riesgos y esfuerzo.
