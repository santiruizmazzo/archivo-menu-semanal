const fs = require("fs");
const path = require("path");

const MENUS_DIR = path.join(__dirname, "menus");
const OUTPUT = path.join(__dirname, "index.html");

// Lee todos los HTMLs en /menus/ y los ordena numéricamente (más reciente primero)
const files = fs
  .readdirSync(MENUS_DIR)
  .filter((f) => f.endsWith(".html"))
  .sort((a, b) => {
    const weekA = parseInt(a.match(/(\d+)/)?.[1] ?? "0");
    const weekB = parseInt(b.match(/(\d+)/)?.[1] ?? "0");
    return weekB - weekA;
  });

// Formatea el nombre del archivo en un título legible
// Espera nombres tipo: menu_semana_7.html → "Semana 7"
function formatTitle(filename) {
  const base = filename.replace(".html", "");
  const match = base.match(/^menu_semana_(\d+)$/i);
  if (match) {
    return `Semana ${parseInt(match[1])}`;
  }
  // Si el nombre no sigue la convención, lo muestra como está
  return base.replace(/[_-]/g, " ");
}

// Genera una etiqueta "hace N semanas" o "esta semana"
// Como el archivo no trae año, compara solo contra la semana actual del año en curso
function weekLabel(filename) {
  const match = filename.match(/^menu_semana_(\d+)/i);
  if (!match) return "";

  const fileWeek = parseInt(match[1]);
  const currentWeek = getISOWeek(new Date());
  const diff = currentWeek - fileWeek;

  if (diff === 0) return "esta semana";
  if (diff === 1) return "hace 1 semana";
  if (diff > 1) return `hace ${diff} semanas`;
  return "";
}

function getISOWeek(date) {
  const d = new Date(date);
  d.setHours(0, 0, 0, 0);
  d.setDate(d.getDate() + 3 - ((d.getDay() + 6) % 7));
  const week1 = new Date(d.getFullYear(), 0, 4);
  return (
    1 +
    Math.round(
      ((d.getTime() - week1.getTime()) / 86400000 -
        3 +
        ((week1.getDay() + 6) % 7)) /
        7
    )
  );
}

const menuCards = files
  .map((file, i) => {
    const title = formatTitle(file);
    const label = weekLabel(file);
    const isLatest = i === 0;
    return `
      <a href="menus/${file}" class="card${isLatest ? " card--latest" : ""}">
        <div class="card-header">
          ${isLatest ? '<span class="badge">Último</span>' : ""}
          ${label ? `<span class="label">${label}</span>` : ""}
        </div>
        <div class="card-title">${title}</div>
        <div class="card-arrow">→</div>
      </a>`;
  })
  .join("\n");

const emptyState = `
  <div class="empty">
    <p>Todavía no hay menús guardados.</p>
    <p>Agregá un HTML en la carpeta <code>menus/</code> con el formato <code>YYYY-WNN.html</code></p>
  </div>`;

