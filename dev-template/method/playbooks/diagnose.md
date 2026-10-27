---
name: diagnose
description: Diagnostica la salud de dev/ ejecutando check.py y leyendo sus resultados junto con INDEX.md y las tasks. Úsala cuando el desarrollador pida revisar, auditar o diagnosticar dev/, al cerrar una task, tras actualizar el paquete o si algo parece inconsistente.
---

# Diagnóstico de salud de dev/

Solo lee y propone: **no modifiques nada** hasta que el desarrollador apruebe los arreglos.

## 1. Ejecutar el verificador

```bash
python -I dev/.tools/check.py dev --json
```

- En modo B la ruta es `dev/` dentro del workspace; ajusta el directorio actual si hace falta.
- Si `dev/.tools/check.py` no existe, la instalación es anterior al diagnóstico: dilo y propón actualizar con la skill `dev-setup`.
- Si no hay Python que funcione, haz solo la revisión manual del §3 y avisa de que falta la parte automática.
- Añade `--strict` solo si el desarrollador lo pide (convierte los `TODO` literales y los excesos de presupuesto en errores).

La salida es JSON: `errors` y `warnings` (listas de `{where, msg}`), `counts` y `root`.

## 2. Interpretar los hallazgos

| Hallazgo | Causa probable | Arreglo propuesto |
|---|---|---|
| Falta archivo, carpeta o playbook | Instalación incompleta o borrado accidental | Actualizar con `dev-setup` (no pisa tus datos) |
| Enlace roto o alias sin resolver | Archivo movido o `PROJECT.md` §1 sin ese alias | Corregir el enlace o añadir el alias |
| Numeración con huecos o duplicados | Task creada a mano o renombrada | Renumerar y revisar `INDEX.md` |
| Estado de subtask inválido | Texto libre en la tabla del README de la task | Usar `pendiente`, `en curso`, `hecha` o `hecha (commit <hash>)` |
| Falta `COMANDOS.md` | Instalación anterior a 0.5.0 sin migrar | Proponer `dev-update` (migración de `MIGRATIONS.md`, 0.5.0) |
| `TODO` literal en `PROJECT.md`, `COMANDOS.md` o `DEV-PROFILE.md` | Alguien lo dejó a mano (las plantillas usan `—`) | Rellenar o cambiar por `—`; no hay campos obligatorios |
| Presupuesto de tokens excedido | Un playbook o `AGENTS.md` creció | Mover detalle a una plantilla o a un stack |
| Adaptador apunta a un playbook inexistente | Playbook borrado o renombrado | Regenerar adaptadores con `dev-setup` |
| Task archivada con subtasks sin hacer | Se archivó antes de tiempo | Reabrir o cerrar las subtasks |
| Documento sin fecha o sin índice | Página escrita sin la plantilla | Añadir fecha y `## Contenido` |

## 3. Revisión que el script no hace

Cuando el resultado es limpio, comprueba también:

1. **«Activo ahora» frente a las tasks:** la task y la subtask que indica `INDEX.md` existen, y la subtask está `en curso` o `pendiente`.
2. **Subtasks `en curso` olvidadas:** una subtask `en curso` sin report parcial en `work/reports/` no se puede retomar.
3. **Subtasks `hecha` sin commit:** si el repo ya tiene el commit, el estado debe ser `hecha (commit <hash>)`. Verifícalo con `git log`.
4. **Retros pendientes:** cuenta las filas `pendiente` de `RETRO.md`; si hay 3 o más, recomienda «pide feedback del método (dev-feedback)».
5. **Versión del paquete:** `dev/.package-version` frente a la versión que ofrece `dev-setup`, si el desarrollador la conoce.

## 4. Informe

Entrega esto, breve y en este orden:

1. **Veredicto:** `sano` (0 errores, 0 avisos), `con avisos` o `roto` (hay errores).
2. **Hallazgos**, del más grave al menos, cada uno con archivo, causa probable y arreglo propuesto.
3. **Qué no pudiste comprobar** (sin Python, sin git, repos ausentes).
4. **Pregunta única:** «¿Aplico estos arreglos?», con los de bajo riesgo marcados.

No repitas la salida completa del script: resume por categoría.

## 5. Después de aprobar

Aplica solo lo aprobado, vuelve a ejecutar el verificador y reporta el veredicto nuevo. Si el arreglo cambia el estado de una task, actualiza también `INDEX.md` ([close-session](./close-session.md) §1, punto 6).
