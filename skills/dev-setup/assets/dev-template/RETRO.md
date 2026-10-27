# RETRO — mejoras al método

Retro de este proyecto: al cerrar una task se añade una fila `pendiente` ([close-session](./method/playbooks/close-session.md) §3). Cuando haya varias, pide «feedback del método» (skill `dev-feedback`) para convertirlas en propuestas de cambio al paquete. Es un archivo del proyecto: el instalador nunca lo pisa.

Estados: `pendiente` (sin procesar), `propuesta` (feedback ya redactado en `.feedback/`), `enviada` (el desarrollador la llevó al paquete), `descartada` (añade el motivo en «Qué cambiarías»).

<!-- Ejemplo: | 2026-10-27 | task-3 | Los briefs se retoman sin contexto | El INDEX queda desactualizado al pausar | Pedir el INDEX en el cierre parcial | pendiente | -->

| Fecha | Task o bug | Qué funcionó | Qué falló o sobró | Qué cambiarías | Estado |
|---|---|---|---|---|---|
| — | — | — | — | — | — |
