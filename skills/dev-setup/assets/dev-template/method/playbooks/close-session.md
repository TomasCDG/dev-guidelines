---
name: close-session
description: Cierra una subtask o una task con la lista única de cierre: report, docs, changelog, estados, INDEX, decisiones, mensaje de commit y archivo de la task. Úsala cuando termines o interrumpas una subtask, o cuando se cierre la última subtask de una task.
---

# Cerrar una sesión

## 1. Lista única de cierre (subtask)

Comprueba cada punto; el report debe poder responder a todos.

| # | Acción | Dónde |
|---|---|---|
| 1 | Verificación hecha y limitaciones (pruebas, ejecución real, lo que no se pudo comprobar) | Report |
| 2 | Report con **Impacto en docs** y **Siguiente paso** | `work/reports/<task>/subtask-N-*.md` ([write-report](./write-report.md)) |
| 3 | Docs actualizados (o «ninguno» con motivo), con fecha y «Verificado contra» de cada página tocada, también en `docs/README.md` | `docs/` ([update-docs](./update-docs.md)) |
| 4 | Changelog, solo si cambió código funcional | `work/changelogs/<task>/subtask-N-*.md` |
| 5 | Estado de la subtask en el README de la task: `hecha` (sin commit todavía). Cuando el desarrollador commitea, `hecha (commit <hash>)`. Estados: [write-task](./write-task.md) §3 | `work/tasks/<task>/README.md` |
| 6 | `INDEX.md`: «Activo ahora», fila de la task o bug, fecha de actualización | `INDEX.md` |
| 7 | Decisiones nuevas ([record-decision](./record-decision.md)) y filas resueltas de «Qué necesita del desarrollador» marcadas con la respuesta | `decisions.md` / `docs/decisions/` / README de la task |
| 8 | Mensaje de commit sugerido, con ID de task (un mensaje por repo en multirepo) | Report ([commit-pr](./commit-pr.md)) |
| 9 | Preguntas abiertas y desviaciones comunicadas al desarrollador | Respuesta final |

## 2. Subtask que no cierra

Déjala `en curso`, escribe un **report parcial** con lo hecho y lo que falta, y deja ese punto como «Siguiente paso». Actualiza «Activo ahora» con el estado exacto. La sesión siguiente lo lee ([start-session](./start-session.md) §2).

## 3. Cierre de una task

Cuando se cierra la última subtask:

1. Limpieza final de las páginas de `docs/` afectadas: sin notas provisionales, «verificado contra» al día.
2. Informe de PR de la task ([commit-pr](./commit-pr.md)).
3. Promoción a `docs/decisions/` de las decisiones que siguen vigentes ([record-decision](./record-decision.md)).
4. **Retro de 3 líneas** como una fila nueva en [RETRO.md](../../RETRO.md) con estado `pendiente`: qué funcionó, qué falló o sobró, qué cambiarías del método. Marca «Retro pendiente: sí» en `INDEX.md`; pasa a «no» cuando la retro se procesa (`propuesta` o `descartada`, skill `dev-feedback`).
5. **Archivar:** mueve `work/tasks/task-N-nombre/` a `work/tasks/archive/task-N-nombre/` (un bug, a `work/bugs/archive/`). Corrige los enlaces entrantes (reports, changelogs, docs, decisions): busca el nombre de la carpeta con `grep`. Reports y changelogs no se mueven.
6. En `INDEX.md`: pasa la task a `hecha (archivada)` con su ruta nueva y vacía «Activo ahora» o apúntalo a la siguiente.

El número de una task archivada no se reutiliza.
