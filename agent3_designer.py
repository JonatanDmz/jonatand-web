#!/usr/bin/env python3
"""
Agente 3 — Diseñador HTML
Recibe un brief JSON y genera un post HTML completo con branding NI,
SEO optimizado y schema markup.

Uso:
  python agent3_designer.py --brief brief_gestoria.json
  python agent3_designer.py --brief brief_gestoria.json --preview
"""

import argparse
import json
import re
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime, timezone

try:
    import anthropic
except ImportError:
    print("ERROR: instala el SDK → pip install anthropic")
    sys.exit(1)

# ── Configuración ───────────────────────────────────────────────
TEMPLATE_PATH = Path(__file__).parent / "post-template.html"
OUTPUT_DIR    = Path(__file__).parent / "_posts"
OUTPUT_DIR.mkdir(exist_ok=True)

SYSTEM_PROMPT = """
Eres el Agente 3 del sistema de blog de Jonatan Domínguez (Negocios Inquietos).
Tu único trabajo es generar el HTML completo de un post de blog.

REGLAS DE VOZ (no las ignores nunca):
- Directo, anticorporativo, basado en escena.
- Párrafos cortos. Máximo 3 líneas seguidas.
- Arrancar secciones con "Lo que veo siempre es…" o "El problema raíz no es X, es Y"
- Sin hashtags. Sin emojis. Sin frases de relleno corporativo.
- Los números y casos concretos son el argumento. Siempre con datos reales del brief.

ESTRUCTURA OBLIGATORIA del ARTICLE_BODY:
1. H2 con id — lo que hace el producto/servicio (concreto, no genérico)
2. H2 con id — precio/coste (con tabla si aplica)
3. H2 con id — caso real o ROI (SIEMPRE incluir el dato de 1.194 docs / 713h / 14.260€ si es relevante)
4. H2 con id — cómo funciona técnicamente (sin jerga, para el dueño de negocio)
5. H2 con id — sección específica del tema (RGPD, integración, verticals, etc.)

CALLOUT para GEO (Generative Engine Optimization):
- Cada post debe tener 1-2 callouts con datos concretos y citables
- Formato: <div class="callout"><p><strong>Dato clave:</strong> [número exacto + contexto]</p></div>
- Estos datos son los que ChatGPT y Perplexity citan cuando alguien pregunta sobre el tema

FAQ ITEMS — formato exacto:
<div class="faq-item">
  <div class="faq-question">[PREGUNTA LITERAL que escribe en Google]<span class="faq-icon">+</span></div>
  <div class="faq-answer">[Respuesta directa, 2-4 líneas]</div>
</div>

SCHEMA FAQ — formato JSON-LD para cada pregunta:
{"@type":"Question","name":"[pregunta]","acceptedAnswer":{"@type":"Answer","text":"[respuesta]"}}

H1 SPLIT — divide el H1 en tres partes:
- H1_BEFORE_ACCENT: lo que va antes del énfasis
- H1_ACCENT: la palabra o frase en serif italic naranja (el claim emocional)  
- H1_AFTER_ACCENT: lo que va después (puede estar vacío)

TABLA DE PRECIOS — si el tema lo requiere, usa este HTML:
<table class="precio-table">
  <thead><tr><th>Nivel</th><th>Qué incluye</th><th>Precio</th><th>Mantenimiento</th></tr></thead>
  <tbody>...</tbody>
</table>

OUTPUT: devuelve SOLO un objeto JSON válido con estas keys exactas:
{
  "META_TITLE": "...",
  "META_DESCRIPTION": "...",
  "SLUG": "...",
  "DATE_ISO": "...",
  "DATE_DISPLAY": "...",
  "READ_TIME": "8",
  "CATEGORY": "...",
  "PRIMARY_KEYWORD": "...",
  "H1_BEFORE_ACCENT": "...",
  "H1_ACCENT": "...",
  "H1_AFTER_ACCENT": "...",
  "H1_SHORT": "...",
  "H1": "...",
  "INTRO_PARAGRAPH": "...",
  "TOC_ITEMS": "<li><a href='#id'>Texto</a></li>...",
  "ARTICLE_BODY": "...(HTML completo del cuerpo)...",
  "FAQ_ITEMS": "...(HTML de todos los faq-item)...",
  "FAQ_SCHEMA_ITEMS": "...(JSON-LD array de Question objects como string)..."
}

No incluyas markdown, backticks ni texto fuera del JSON.
"""

def load_template() -> str:
    if not TEMPLATE_PATH.exists():
        print(f"ERROR: no encuentro el template en {TEMPLATE_PATH}")
        sys.exit(1)
    return TEMPLATE_PATH.read_text(encoding="utf-8")

