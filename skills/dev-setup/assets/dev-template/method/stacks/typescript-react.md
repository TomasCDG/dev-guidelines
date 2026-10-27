# Stack: TypeScript + React

Activar en `COMANDOS.md` §1. Complementa [develop-code](../playbooks/develop-code.md).

- **TypeScript estricto:** `noImplicitAny`, interfaces explícitas para props y estado; evita `any`.
- **Contratos de datos:** `types` o `interfaces` compartidas; validación en los bordes con esquemas (por ejemplo Zod).
- **Componentes enfocados:** funcionales, pequeños, de una sola responsabilidad visual o lógica.
- **Lógica fuera de la vista:** estado y servicios en *custom hooks*; funciones puras para decidir qué mostrar (fáciles de probar).
- **Rendimiento:** dependencias correctas en `useEffect`; `useMemo`/`useCallback` solo donde haya un motivo; imports limpios.
- **El navegador dibuja:** el cálculo de negocio vive donde `PROJECT.md` o el brief lo indiquen, no en el componente.
- **Pruebas:** funciones puras y hooks con casos mínimos; evita pruebas que dependan de la estructura interna del DOM.

## Notas para quien no conoce React

Si la fila «Tecnologías que NO conozco» de `DEV-PROFILE.md` incluye React o TypeScript, los reports explican en lenguaje sencillo términos como componente (función que devuelve una parte de la pantalla), *props* (argumentos del componente), *hook* (función que conserva datos entre actualizaciones de pantalla) y *view model* (función pura que decide qué texto o números mostrar).
