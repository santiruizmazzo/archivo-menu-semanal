## Nuevo menú semanal descargado

1. Ejecutar el script de conversión (reemplaza referencias locales `_files/` por URLs en vivo e inlinea el CSS específico de la página):
   ```
   python3 scripts/convert_to_single_html.py "Semana del X-X-XX al X-X-XX/Menu semana X - Almacén Paulina Cocina.html"
   ```

2. Ejecutar el script de limpieza:
   ```
   python3 scripts/clean_menu.py "Semana del X-X-XX al X-X-XX/Menu semana X - Almacén Paulina Cocina.html"
   ```

   El script:
   - Elimina `<header>` y `<footer>` del sitio.
   - Elimina la sección "Unite a nuestra comunidad de WhatsApp" y el texto de cierre ("Espero haberte salvado...", etc.).
   - Elimina el `div#float-whatsapp` (botón flotante de WhatsApp) y los 3 `div`s siguientes (popups de Elementor).
   - Elimina cualquier `div[data-elementor-type="popup"]` remanente (pueden quedar sueltos por HTML embebido dentro de los popups).
   - Trunca el contenido que queda después del primer `</html>` (fragmentos que el parser deja fuera del documento por HTML embebido mal formado dentro de los popups).
   - Setea todos los `sticky_offset` a 0 (la nav bar de días queda pegada al tope).
   - Elimina clases e inline styles de Elementor sticky (sobrantes del JS).
   - Formatea el HTML con indentación legible.

3. Opcional: borrar la carpeta `_files` ya no es necesaria.

4. Si el script falla o no encuentra alguna sección, puede que el diseño de la web haya cambiado. Revisar manualmente el HTML y ajustar los patrones de texto en `scripts/clean_menu.py` (variables `FAREWELL_PATTERNS` y/o `WHATSAPP_PATTERNS`).
