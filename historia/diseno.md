# Por qué el paquete es como es

**Fecha:** 27 de octubre de 2026

Resumen del análisis y el plan que originaron dev-guidelines, extraídos de un método de desarrollo agéntico usado en un «proyecto de origen» (sin su historial ni su contenido).

## Contenido

1. [Problemas de origen y decisión](#1-problemas-de-origen-y-decisión)
2. [Decisiones de diseño](#2-decisiones-de-diseño)
3. [Métodos externos consultados](#3-métodos-externos-consultados)

## 1. Problemas de origen y decisión

| # | Problema | Decisión |
|---|---|---|
| P1 | Lo genérico y lo específico de un stack iban mezclados | Núcleo genérico más `method/stacks/` opcionales, activados desde `COMANDOS.md` |
| P2 | El estado vivía en la memoria de la herramienta y en el prompt | `INDEX.md` con «Activo ahora» y estado por subtask; frase de entrada «continúa task-N» |
| P3 | Numeración con colisiones entre tasks | Una secuencia global `task-N` y `bug-N`; el número de una task archivada no se reutiliza |
| P4 | Nombres inconsistentes (mayúsculas, idiomas) | Convención única, `check.py` la verifica |
| P5 | Duplicados y carpetas sueltas | `check.py` y reglas de archivo (`archive/`) |
| P6 | Reglas de cierre dispersas y contradictorias | Una lista única de cierre en `close-session` |
| P7 | Sin protocolo de inicio | `start-session`: lista mínima de lectura y verificación del repo real |
| P8 | Sin configuración del proyecto | `PROJECT.md` y `COMANDOS.md` |
| P9 | Decisiones sin registro propio | `decisions.md` por task con promoción a ADR global |
| P10 | Report, changelog y docs se solapaban | El changelog se deriva del report; lo estable se promueve a `docs/` |
| P11 | Enlaces al código con rutas relativas frágiles | Alias `@repo/` declarados en `PROJECT.md` |
| P12 | Briefs largos y con restricciones copiadas a mano | Restricciones por ID y plantillas con comentarios |

## 2. Decisiones de diseño

- **Español** para guías y plantillas; el idioma de docs y UI de cada proyecto se declara en `PROJECT.md`.
- **Changelog derivado del report:** una sola tabla «qué cambió», copiada con fecha.
- **Sin historial migrado:** al paquete solo llegan reglas y plantillas genéricas; el trabajo antiguo del proyecto de origen queda donde estaba.
- **`dev/` es su propio repo en multirepo (modo B)** y se excluye localmente en modo A.
- **`DEV-PROFILE.md` es personal y no se versiona**; `PROJECT.md` es del proyecto. Se separa por quién cambia el dato.
- **Decisiones por task** (`T6-F1`) y promoción a ADR cuando una task futura podría incumplirlas sin saberlo.
- **Dos capas:** playbooks portables en markdown y adaptadores (skills, reglas, hook) generados desde ellos, sin duplicar contenido.
- **Divulgación progresiva:** `AGENTS.md` enrutador corto, playbooks de una sola situación y plantillas bajo demanda; el presupuesto de líneas lo vigila `check.py`.
- **Alias `@repo/`** para que el mismo `dev/` sirva en modo A y B.
- **Estados de subtask** `pendiente`, `en curso`, `hecha` y `hecha (commit <hash>)`.
- **Verificador `check.py`:** estructura, numeración, enlaces, alias, fechas, presupuesto y adaptadores.
- **Instalación determinista** con la skill `dev-setup`, actualización con `dev-update` y diagnóstico con el agente `dev-doctor`; el copiado lo hace un script, no el agente.
- **Estructura `work/` · `docs/` · `method/`:** lo del equipo, la verdad técnica y lo que el paquete reemplaza.
- **`PROJECT.md` y `DEV-PROFILE.md` mínimos** con «pregunta en el momento»: un campo vacío (`—`) no es un aviso.
- **Versión y `MIGRATIONS.md`:** cada proyecto sabe qué versión tiene y cómo adaptar sus archivos al actualizar.
- **Retro por proyecto** (0.7.0): cada `dev/` guarda sus retros y la skill `dev-feedback` las convierte en propuestas para el paquete.

## 3. Métodos externos consultados

| Método | Qué se tomó |
|---|---|
| AGENTS.md | Un archivo de entrada estándar que lee cualquier herramienta; aquí es un enrutador corto |
| Agent Skills | Playbooks con `name` y `description` que se cargan solo cuando la situación lo pide |
| CLAUDE.md y reglas por ruta | `CLAUDE.md` con `@AGENTS.md` y reglas `paths:` que activan el playbook al tocar `work/` o `docs/` |
| Spec Kit | Especificación antes de implementar: el brief autocontenido de cada subtask |
| Kiro | Tareas con requisitos y aceptación explícitos |
| OpenSpec | Cambios propuestos y archivados: de ahí `archive/` para lo cerrado |
| BMAD | Roles y artefactos por etapa; se tomó la idea de documentos de traspaso, no los roles |
| Cursor rules | Reglas `.mdc` por ruta, generadas como adaptador |
| Cline Memory Bank | Un estado vivo que permite retomar sin memoria: `INDEX.md` |
| Aider | Convenciones del repo leídas al inicio y mensajes de commit con política explícita |
| MADR | Formato corto de decisiones con alternativas y consecuencias: la plantilla de ADR |
| Hooks de Claude Code | El hook `SessionStart` opcional que inyecta «Activo ahora» |
