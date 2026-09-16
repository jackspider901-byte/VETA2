"""Build a portable, dependency-free HTML prototype from the editable source."""
from pathlib import Path
import base64
import json
import re

ROOT = Path(__file__).resolve().parent

def build() -> Path:
    html = (ROOT / 'index.html').read_text(encoding='utf-8')
    css = (ROOT / 'src/styles.css').read_text(encoding='utf-8')
    catalogue = (ROOT / 'src/catalogue.js').read_text(encoding='utf-8')
    app = (ROOT / 'src/app.js').read_text(encoding='utf-8')
    assets = {p.name: 'data:image/jpeg;base64,' + base64.b64encode(p.read_bytes()).decode('ascii') for p in (ROOT / 'assets').glob('*.jpg')}
    favicon = 'data:image/svg+xml;base64,' + base64.b64encode((ROOT / 'assets/favicon.svg').read_bytes()).decode('ascii')
    html = html.replace('href="assets/favicon.svg"', 'href="' + favicon + '"')
    html = html.replace('<link rel="stylesheet" href="src/styles.css">', '<style>\n' + css + '\n</style>')
    # Escape HTML closing-script sequences defensively when adding inline source.
    safe = lambda s: re.sub(r'</script', r'<\\/script', s, flags=re.I)
    html = html.replace('<script src="src/catalogue.js"></script>', '<script>window.VEXA_ASSETS=' + json.dumps(assets) + ';\n' + safe(catalogue) + '\n</script>')
    html = html.replace('<script src="src/app.js"></script>', '<script>\n' + safe(app) + '\n</script>')
    output = ROOT / 'VEXA-Prototype.html'
    output.write_text(html, encoding='utf-8')
    print(f'Built {output.name}: {output.stat().st_size:,} bytes')
    return output

if __name__ == '__main__':
    build()
