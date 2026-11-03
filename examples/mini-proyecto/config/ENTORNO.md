# ENTORNO — herramientas y entorno de trabajo

Versionado y común a todo el equipo; lo lee el agente en cada sesión, porque las herramientas sirven en todas las etapas de una task, no solo al programar. Comandos de consola: [COMANDOS.md](./COMANDOS.md). Lo de tu máquina (WSL, rutas propias): [DEV-PROFILE.md](./DEV-PROFILE.md). `—` = sin definir. Una fila por herramienta: si crece, resume.

## 1. Herramientas y servicios

Etapas: `planificar` · `investigar` · `desarrollar` · `probar` · `revisar`.

| Herramienta o servicio | Para qué usarla | Etapas | Cómo (URL, nombre del MCP, comando) |
|---|---|---|---|
| API local | Probar endpoints y ver el esquema OpenAPI | investigar, probar, revisar | http://127.0.0.1:8000/docs |
| Front local | Ver el cambio en pantalla | probar, revisar | http://localhost:5173 |
| Búsqueda de código | Localizar símbolos y llamadas antes de abrir archivos | planificar, investigar, desarrollar | `rg` desde la raíz del workspace (no hay MCP) |

## 2. Cómo probar en vivo

| Paso | Detalle |
|---|---|
| Levantar | API y front con «Ejecutar en desarrollo» de `COMANDOS.md` §2, cada uno en su terminal |
| Dónde mirar | Lista de tareas en http://localhost:5173; respuestas de la API en `/docs` |
| Datos de prueba | La API arranca vacía; crea 3 o 4 tareas desde `/docs` (`POST /tasks`) |
| Qué no tocar | — |

## 3. Reglas de uso

Valen en cualquier etapa; se citan como `E1`…

| ID | Regla |
|---|---|
| E1 | Verifica en pantalla todo cambio de `@front` antes de cerrar la subtask; si no puedes levantarlo, dilo en el report |
