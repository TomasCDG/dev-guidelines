---
name: start-session
description: Retoma el trabajo al inicio de una sesión: resuelve la frase de entrada, lee solo lo necesario, verifica el repo real y confirma qué subtask toca. Úsala cuando el desarrollador diga «continúa task-N», «siguiente» o «bug-N», o adjunte un brief.
---

# Iniciar una sesión

Objetivo: que una frase baste para retomar sin re-explicar el estado. El estado sale de `INDEX.md` y se **verifica contra el repo**.

## 1. Frases de entrada

| El desarrollador dice | Cómo se resuelve |
|---|---|
| «continúa task-N» | Task N de `INDEX.md`: primera subtask `en curso` o, si no hay, la primera `pendiente` cuyas dependencias estén `hecha`. |
| «siguiente» | La task y subtask de «Activo ahora» en `INDEX.md`. Si está vacío, pregunta cuál (§5). |
| «subtask N de task-M» | Esa subtask, aunque `INDEX.md` indique otra. Verifica que sus dependencias estén hechas; si no, avisa y propón el orden. |
| «bug-N» | Igual que una task, en `work/bugs/bug-N-*/`; sigue además [fix-bug](./fix-bug.md). |
| Un brief adjunto (`subtask-N-*.md`) | Ese brief manda; contrasta su estado con `INDEX.md`. |

## 2. Qué leer (en este orden, y no más)

1. `AGENTS.md`, [PROJECT.md](../../PROJECT.md) (núcleo) y [DEV-PROFILE.md](../../DEV-PROFILE.md).
   - Un campo vacío (`—`) no es un aviso: no lo menciones. Usa el valor por defecto; si lo necesitas para el trabajo, pregúntalo una vez, propón un valor y anótalo en el archivo (§5).
   - [COMANDOS.md](../../COMANDOS.md) **no** se lee aquí: solo cuando vayas a escribir o probar código o a commitear.
2. [INDEX.md](../../INDEX.md): «Activo ahora» y la fila de la task.
3. `README.md` y `decisions.md` de la task.
4. El brief de la subtask y lo que cite (decisiones globales, restricciones, ADR).
5. El report de la subtask anterior («Siguiente paso», «Impacto en docs») y, si la subtask está `en curso`, su propio report parcial si existe.
6. Las páginas de `docs/` de las áreas que vas a tocar (índice: `docs/README.md`).
7. El playbook del trabajo que vas a hacer (tabla de `AGENTS.md`).

No leas `work/tasks/archive/`, `work/reports/` antiguos ni el resto de `work/tasks/` salvo que el brief lo cite.

## 3. Verificar el repo real

Ejecuta `git` (rama, `git status`, `git log` reciente) en cada repo de «Repos afectados» del brief (alias en `PROJECT.md` §1) y en `dev/` si está versionado. Comprueba que existen los archivos que el brief da por hechos. Confirma en **dos líneas** qué subtask harás y qué estado encontraste, y trabaja.

## 4. Si INDEX.md contradice al repo

Manda siempre el repo. Anota la corrección en el report («Decisiones y desviaciones»).

| Contradicción | Qué haces |
|---|---|
| Índice `pendiente`, pero el trabajo ya está en el repo (commits, archivos, report) | Trátala como `hecha`, corrige `INDEX.md` y el README de la task, y avanza a la siguiente. |
| Índice `hecha`, pero faltan archivos o código | Trátala como `en curso`, corrige el índice y repórtalo al inicio. |
| Índice y brief apuntan a subtasks distintas | Haz la del brief y deja constancia en el report. |
| Cambios sin commitear coherentes con la subtask `en curso` según `INDEX.md` (y su report parcial) | Se asumen propios: continúa sobre ellos. |
| Cambios sin commitear que no reconoces | No los toques ni los descartes; pregunta (§5). |
| Una dependencia del brief no está lista | No inventes su resultado: avisa y propón el orden. |

## 5. Preguntas

- Pregunta solo ante **contradicciones reales** o **decisiones del desarrollador** (comportamiento, alcance, arquitectura, datos, criterios de aceptación).
- **Una vez**, en un solo mensaje, concretas y con **un valor por defecto** que usarás si no hay respuesta.
- Detalles menores: decide, márcalo «decisión del agente» en el report y, si rige más allá de la subtask, regístralo con [record-decision](./record-decision.md).
- Un dato vacío de `PROJECT.md`, `COMANDOS.md` o `DEV-PROFILE.md` que necesitas: pregúntalo en ese momento, con valor propuesto, y escribe la respuesta en ese archivo.
- No pidas que re-expliquen lo que ya está en el brief, el README, `decisions.md`, `PROJECT.md` o `DEV-PROFILE.md`.

## 6. Durante el trabajo

- **Un solo escritor por archivo compartido.** Si otra subtask o sesión puede tocar los mismos archivos, no corren en paralelo.
- Antes de tocar un área, lee su página en `docs/`; si tu cambio altera lo documentado, actualízala en esta misma subtask ([update-docs](./update-docs.md)).
- Respeta las restricciones (`PROJECT.md` §3, README de la task) y las zonas intocables (`PROJECT.md` §4).
- Haz el cambio mínimo que cumple el brief; lo que queda fuera de alcance se anota, no se hace.
- Reglas de código y verificación: [develop-code](./develop-code.md).
- Al terminar: [close-session](./close-session.md).