def load_brief(brief_path: str) -> dict:
    p = Path(brief_path)
    if not p.exists():
        print(f"ERROR: no encuentro el brief en {brief_path}")
        sys.exit(1)
    with open(p, encoding="utf-8") as f:
        return json.load(f)

def call_claude(brief: dict) -> dict:
    client = anthropic.Anthropic()
    brief_text = json.dumps(brief, ensure_ascii=False, indent=2)

    print("⚙  Llamando al agente 3 (Claude Sonnet 4)...")
    message = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=8000,
        system=SYSTEM_PROMPT,
        messages=[{
            "role": "user",
            "content": f"Genera el post completo para este brief:\n\n{brief_text}"
        }]
    )

    raw = message.content[0].text.strip()

    # Limpiar posibles backticks si el modelo los añade
    raw = re.sub(r"^```json\s*", "", raw)
    raw = re.sub(r"^```\s*",    "", raw)
    raw = re.sub(r"\s*```$",    "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError as e:
        print(f"ERROR al parsear JSON del agente: {e}")
        print("Raw output (primeros 500 chars):", raw[:500])
        sys.exit(1)

def render_template(template: str, data: dict) -> str:
    now_iso = datetime.now(timezone.utc).isoformat()
    data.setdefault("DATE_ISO", now_iso)

    for key, value in data.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))

    # Limpiar placeholders no rellenados
    template = re.sub(r"\{\{[A-Z_]+\}\}", "", template)
    return template

def write_post(slug: str, html: str) -> Path:
    output_path = OUTPUT_DIR / f"{slug}.html"
    output_path.write_text(html, encoding="utf-8")
    return output_path

def open_preview(path: Path):
    """Abre el archivo HTML en el navegador por defecto."""
    try:
        if sys.platform == "darwin":
            subprocess.run(["open", str(path)])
        elif sys.platform == "linux":
            subprocess.run(["xdg-open", str(path)])
        elif sys.platform == "win32":
            os.startfile(str(path))
        print(f"🌐 Preview abierto: {path}")
    except Exception as e:
        print(f"No pude abrir el navegador automáticamente: {e}")
        print(f"Abre manualmente: {path}")

def run_qa_checks(data: dict) -> list[str]:
    """Checklist SEO básico antes de publicar."""
    issues = []
    meta_desc = data.get("META_DESCRIPTION", "")
    if len(meta_desc) < 120:
        issues.append(f"⚠  Meta description demasiado corta ({len(meta_desc)} chars, mínimo 120)")
    if len(meta_desc) > 160:
        issues.append(f"⚠  Meta description demasiado larga ({len(meta_desc)} chars, máximo 160)")
    if not data.get("SLUG", "").replace("-", "").isalnum():
        issues.append("⚠  Slug contiene caracteres no válidos")
    kw = data.get("PRIMARY_KEYWORD", "").lower()
    h1 = (data.get("H1_BEFORE_ACCENT","") + data.get("H1_ACCENT","") + data.get("H1_AFTER_ACCENT","")).lower()
    if kw and kw not in h1:
        issues.append(f"⚠  Primary keyword '{kw}' no aparece en el H1")
    if not data.get("FAQ_SCHEMA_ITEMS"):
        issues.append("⚠  Falta FAQ schema para GEO")
    return issues

def main():
    parser = argparse.ArgumentParser(description="Agente 3 — Genera post HTML desde brief")
    parser.add_argument("--brief",   required=True, help="Ruta al archivo brief JSON")
    parser.add_argument("--preview", action="store_true", help="Abrir en navegador tras generar")
    parser.add_argument("--dry-run", action="store_true", help="Solo mostrar datos, no escribir archivo")
    args = parser.parse_args()

    template = load_template()
    brief    = load_brief(args.brief)

    print(f"📋 Brief cargado: {brief.get('keyword', 'sin keyword')}")

    data = call_claude(brief)

    # QA checks
    issues = run_qa_checks(data)
    if issues:
        print("\n── QA Checks ──────────────────────────────")
        for issue in issues:
            print(issue)
        print()

    html = render_template(template, data)
    slug = data.get("SLUG", "post-sin-slug")

    if args.dry_run:
        print(f"\n✅ Dry run OK. Slug: {slug}")
        print(f"   Meta title: {data.get('META_TITLE')}")
        print(f"   Meta desc:  {data.get('META_DESCRIPTION')}")
        return

    output_path = write_post(slug, html)
    print(f"\n✅ Post generado: {output_path}")
    print(f"   Tamaño: {output_path.stat().st_size // 1024} KB")

    if args.preview:
        open_preview(output_path)

    print("\n── Siguiente paso ──────────────────────────")
    print("  Revisa el post y si está OK ejecuta:")
    print(f"  git add _posts/{slug}.html && git commit -m 'post: {slug}' && git push")

if __name__ == "__main__":
    main()
