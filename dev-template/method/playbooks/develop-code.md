---
name: develop-code
description: Aplica las reglas de código limpio, arquitectura y testing, más los packs de stack activos del proyecto. Úsala cuando vayas a escribir, modificar o probar código, o a definir criterios de código y pruebas en un brief.
---

# Desarrollo de código

## 1. Principios

- **Simplicidad sobre astucia:** claridad y legibilidad antes que trucos.
- **Responsabilidad única** por módulo, clase o función.
- **Nombres con intención**, sin abreviaturas ambiguas.
- **Cero código muerto:** sin código comentado, variables sin usar ni funciones obsoletas; la historia vive en git.
- **Atomización equilibrada:** funciones pequeñas sí, pero sin helpers de un solo uso que obliguen a saltar entre decenas de funciones. Manda la legibilidad del flujo.
- **Cambio mínimo y enfocado:** lo que pide el brief; sin refactors ni funcionalidad fuera de alcance.
- **Dependencias nuevas:** solo con aprobación del desarrollador.

## 2. Arquitectura

- **Capas desacopladas:** dominio, casos de uso e infraestructura/adaptadores.
- **Inversión de dependencias:** la lógica de negocio no depende de bases de datos, APIs ni SDKs; ambos dependen de abstracciones.
- **Defensa en los bordes:** valida y sanea la entrada en los límites del sistema con esquemas declarativos.
- **Contratos aditivos:** cambia API, formatos y mensajes compartidos solo de forma compatible hacia atrás, salvo decisión expresa.
- **El cálculo vive donde el brief indique:** no dupliques lógica de negocio entre capas.

## 3. Testing

- Pruebas unitarias simples, con mocks y fixtures mínimos; **aisladas** (sin servicios ni recursos externos salvo que el brief pida integración o extremo a extremo).
- **AAA:** Arrange (preparar), Act (actuar), Assert (afirmar).
- **Deterministas y rápidas:** mismo resultado en cualquier entorno; sin depender del reloj, del azar ni del orden.
- **Núcleo mínimo en cada subtask:** las funciones de las que dependen los criterios de aceptación (caso feliz y el caso límite que cite el brief). La matriz completa se pide en subtasks de endurecimiento.
- **Verificación real:** si el cambio es observable, ejecútalo (comandos en [COMANDOS.md](../../COMANDOS.md) §2; si falta el que necesitas, pregúntalo una vez, propón uno y anótalo allí; los de esta máquina, en `docs/`) y comprueba el resultado, no solo que pasen las pruebas. Informa de lo que no pudiste ejecutar.

## 4. Stacks

Lee **solo** los packs marcados como activos en `COMANDOS.md` §1 (si todos valen `—`, pregunta qué stacks aplican y anótalo):

| Pack | Archivo |
|---|---|
| Python | [python](../stacks/python.md) |
| TypeScript + React | [typescript-react](../stacks/typescript-react.md) |
| Swift / iOS | [swift](../stacks/swift.md) |
