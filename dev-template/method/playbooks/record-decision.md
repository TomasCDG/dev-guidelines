---
name: record-decision
description: Registra decisiones por task con IDs y promueve a ADR global las que siguen vigentes tras cerrar la task. Úsala cuando se apruebe o se tome por defecto una decisión, o al cerrar una task con decisiones que seguirán rigiendo.
---

# Registrar decisiones

## 1. Decisiones de la task

Cada task tiene `decisions.md` ([decisions](../templates/decisions.md)), en `work/tasks/task-N-nombre/decisions.md`. Una fila por decisión:

| Campo | Contenido |
|---|---|
| ID | Con prefijo de la task: `T6-F1`, `T3-D4`. |
| Decisión | Una frase. |
| Motivo | Por qué, si no es obvio. |
| Fecha y quién | Desarrollador, o agente (valor por defecto a confirmar). |
| Estado | `vigente`, o `reemplazada por <ID>`. |

Los briefs y el README citan las decisiones por ID; no las copian ni las reexplican.

## 2. Promoción a ADR global

Una decisión se promueve cuando sigue rigiendo después de cerrar la task: **una task futura podría incumplirla sin saberlo**.

1. Crea `docs/decisions/ADR-NNN-nombre.md` con la plantilla [adr](../templates/adr.md). Numeración consecutiva única; una decisión por archivo, corto.
2. En `decisions.md` de la task marca la original como `promovida a ADR-NNN` y enlaza el ADR.
3. Si la decisión cambia el comportamiento documentado, actualiza las páginas de docs ([update-docs](./update-docs.md)).

## 3. Cuándo se registra

- **Del desarrollador:** al aprobarla, en la misma sesión.
- **Del agente** (detalle menor decidido por defecto): márcala «decisión del agente» en el report y regístrala solo si rige más allá de la subtask.
- Una decisión **reemplazada** no se borra: cambia su estado y enlaza la nueva.
