# Glee-fully Personalizable Tools™

A joyful static website serving as a hub for custom GPTs organized in a "trunk-branch-twig" hierarchy. Part of the OKHP³™ (OverKill Hill P³) universe.

## Tech Stack

- **Frontend:** Pure HTML5, CSS3, and vanilla JavaScript (no build system)
- **Styling:** Custom CSS variables with a retro-bright palette (Teal, Olive, Ochre, Rust)
- **Fonts:** Google Fonts (Fredoka, Open Sans, Poppins, DM Sans, Alfa Slab One)
- **Dependencies:** Loaded via CDN (Mermaid.js, Ko-fi, Google Analytics)
- **Hosting:** Static site served with Python's built-in HTTP server in dev

## Project Structure

- `index.html` — Main landing page
- `assets/css/theme.css` — Central stylesheet
- `assets/js/app.js` — Shared JS (progress bar, theme toggle, mobile nav)
- `assets/img/` — Branded butterfly and GPT icons
- `toolbox/` — Central hub with 7 thematic branches and their tool-ettes
- `about/`, `contact/`, `legal/`, `persona/`, `universe/`, `ecosystem/` — Supporting pages

## Workflows

- **Start application:** `python3 -m http.server 5000 --bind 0.0.0.0` (port 5000, webview)

## Deployment

Configured as a **static** deployment with `publicDir: "."` — no build step needed.
