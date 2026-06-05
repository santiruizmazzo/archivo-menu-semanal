## Nuevo menú semanal descargado

1. Ubicar el HTML descargado dentro de una carpeta con el formato `Semana del X-X-XX al X-X-XX/`.

2. Ejecutar el script de limpieza:
   ```
   python3 scripts/clean_menu.py "Semana del X-X-XX al X-X-XX/Menu semana X - Almacén Paulina Cocina.html"
   ```

   El script:
   - Elimina `<header>` y `<footer>` del sitio.
   - Elimina la sección "Unite a nuestra comunidad de WhatsApp" y el texto de cierre ("Espero haberte salvado...", etc.).
   - Setea todos los `sticky_offset` a 0 (la nav bar de días queda pegada al tope).
   - Formatea el HTML con indentación legible.

3. Si el script falla o no encuentra alguna sección, puede que el diseño de la web haya cambiado. Revisar manualmente el HTML y ajustar los patrones de texto en `scripts/clean_menu.py` (variables `FAREWELL_PATTERNS` y/o `WHATSAPP_PATTERNS`).
