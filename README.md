# Archivo Menú Semanal

Archivo personal de menús semanales descargados de mi suscripción.

## Estructura

```
/
├── menus/              ← HTMLs de cada menú semanal
├── index.html          ← generado automáticamente, no editar a mano
├── generate-index.js   ← script generador
└── .github/workflows/  ← GitHub Action de deploy
```

## Convención de nombres

Los archivos en `/menus/` deben seguir el formato:

```
menu_semana_N.html
```

Ejemplos:
- `menu_semana_7.html` → "Semana 7"
- `menu_semana_23.html` → "Semana 23"

Es el mismo nombre que descargás de la app, no hace falta renombrar nada.

## Flujo semanal

1. Descargás el HTML del menú desde la app (ya viene con el nombre correcto)
2. Lo copiás a la carpeta `menus/`
3. `git add . && git commit -m "menú semana X" && git push`
4. La GitHub Action regenera el `index.html` y despliega automáticamente ✓

