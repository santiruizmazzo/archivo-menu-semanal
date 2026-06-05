#!/usr/bin/env python3
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup, Tag

FAREWELL_PATTERNS = [
    "Espero haberte salvado",
    "Si llegaste hasta aca sin caer",
    "Bueno, mision cumplida",
    "Nos reencontramos en la proxima",
    "Nos vemos en el proximo menu",
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

    result = str(soup.prettify(formatter="html"))
    result = re.sub(r'"sticky_offset(_mobile)?":\d+', r'"sticky_offset\1":0', result)
    path.write_text(result, "utf-8")
    print(f"✅ Limpiado: {path}")


if __name__ == "__main__":
    main()
