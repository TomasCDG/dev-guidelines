# RETRO — mejoras al método

Retro de este proyecto: al cerrar una task se añade una fila `pendiente` (playbook `close-session` §3). Cuando haya varias, pide «feedback del método» (skill `dev-feedback`). Es un archivo del proyecto: el instalador nunca lo pisa.

Estados: `pendiente` (sin procesar), `propuesta` (feedback ya redactado en `.feedback/`), `enviada` (el desarrollador la llevó al paquete), `descartada` (añade el motivo en «Qué cambiarías»).

| Fecha | Task o bug | Qué funcionó | Qué falló o sobró | Qué cambiarías | Estado |
|---|---|---|---|---|---|
| 2026-10-26 | task-1 (ficticia) | «continúa task-1» abre la subtask correcta | El report parcial no se mencionaba al retomar | Citar el report parcial en start-session | pendiente |
