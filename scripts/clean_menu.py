#!/usr/bin/env python3
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Tag

FAREWELL_PATTERNS = [
    "Espero haberte salvado",
    "Si llegaste hasta aca sin caer",
    "Si llegaste hasta acá sin caer",
    "Bueno, mision",
    "Bueno, misión",
    "Nos reencontramos en la proxima",
    "Nos reencontramos en la próxima",
    "Nos vemos en el proximo menu",
    "Nos vemos en el próximo menú",
]

WHATSAPP_PATTERNS = [
    "Unite a nuestra comunidad de WhatsApp",
    "SUMATE AHORA",
]


def find_topmost_econ(element: Tag) -> Tag | None:
    top = None
    current = element.parent
    while current is not None:
        if isinstance(current, Tag) and "e-con" in (current.get("class") or []):
            top = current
        current = current.parent
    return top


def remove_sections_by_text(soup, patterns):
    for pattern in patterns:
        for node in soup.find_all(string=lambda t: isinstance(t, str) and pattern in t):
            tag = node.parent
            if not isinstance(tag, Tag):
                continue
            container = find_topmost_econ(tag)
            if container:
                container.decompose()


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 scripts/clean_menu.py <ruta/al/archivo.html>", file=sys.stderr)
        sys.exit(1)

    path = Path(sys.argv[1])
    if not path.exists():
        print(f"Error: archivo no encontrado: {path}", file=sys.stderr)
        sys.exit(1)

    raw = path.read_text("utf-8")
    soup = BeautifulSoup(raw, "lxml")

    for tag_name in ["header", "footer"]:
        for el in soup.find_all(tag_name):
            el.decompose()

    remove_sections_by_text(soup, WHATSAPP_PATTERNS)
    remove_sections_by_text(soup, FAREWELL_PATTERNS)

    # Remove the "Volver" link box (div with SVG icon + "Volver" text link)
    for el in soup.find_all("div", attrs={"data-id": "739cf578"}):
        el.decompose()

    # Remove floating WhatsApp button and the 3 popup divs that follow it
    fw = soup.find("div", id="float-whatsapp")
    if fw:
        to_remove = [fw]
        sibling = fw.next_sibling
        while sibling and len(to_remove) < 4:  # fw + 3 next divs
            if isinstance(sibling, Tag) and sibling.name == "div":
                to_remove.append(sibling)
            sibling = sibling.next_sibling
        for el in to_remove:
            el.decompose()

    # Remove stray popup divs outside the main document (caused by embedded HTML snippets)
    for popup in soup.find_all("div", attrs={"data-elementor-type": "popup"}):
        popup.decompose()

    # Fix sticky nav bars: remove JS-added classes/inline styles, remove spacer duplicates
    STICKY_DATA_IDS = {"740ebe60"}
    for data_id in STICKY_DATA_IDS:
        elements = soup.find_all("div", attrs={"data-id": data_id})
        for i, el in enumerate(elements):
            if not isinstance(el, Tag):
                continue
            if i == 0:
                keep_classes = [c for c in (el.get("class") or [])
                                if not c.startswith("elementor-sticky") and c != "elementor-section--handles-inside"]
                el["class"] = keep_classes
                if el.get("style"):
                    style = el["style"]
                    el["style"] = "; ".join(
                        s for s in style.split(";")
                        if not any(k in s.strip() for k in ["position: fixed", "top:", "width:", "margin-top:", "margin-bottom:"])
                    ).strip("; ")
                    if not el["style"]:
                        del el["style"]
            else:
                el.decompose()

    result = str(soup.prettify(formatter="html"))
    result = re.sub(r'"sticky_offset(_mobile)?":\d+', r'"sticky_offset\1":0', result)
    # Strip leaked content after premature </html> (from embedded HTML snippets inside popups)
    first_html_close = result.find("</html>")
    if first_html_close != -1 and first_html_close + 7 < len(result):
        trailing = result[first_html_close + 7:].strip()
        if trailing:
            result = result[:first_html_close + 7]
    path.write_text(result, "utf-8")
    print(f"✅ Limpiado: {path}")


if __name__ == "__main__":
    main()
