---
name: fix-bug
description: Planifica y corrige un bug con el cambio mínimo y una prueba que falla antes y pasa después. Úsala cuando el trabajo sea corregir un error en código existente («bug-N») y no desarrollar funcionalidad nueva.
---

# Bugfixing

Los bugs siguen la lógica de las tasks ([write-task](./write-task.md)) en `work/bugs/`, con las reglas de [develop-code](./develop-code.md). Para ejecutar pruebas y comandos lee [COMANDOS.md](../../COMANDOS.md) §2 (si falta uno, pregúntalo una vez y anótalo).

## Organización

| Elemento | Ruta |
|---|---|
| Bug | `work/bugs/bug-N-nombre/` (numeración consecutiva propia; archivados en `work/bugs/archive/`) |
| Resumen y decisiones | `work/bugs/bug-N-nombre/README.md` ([bug-README](../templates/bug-README.md)) |
| Unidad de trabajo | `work/bugs/bug-N-nombre/subtask-N-descripcion.md` ([bug-subtask](../templates/bug-subtask.md)) |
| Informes | `work/reports/bug-N-nombre/` |
| Changelogs | `work/changelogs/bug-N-nombre/` (solo si cambia código funcional) |

## Contenido obligatorio del brief

- **Síntoma** observado y **pasos para reproducirlo**.
- **Esperado frente a observado.**
- **Causa raíz** confirmada, o hipótesis marcada como tal.
- **Criterio de aceptación con prueba:** una prueba que falla antes del arreglo y pasa después.

## Reglas

- Corrige con el **cambio mínimo necesario**.
- No mezcles el arreglo con desarrollo de componentes nuevos; si exige funcionalidad nueva, abre una task aparte y enlázala.
- Si el bug revela un hecho que `docs/` documenta mal, corrige la página ([update-docs](./update-docs.md)).
- Al terminar: [close-session](./close-session.md).
