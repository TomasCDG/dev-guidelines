# Almacenamiento de tareas

**Fecha:** 2026-03-03
**Estado:** vigente
**Verificado contra:** `a1b2c3d`
**Código relacionado:** `@back/src/pendientes/repository.py`

## Contenido

1. [Dónde se ejecuta](#1-dónde-se-ejecuta)
2. [Tabla](#2-tabla)

## 1. Dónde se ejecuta

| Paso | Código | Usado por |
|---|---|---|
| Crear y listar | `@back/src/pendientes/repository.py` | Endpoints de `main.py` |
| Archivo de datos | `@back/data/pendientes.db` (SQLite) | El repositorio |

Los endpoints no ejecutan SQL: solo llaman al repositorio.

## 2. Tabla

| Columna | Tipo | Nota |
|---|---|---|
| `id` | entero, clave primaria | Autoincremental. |
| `title` | texto, no nulo | |
| `status` | texto, no nulo | `pending` por defecto. |
| `created_at` | texto ISO 8601, no nulo | |
