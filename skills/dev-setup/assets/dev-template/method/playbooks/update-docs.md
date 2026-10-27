---
name: update-docs
description: Decide dónde va cada tipo de conocimiento y crea o actualiza páginas de docs técnicos con su cabecera de frescura. Úsala cuando vayas a tocar un área documentada, cambies un comportamiento, descubras un hecho estable o cierres un cambio funcional.
---

# Docs técnicos (`docs/`)

Fuente de verdad sobre el **estado actual** del sistema, para agentes y desarrolladores; distinta de la documentación oficial del proyecto. Solo hechos **verificables** contra el código. Todo `docs/` se indexa en [docs/README.md](../../docs/README.md): una página que no está en el índice no existe para el agente.

## Contenido

1. [Dónde va cada cosa](#1-dónde-va-cada-cosa)
2. [Qué NO va en docs](#2-qué-no-va-en-docs)
3. [Categorías y formato](#3-categorías-y-formato)
4. [Disparadores](#4-disparadores)
5. [Frescura](#5-frescura)
6. [Impacto en docs](#6-impacto-en-docs)

## 1. Dónde va cada cosa

| Tipo de conocimiento | Dónde va |
|---|---|
| Estado y comportamiento actual del sistema | `docs/<categoría>/` |
| Decisión que rige una task / todo el proyecto | `work/tasks/task-N/decisions.md` / `docs/decisions/` ([record-decision](./record-decision.md)) |
| Cómo operar el proyecto | `docs/runbook/` (comandos generales: `COMANDOS.md`) |
| Cómo ejecutar en **esta** máquina (WSL, rutas, puertos) | Una página de `docs/runbook/` |
| Vocabulario del dominio | `docs/glossary.md` |
| Deuda técnica, pendientes, ideas | `INDEX.md` (backlog) |
| Historia, análisis, evidencia | `work/reports/` ([write-report](./write-report.md)) |
| Plan y alcance | `work/tasks/` ([write-task](./write-task.md)) |
| Cambios de código por entrega | `work/changelogs/` |

Si un dato encaja en dos filas, escríbelo donde se mantiene vigente y enlázalo desde la otra.

## 2. Qué NO va en docs

- Planes, roadmaps, pendientes, reflexiones, hipótesis sin verificar, «podríamos…».
- Notas de sesión o historial de qué se hizo (eso es del report y de git).
- Instrucciones dirigidas al agente («ahora haz…») y preferencias de una persona o máquina.
- Código copiado que se puede leer en el repo: enlaza con `@repo/ruta:línea`.

## 3. Categorías y formato

| Categoría | Contenido |
|---|---|
| `architecture/` | Estructura, módulos, flujos de datos, límites entre componentes. |
| `business_logic/` | Reglas de negocio y de dominio: qué calcula el sistema y con qué criterios. |
| `contracts/` | API, formatos de archivo, mensajes, esquemas. |
| `runbook/` | Puesta en marcha, despliegue, diagnóstico de fallos comunes. |

- Subcarpetas por tema cuando haya varias páginas. Una categoría nueva se consulta con el desarrollador (no crees `notas/` ni similares).
- Plantilla: [_page-template](../../docs/_page-template.md). Markdown, tablas, conciso, en el idioma de `PROJECT.md` §2.
- Cabecera: **fecha**, **estado** (`vigente` u `obsoleta`), **verificado contra** (commit o fecha) e índice anidado.
- Una página, un tema; si crece más de lo que se lee de una vez, divídela y actualiza el índice.

## 4. Disparadores

| Disparador | Acción obligatoria |
|---|---|
| Vas a tocar el código de un área | Lee su página (búscala en el índice). Si no existe, anótalo en el report como hueco. |
| El brief cita una página | Léela entera antes de planificar. |
| Tu subtask cambia un comportamiento, contrato o regla documentada | Actualiza la página **en esa misma subtask**. |
| Tu subtask crea un componente, contrato o regla sin página | Crea la página y regístrala en `docs/README.md`. |
| El código no coincide con la página | Manda el código: corrige la página (o márcala `obsoleta`) y avísalo en el report. |
| Un report contiene un hecho estable y reutilizable | Pásalo a docs y deja en el report solo el enlace. |
| Se cierra una task | Revisa las páginas tocadas: quita notas provisionales y refresca «verificado contra». |

Si eliminas una página, quítala del índice y corrige los enlaces.

## 5. Frescura

- Al editar o revisar una página, refresca fecha y «verificado contra»; el índice refleja ambos y el estado.
- Si sospechas que describe algo ya cambiado y no puedes verificarlo, márcala `obsoleta` con una línea que diga qué parte dudas; no la borres en silencio.
- Una página `obsoleta` no es fuente de verdad: contrástala con el código antes de usarla, y corrígela o elimínala, no la dejes indefinida.

## 6. Impacto en docs

Todo brief y todo report incluye la sección **Impacto en docs**: tabla `página → cambio → tipo` (`actualizar` / `crear`) o «ninguno» con el motivo. En el brief es lo **esperado**; en el report, lo **realizado** con desviaciones. Una subtask que cambia comportamiento y declara «ninguno» sin motivo no está cerrada.

Antes de cerrar: ¿las páginas tocadas están en el índice, con cabecera al día y sin contenido de la sección 2?
