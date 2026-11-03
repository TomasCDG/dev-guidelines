# Retros aplicadas

**Fecha:** 27 de octubre de 2026

Registro de las mejoras al paquete que llegaron por retro. Se alimenta así: cada proyecto anota sus retros en `dev/work/RETRO.md`; las filas que el desarrollador lleva al paquete (estado `enviada`) y que ya están aplicadas se anotan aquí, con la versión en que salieron. El detalle de cada versión está en [CHANGELOG.md](../release/CHANGELOG.md).

| Fecha | Origen (proyecto/task) | Qué se detectó | Cambio aplicado | Versión |
|---|---|---|---|---|
| 2026-10-26 | Prueba de humo con `examples/mini-proyecto` | «continúa task-1» abre la subtask correcta, pero hubo 13 fricciones: ejemplo sin `bugs/` ni plantilla de docs; estados de subtask sin commit; `PROJECT.md` con `TODO` sin regla; report parcial no leído; repo a verificar en multirepo; ubicación de capturas; listas de inicio duplicadas | Estados de subtask con commit, `TODO` como aviso, lista única de inicio y de cierre, carpeta de capturas, validaciones en `check.py` y ejemplo completado | 0.1.0 |
| 2026-10-26 | Investigación de métodos externos (AGENTS.md, Agent Skills, reglas por ruta, OpenSpec, Kiro, Cline, MADR) | El inicio obligatorio pesaba ~20 KB y las guías largas se leían enteras; sin respaldo si una regla no se activa; sin forma de comprobar el presupuesto de tokens | `AGENTS.md` enrutador, playbooks por situación, `archive/`, adaptadores y hook generados desde una fuente, lint de presupuesto en `check.py` | 0.2.0 |
| 2026-10-27 | Instalación en modo B, workspace multirepo | Las herramientas del entorno (servicios locales, MCP, cómo probar en vivo) no tenían lugar versionado y terminaban en `DEV-PROFILE.md` | `config/ENTORNO.md`, leído en cada sesión y copiado en los briefs por etapa | 0.8.0 |
| 2026-10-27 | task-33 (redacción de task) | El agente ofrecía commitear archivos de `dev/` (planificación, no producto) | Commits solo por código del proyecto en `AGENTS.md`, `commit-pr` y `close-session` | 0.8.0 |
| 2026-10-28 | Stacks | `typescript-react.md` mezclaba reglas técnicas con cómo explicar a quien no conoce la tecnología | Packs solo técnicos; la regla de explicar pasa a `develop-code` §4 | 0.8.0 |
| 2026-10-28 | Mapas del método | No había un lugar que mostrara cómo fluye la lógica ni qué contexto se lee en cada paso | `method/MAPA.md` con cuatro mapas y aviso en `check.py` | 0.8.0 |
| 2026-10-29 | task-34 (cierre) | Un valor de referencia del brief estaba mal y solo se vio al recalcular; las pruebas contra el chat eran lentas y manuales | Recalcular las referencias en `write-task` §4 y la plantilla `subtask`; fila «Script de pruebas» en `ENTORNO.md` §2 (el script es del proyecto) | 0.8.0 |
| 2026-11-02 | task-34 (informe para la call) | El informe técnico era ilegible para un equipo no técnico; funcionó una matriz «qué se puede hacer» con ✅ ⚠️ ❌ | `write-report` §5 y plantilla `report-funcional.md` | 0.8.0 |
| 2026-11-02 | Proyecto del desarrollador (pedido perdido) | Demasiadas subtasks: cambios chicos en sesiones distintas disparan los tokens | `write-task` §5: mínimo sin comprometer comprobabilidad ni stacks, corte D6, regla «sin goteo» y chequeo de fusión con costo estimado | 0.8.0 |