const html = `<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Mis Menús Semanales</title>
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet" />
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #faf8f4;
      --surface: #ffffff;
      --border: #e8e2d9;
      --text: #1a1714;
      --muted: #8a8076;
      --accent: #c8603a;
      --accent-light: #f5ede8;
      --latest-bg: #1a1714;
      --latest-text: #faf8f4;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'DM Sans', sans-serif;
      min-height: 100vh;
      padding: 3rem 1.5rem 5rem;
    }

    header {
      max-width: 640px;
      margin: 0 auto 3.5rem;
    }

    .eyebrow {
      font-size: 0.7rem;
      font-weight: 500;
      letter-spacing: 0.15em;
      text-transform: uppercase;
      color: var(--accent);
      margin-bottom: 0.75rem;
    }

    h1 {
      font-family: 'Playfair Display', serif;
      font-size: clamp(2rem, 5vw, 3rem);
      font-weight: 700;
      line-height: 1.1;
      color: var(--text);
    }

    .subtitle {
      margin-top: 0.75rem;
      font-size: 0.95rem;
      color: var(--muted);
      font-weight: 300;
    }

    .count {
      display: inline-block;
      margin-top: 1.5rem;
      font-size: 0.8rem;
      color: var(--muted);
      border-top: 1px solid var(--border);
      padding-top: 1rem;
      width: 100%;
    }

    .grid {
      max-width: 640px;
      margin: 0 auto;
      display: flex;
      flex-direction: column;
      gap: 0.75rem;
    }

    .card {
      display: grid;
      grid-template-columns: 1fr auto;
      grid-template-rows: auto auto;
      gap: 0.25rem 1rem;
      padding: 1.25rem 1.5rem;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 6px;
      text-decoration: none;
      color: inherit;
      transition: border-color 0.15s, box-shadow 0.15s, transform 0.15s;
      position: relative;
      overflow: hidden;
    }

    .card::before {
      content: '';
      position: absolute;
      left: 0; top: 0; bottom: 0;
      width: 3px;
      background: transparent;
      transition: background 0.15s;
    }

    .card:hover {
      border-color: var(--accent);
      box-shadow: 0 4px 20px rgba(200, 96, 58, 0.08);
      transform: translateX(2px);
    }

    .card:hover::before { background: var(--accent); }

    .card--latest {
      background: var(--latest-bg);
      border-color: var(--latest-bg);
      color: var(--latest-text);
    }

    .card--latest:hover {
      border-color: var(--accent);
      box-shadow: 0 4px 24px rgba(0,0,0,0.2);
    }

    .card-header {
      grid-column: 1;
      grid-row: 1;
      display: flex;
      align-items: center;
      gap: 0.5rem;
      min-height: 1.2rem;
    }

    .badge {
      font-size: 0.65rem;
      font-weight: 500;
      letter-spacing: 0.1em;
      text-transform: uppercase;
      background: var(--accent);
      color: white;
      padding: 0.15em 0.5em;
      border-radius: 3px;
    }

    .label {
      font-size: 0.75rem;
      color: var(--muted);
      font-weight: 300;
    }

    .card--latest .label { color: #a09890; }

    .card-title {
      grid-column: 1;
      grid-row: 2;
      font-family: 'Playfair Display', serif;
      font-size: 1.1rem;
      font-weight: 400;
      line-height: 1.3;
    }

    .card-arrow {
      grid-column: 2;
      grid-row: 1 / 3;
      display: flex;
      align-items: center;
      font-size: 1.1rem;
      color: var(--muted);
      transition: transform 0.15s, color 0.15s;
    }

    .card:hover .card-arrow {
      transform: translateX(3px);
      color: var(--accent);
    }

    .card--latest .card-arrow { color: #a09890; }
    .card--latest:hover .card-arrow { color: var(--accent); }

    .empty {
      max-width: 640px;
      margin: 0 auto;
      padding: 3rem;
      text-align: center;
      color: var(--muted);
      border: 1px dashed var(--border);
      border-radius: 6px;
      line-height: 2;
    }

    .empty code {
      font-size: 0.85rem;
      background: var(--border);
      padding: 0.1em 0.4em;
      border-radius: 3px;
    }

    footer {
      max-width: 640px;
      margin: 3rem auto 0;
      font-size: 0.75rem;
      color: var(--border);
      text-align: center;
    }
  </style>
</head>
<body>
  <header>
    <p class="eyebrow">Archivo personal</p>
    <h1>Mis Menús<br>Semanales</h1>
    <p class="subtitle">Menús guardados de mi suscripción semanal.</p>
    ${
      files.length > 0
        ? `<span class="count">${files.length} menú${files.length !== 1 ? "s" : ""} guardado${files.length !== 1 ? "s" : ""}</span>`
        : ""
    }
  </header>

  <main class="grid">
    ${files.length > 0 ? menuCards : emptyState}
  </main>

  <footer>
    Generado el ${new Date().toLocaleDateString("es-AR", {
      weekday: "long",
      year: "numeric",
      month: "long",
      day: "numeric",
    })}
  </footer>
</body>
</html>`;

fs.writeFileSync(OUTPUT, html, "utf8");
console.log(`✓ index.html generado con ${files.length} menú(s).`);
