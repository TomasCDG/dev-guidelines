---
name: write-task
description: Investiga y redacta una task (una subtask salvo criterio de corte) con su README y sus briefs de subtask autocontenidos. Úsala cuando haya que planificar un desarrollo nuevo, crear o modificar subtasks, o actualizar el estado de una task.
---

# Redactar tasks y subtasks

Una subtask debe poder iniciarse en una sesión independiente («continúa task-N») sin que el agente recuerde conversaciones anteriores. El **brief** es el traspaso. Vocabulario: **task** = carpeta con el plan completo; **subtask** = cada markdown dentro (una unidad entregable; puede ocupar varias sesiones con report parcial). **Por defecto una task tiene una sola subtask** (§5).

## Contenido

1. [Antes de escribir](#1-antes-de-escribir)
2. [Organización](#2-organización-e-identificación)
3. [README de la task y estados](#3-readme-de-la-task-y-estados)
4. [Contenido de cada brief](#4-contenido-de-cada-brief)
5. [Cuándo dividir](#5-cuándo-dividir)
6. [Preservar el contexto](#6-preservar-el-contexto)

## 1. Antes de escribir

1. **Entender la solicitud:** resultado final, motivo, restricciones, exclusiones y quién aprueba qué.
2. **Investigar el estado real:** código, docs, pruebas, con las herramientas de `ENTORNO.md` §1 para `planificar` e `investigar`. Separa hechos verificados de propuestas y supuestos; no conviertas una idea en decisión sin confirmación.
3. **Mapear el trabajo completo:** entregables, dependencias reales, qué documentación necesitarán los siguientes agentes. No busques cortes: divide solo con un criterio de §5.
4. **Cerrar ambigüedades importantes:** pregunta si una decisión cambia comportamiento, alcance, arquitectura, datos o criterios de aceptación; para detalles menores, propón un valor por defecto marcado «decisión del agente».
5. Lee [update-docs](./update-docs.md) (qué va en docs y qué no) y [develop-code](./develop-code.md) si el brief fija criterios de código.

No asumas que un agente futuro tendrá esta investigación: incluye en el brief lo que deba sobrevivir al traspaso.

## 2. Organización e identificación

- Una carpeta por task: `work/tasks/task-N-nombre/`. **Numeración única por proyecto**, sin reiniciar ni reutilizar números (tampoco los de `work/tasks/archive/`).
- Subtasks: `subtask-N-descripcion.md`, consecutivas dentro de la task.
- Material de origen del brief (capturas, ejemplos): `work/tasks/task-N-nombre/assets/`. Evidencia de un report: `work/reports/task-N-nombre/assets/`.
- El número ordena pero **no sustituye las dependencias**: no infieras que algo está hecho por su número; verifica el repo.

## 3. README de la task y estados

Plantilla: [task-README](../templates/task-README.md). Contiene:

- Objetivo, origen y estado de la task (con fecha).
- **Tabla de subtasks:** número, enlace, tipo, resultado, esfuerzo, modelo sugerido, dependencias, **corte** (criterio de §5 que la justifica; `—` en la primera) y **estado**.
- Diagrama de dependencias, solo si hay más de una subtask.
- Restricciones de la task (IDs) y referencia a las del proyecto (`PROJECT.md` §3).
- «Qué necesita del desarrollador»: cada ítem con el **valor por defecto** que el agente usa mientras tanto.
- Backlog (fuera de alcance, no redactado) y entregables compartidos.

| Estado de subtask | Significado |
|---|---|
| `pendiente` | No iniciada. |
| `en curso` | Iniciada; puede tener report parcial. |
| `hecha` | Cerrada, sin commit todavía. |
| `hecha (commit <hash>)` | El desarrollador commiteó; se rellena el hash. |

Estado de task (en `INDEX.md`): `borrador`, `en curso`, `pausada`, `hecha (archivada)`. Decisiones de la task: [record-decision](./record-decision.md).

## 4. Contenido de cada brief

Plantilla: [subtask](../templates/subtask.md). Secciones en orden; quita solo las que claramente no correspondan.

1. **Título e instrucciones para la sesión:** qué leer (README de la task, reports previos, docs del área) y recordar verificar el repo.
2. **Objetivo y lugar en el resultado final.**
3. **Historia de usuario** (si ayuda): «Como [rol], quiero [capacidad], para [beneficio]».
4. **Contexto y decisiones aprobadas:** estado actual, problema, fuentes canónicas (`@repo/ruta`), decisiones por ID, supuestos y preguntas abiertas. Explica los términos esenciales según la fila «Tecnologías que NO conozco» de `DEV-PROFILE.md`.
5. **Alcance, límites y exclusiones:** qué hacer y qué no, **repos afectados**, archivos intactos. Cita las restricciones por ID y repite en una línea las críticas.
6. **Trabajo:** pasos concretos, empezando por inspeccionar el código y las fuentes. Copia de [ENTORNO.md](../../config/ENTORNO.md) las herramientas y servicios de las etapas que recorre la subtask (con su URL o nombre) y las reglas `E…` que apliquen; el brief no debe depender de que alguien recuerde que existen.
7. **Criterios de aceptación y verificación:** resultados observables y comprobables (comportamiento, errores, pruebas, verificación manual o visual, enlaces si es documental). Verifican el requisito original, no que «se ejecutó un comando». **Recalcula cada valor de referencia** (cifra, conteo, mediana) contra la fuente antes de copiarlo, y anota cómo se obtuvo (consulta, script, fecha); si no pudiste recalcularlo, márcalo «sin verificar». Si `ENTORNO.md` §2 tiene un script de pruebas en vivo, cítalo.
8. **Dependencias y siguiente paso:** qué debe estar hecho antes (comprueba su estado, no inventes el resultado), qué desbloquea, qué corre en paralelo.
9. **Fuera de alcance.**
10. **Impacto en docs:** tabla `página → cambio esperado`, o «ninguno» con motivo.
11. **Entregables y cierre:** rutas de report, docs, changelog y código; el cierre sigue [close-session](./close-session.md).

Metadatos recomendados: tipo (marco, funcionalidad, endurecimiento, investigación), esfuerzo (S horas · M un día · L varios días), modelo sugerido. Un bug usa [bug-subtask](../templates/bug-subtask.md) ([fix-bug](./fix-bug.md)).

## 5. Cuándo dividir

Cada subtask cuesta un brief, un report, un changelog, un cierre y releer el contexto (unos 12 000 tokens). **Apunta al mínimo de subtasks que no comprometa los demás criterios:** cada una comprobable por sí sola, stacks separados cuando lo pidan (D6) y los cortes de abajo. **Por defecto, una sola subtask.** Corta solo si se cumple al menos uno de estos criterios, y anótalo en la columna «Corte»:

| ID | Criterio |
|---|---|
| D1 | **Tamaño:** esfuerzo L, más de unos 15 archivos o lecturas necesarias que ocupan más de la mitad del contexto. |
| D2 | **Entregas independientes:** repos o despliegues que se publican por separado (varios repos en un mismo cambio no bastan). |
| D3 | **Aprobación a mitad:** el desarrollador debe aprobar algo que cambia el resto (fila bloqueante de «Qué necesita del desarrollador»). |
| D4 | **Riesgo:** migración de datos, zona intocable de `PROJECT.md` §4 o cambio irreversible que pide commit y revisión aparte. |
| D5 | **Investigación:** su resultado decide el plan restante. |
| D6 | **Stack distinto:** el cambio cruza stacks con packs distintos de `method/stacks/` (por ejemplo Swift y React) que no conviene cargar en la misma sesión. Las capas de un mismo stack no cuentan. |

- **No justifican un corte:** las capas técnicas de un mismo stack, las pruebas o docs del cambio, el paralelismo deseable ni el tipo de subtask. Van dentro de la misma subtask.
- **Sin goteo:** cambios chicos y parecidos (cada botón, cada texto, cada pantalla con el mismo patrón) van juntos en una subtask, con una tabla de ítems en «Trabajo» y un criterio de aceptación por ítem; nunca uno por sesión.
- **Número mínimo:** subtasks = cortes justificados + 1. Con más de 3, añade al README un párrafo «Por qué N».
- **Antes de pedir aprobación:** por cada par de subtasks contiguas, pregúntate si podrías fusionarlas sin romper D1–D6 ni la comprobabilidad; si sí, fusiónalas. Muestra en el plan el costo estimado (subtasks × unos 12 000 tokens).
- **Si a mitad resulta grande:** deja un report parcial y sigue `en curso` en otra sesión. Solo si lo que queda es un resultado separable, cierra la subtask como `hecha` con el alcance reducido y crea `subtask-(N+1)` con un brief corto que remite al report.

## 6. Preservar el contexto

- **Autocontenido en lo crítico:** decisiones, restricciones, alcance y objetivo local escritos en el brief.
- **Conserva el antes y el después** y cómo conecta con tareas previas y posteriores.
- **No delegues el contexto a docs que no existen:** si hacen falta, el brief incluye producirlos como primer paso.
- **Tareas enfocadas:** un resultado coherente y revisable; si divides, por resultados utilizables, no por capas técnicas.
- **Nada fuera de alcance como tarea implícita:** exclúyelo expresamente. Las decisiones del desarrollador se formulan como preguntas o puntos de aprobación.
- **Pruebas y docs en la misma subtask:** el núcleo mínimo de pruebas y la actualización de docs van con el cambio; la matriz completa de pruebas también, si el brief la pide en sus criterios de aceptación.
