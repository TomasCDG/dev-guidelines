---
name: commit-pr
description: Redacta el mensaje de commit sugerido de una subtask y el informe de PR de una task, según la política del proyecto. Úsala cuando cierres una subtask (mensaje de commit), cierres una task (informe de PR) o el desarrollador pida commitear.
---

# Commits y pull requests

Lee [COMANDOS.md](../../COMANDOS.md) §3 (formato, cuándo commitear, un commit por subtask o task, informe de PR). Si falta algo (`—`), pregúntalo una vez con un valor propuesto y anótalo allí. La atribución de IA sigue la fila «Atribución de IA» de `DEV-PROFILE.md`; por defecto, ninguna.

- Al cerrar una **subtask**, incluye en el report un **mensaje de commit** conciso y multilínea: tipo (`feat`, `fix`, `refactor`, `docs`, `test`…), resumen y lista breve de cambios. Plantilla: [commit](../templates/commit.md).
- Al cerrar una **task** (no una subtask), redacta un informe de PR breve que reúna los cambios funcionales, a partir de los changelogs. Plantilla: [pr](../templates/pr.md).
- **No hagas commit** salvo que `COMANDOS.md` §3 o el desarrollador lo indiquen. Cuando commitea, anota el hash en el estado de la subtask (`hecha (commit <hash>)`, ver [write-task](./write-task.md) §3).
- **Multirepo:** un commit por repo afectado, con el mismo ID de task en el mensaje.
