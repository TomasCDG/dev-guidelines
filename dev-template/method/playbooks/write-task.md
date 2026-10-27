---
name: write-task
description: Investiga, divide y redacta una task con su README y sus briefs de subtask autocontenidos. Úsala cuando haya que planificar un desarrollo nuevo, crear o modificar subtasks, o actualizar el estado de una task.
---

# Redactar tasks y subtasks

Una subtask debe poder iniciarse en una sesión independiente («continúa task-N») sin que el agente recuerde conversaciones anteriores. El **brief** es el traspaso. Vocabulario: **task** = carpeta con el plan completo; **subtask** = cada markdown dentro (una sesión de trabajo).

## Contenido

1. [Antes de escribir](#1-antes-de-escribir)
2. [Organización](#2-organización-e-identificación)
3. [README de la task y estados](#3-readme-de-la-task-y-estados)
4. [Contenido de cada brief](#4-contenido-de-cada-brief)
5. [Preservar el contexto](#5-preservar-el-contexto)

## 1. Antes de escribir

1. **Entender la solicitud:** resultado final, motivo, restricciones, exclusiones y quién aprueba qué.
2. **Investigar el estado real:** código, docs, pruebas. Separa hechos verificados de propuestas y supuestos; no conviertas una idea en decisión sin confirmación.
3. **Mapear el trabajo completo:** entregables, dependencias reales, qué avanza en paralelo, qué documentación necesitarán los siguientes agentes.
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
- **Tabla de subtasks:** número, enlace, tipo, resultado, esfuerzo, modelo sugerido, dependencias y **estado**.
- Diagrama de dependencias y qué corre en paralelo (solo si no edita los mismos archivos).
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
6. **Trabajo:** pasos concretos, empezando por inspeccionar el código y las fuentes.
7. **Criterios de aceptación y verificación:** resultados observables y comprobables (comportamiento, errores, pruebas, verificación manual o visual, enlaces si es documental). Verifican el requisito original, no que «se ejecutó un comando».
8. **Dependencias y siguiente paso:** qué debe estar hecho antes (comprueba su estado, no inventes el resultado), qué desbloquea, qué corre en paralelo.
9. **Fuera de alcance.**
10. **Impacto en docs:** tabla `página → cambio esperado`, o «ninguno» con motivo.
11. **Entregables y cierre:** rutas de report, docs, changelog y código; el cierre sigue [close-session](./close-session.md).

Metadatos recomendados: tipo (marco, funcionalidad, endurecimiento, investigación), esfuerzo (S horas · M un día · L varios días), modelo sugerido. Un bug usa [bug-subtask](../templates/bug-subtask.md) ([fix-bug](./fix-bug.md)).

## 5. Preservar el contexto

- **Autocontenido en lo crítico:** decisiones, restricciones, alcance y objetivo local escritos en el brief.
- **Conserva el antes y el después** y cómo conecta con tareas previas y posteriores.
- **No delegues el contexto a docs que no existen:** si hacen falta, crea una subtask previa que los produzca.
- **Tareas enfocadas:** un resultado coherente, revisable y verificable en una sesión; divide por resultados utilizables, no por capas técnicas.
- **Nada fuera de alcance como tarea implícita:** exclúyelo expresamente. Las decisiones del desarrollador se formulan como preguntas o puntos de aprobación.
- **Endurecimiento al final:** pruebas exhaustivas y limpieza de docs pueden ser la última subtask, pero el núcleo mínimo de pruebas y la actualización de docs de cada cambio van en su propia subtask.
