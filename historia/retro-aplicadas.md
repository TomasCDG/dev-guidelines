# Retros aplicadas

**Fecha:** 27 de octubre de 2026

Registro de las mejoras al paquete que llegaron por retro. Se alimenta así: cada proyecto anota sus retros en `dev/RETRO.md`; las filas que el desarrollador lleva al paquete (estado `enviada`) y que ya están aplicadas se anotan aquí, con la versión en que salieron. El detalle de cada versión está en [CHANGELOG.md](../release/CHANGELOG.md).

| Fecha | Origen (proyecto/task) | Qué se detectó | Cambio aplicado | Versión |
|---|---|---|---|---|
| 2026-10-26 | Prueba de humo con `examples/mini-proyecto` | «continúa task-1» abre la subtask correcta, pero hubo 13 fricciones: ejemplo sin `bugs/` ni plantilla de docs; estados de subtask sin commit; `PROJECT.md` con `TODO` sin regla; report parcial no leído; repo a verificar en multirepo; ubicación de capturas; listas de inicio duplicadas | Estados de subtask con commit, `TODO` como aviso, lista única de inicio y de cierre, carpeta de capturas, validaciones en `check.py` y ejemplo completado | 0.1.0 |
| 2026-10-26 | Investigación de métodos externos (AGENTS.md, Agent Skills, reglas por ruta, OpenSpec, Kiro, Cline, MADR) | El inicio obligatorio pesaba ~20 KB y las guías largas se leían enteras; sin respaldo si una regla no se activa; sin forma de comprobar el presupuesto de tokens | `AGENTS.md` enrutador, playbooks por situación, `archive/`, adaptadores y hook generados desde una fuente, lint de presupuesto en `check.py` | 0.2.0 |
