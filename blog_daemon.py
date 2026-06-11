#!/usr/bin/env python3
"""
blog_daemon.py — Orquestador del pipeline de blog de Jonatan Domínguez
Lee tareas del dartboard Blog en Dart, ejecuta los agentes correspondientes
según el statusBlog y mueve la tarea al siguiente estado.

Pipeline:
  Idea → [Agente 1: Keyword] → Investigando
  Investigando → [Agente 2: Writer] → Redactando
  Redactando → [Agente 3: Designer] → Diseñando
  Diseñando → [Agente 4: QA] → Revisar  (PARA — espera aprobación manual)
  Revisar → [Agente 5: Publisher] → Publicado  (solo si tú cambias a Publicar)

Uso:
  python blog_daemon.py          # procesa todas las tareas pendientes
  python blog_daemon.py --once   # una sola pasada y sale (para cron)
  python blog_daemon.py --task ID  # procesa solo una tarea concreta

Cron en Hetzner (cada hora):
  0 * * * * cd /opt/jonatand-blog && python blog_daemon.py --once >> logs/daemon.log 2>&1
"""

import os
import re
import sys
import json
import time
import argparse
import subprocess
import logging
from datetime import datetime, timezone
from pathlib import Path

try:
    import anthropic
    import requests
except ImportError:
    print("ERROR: pip install anthropic requests")
    sys.exit(1)

# ── Config ───────────────────────────────────────────────────────
DART_TOKEN      = os.environ.get("DART_TOKEN", "")
ANTHROPIC_KEY   = os.environ.get("ANTHROPIC_API_KEY", "")
DARTBOARD       = "JonatanD/Blog"
STATUS_PROP     = "statusBlog"
REPO_PATH       = Path(os.environ.get("BLOG_REPO_PATH", "/opt/jonatand-blog"))
BLOG_DIR        = REPO_PATH / "blog"
TEMPLATE_PATH   = REPO_PATH / "post-template.html"
GITHUB_REMOTE   = "origin"
GITHUB_BRANCH   = "main"
LIVE_URL_BASE   = "https://blog.jonatand.com/blog"

DART_API        = "https://app.dartai.com/api/v0"
MODEL           = "claude-sonnet-4-20250514"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
log = logging.getLogger("blog-daemon")

# ── Cliente Dart ─────────────────────────────────────────────────
class DartClient:
    def __init__(self, token: str):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

    def list_tasks(self, status_blog: str) -> list[dict]:
        """Devuelve tareas del dartboard Blog con el statusBlog indicado."""
        r = requests.get(
            f"{DART_API}/tasks",
            headers=self.headers,
            params={"dartboard": DARTBOARD, "limit": 50}
        )
        r.raise_for_status()
        tasks = r.json().get("results", [])
        return [
            t for t in tasks
            if t.get("customProperties", {}).get(STATUS_PROP) == status_blog
        ]

    def get_task(self, task_id: str) -> dict:
        r = requests.get(f"{DART_API}/tasks/{task_id}", headers=self.headers)
        r.raise_for_status()
        return r.json()["item"]

    def update_status(self, task_id: str, new_status: str):
        r = requests.patch(
            f"{DART_API}/tasks/{task_id}",
            headers=self.headers,
            json={"item": {"id": task_id, "customProperties": {STATUS_PROP: new_status}}}
        )
        r.raise_for_status()
        log.info(f"  Tarea {task_id} → {new_status}")

    def add_comment(self, task_id: str, text: str):
        r = requests.post(
            f"{DART_API}/comments",
            headers=self.headers,
            json={"item": {"taskId": task_id, "text": text}}
        )
        r.raise_for_status()

    def update_description(self, task_id: str, description: str):
        r = requests.patch(
            f"{DART_API}/tasks/{task_id}",
            headers=self.headers,
            json={"item": {"id": task_id, "description": description}}
        )
        r.raise_for_status()

# ── Cliente Anthropic ─────────────────────────────────────────────
client_ai = None

def get_ai_client():
    global client_ai
    if client_ai is None:
        client_ai = anthropic.Anthropic(api_key=ANTHROPIC_KEY)
    return client_ai

def call_claude(system: str, user: str, max_tokens: int = 8000) -> str:
    ai = get_ai_client()
    msg = ai.messages.create(
        model=MODEL,
        max_tokens=max_tokens,
        system=system,
        messages=[{"role": "user", "content": user}]
    )
    return msg.content[0].text.strip()

# ── Agente 1: Keyword Researcher ─────────────────────────────────
AGENT1_SYSTEM = """
Eres el Agente 1 del sistema de blog de Jonatan Domínguez (jonatand.com / Negocios Inquietos).
Tu trabajo es analizar una keyword candidata y construir el brief estratégico completo
para que el Agente 2 pueda escribir un artículo que posicione en Google Y sea citado
por ChatGPT y Perplexity (GEO — Generative Engine Optimization).

════════════════════════════════════════
CONTEXTO DE MARCA Y NEGOCIO
════════════════════════════════════════

POSICIONAMIENTO CENTRAL:
"Empleados digitales" — los agentes de IA no son herramientas, son empleados sin nómina,
sin bajas, sin irse a la competencia. Jonatan los construye para pymes españolas que quieren
crecer sin contratar.

DOS LÍNEAS DE NEGOCIO:
1. Servicio: construye empleados digitales para empresas (avatar: Manuel)
2. Formación: Club Consultizadores — enseña a freelancers/consultores a vender agentes de IA (avatar: Lucas)

════════════════════════════════════════
AVATAR PRINCIPAL — MANUEL
════════════════════════════════════════

Dueño de negocio, 38-55 años. Autónomo o empresa hasta 20 empleados.
Factura pero no escala. Trabaja 60h/semana. El negocio depende de él para todo.

SUS DOLORES REALES (en su propio lenguaje):
- "No para de trabajar pero el negocio no crece"
- "Todo pasa por mí. Mis empleados no resuelven nada sin consultarme"
- "He intentado contratar. Más personal trajo más gestión, no más beneficio"
- "Veo competidores más pequeños crecer más rápido. Tienen mejores sistemas"
- "Mi familia nota que estoy presente pero ausente"

SUS OBJECIONES PRINCIPALES:
- "Esto es para empresas grandes con departamento IT. Yo soy demasiado pequeño"
- "Ya me quemé — pagué un CRM que nadie usó"
- "¿Cuánto me va a costar realmente?"
- "¿En cuánto tiempo recupero la inversión? Dame un número concreto"
- "¿Funciona para mi sector o es una solución genérica?"

LO QUE REALMENTE QUIERE:
- Que el negocio funcione cuando él no está
- Crecer en facturación sin crecer en plantilla
- Recuperar tiempo para pensar en estrategia
- Poder irse de vacaciones sin que todo se pare
- ROI en menos de 6 meses, con datos

════════════════════════════════════════
CASOS REALES DISPONIBLES COMO PROOF POINTS
════════════════════════════════════════

Usa estos datos concretos siempre que sean relevantes para la keyword:

CASO 1 — Protección de datos Navarra:
2.141 documentos generados automáticamente. 713 horas ahorradas.
14.260€ recuperados en los primeros 5 meses de 2025.
Sistema: transcripción de reunión → agente Claude → informe Word en 20 min.

CASO 2 — Facturación por Telegram:
Agente Telegram + N8N + OneDrive + Google Sheets.
Presentado en charla a comunidad de CEOs.

CASO 3 — Claumar logística:
Empresa de envíos Spain-Paraguay. Automatización de seguimiento y documentación de aduanas.

CASO 4 — Broker electricidad (Alfonso):
Automatización de seguimiento comercial y cualificación de leads.

════════════════════════════════════════
REGLAS SEO
════════════════════════════════════════

1. La keyword principal debe aparecer en el título (H1), en los primeros 100 caracteres
   del artículo y en al menos un H2.

2. El artículo debe responder la pregunta de la keyword en las primeras 2-3 líneas
   (snippet optimization).

3. Identifica keywords secundarias relacionadas que deben aparecer naturalmente en el cuerpo.

4. El slug debe ser corto, sin tildes, con guiones: "agente-ia-gestoria-precio-espana"

5. Meta description: respuesta directa + dato concreto + CTA implícito. Entre 120-160 caracteres.

════════════════════════════════════════
REGLAS GEO (Generative Engine Optimization)
════════════════════════════════════════

Para que ChatGPT y Perplexity citen el artículo de Jonatan cuando alguien pregunte
sobre el tema, el brief debe incluir:

1. RESPUESTA DIRECTA EN INTRO: la primera frase del artículo responde la pregunta
   de la keyword con un dato concreto. Los LLMs escanean el inicio del documento.
   Ejemplo: "Un agente IA para gestoría en España cuesta entre 2.500€ y 8.500€..."

2. CALLOUTS CITABLES: datos numéricos concretos que un LLM puede extraer y citar.
   Formato: [stat] + [contexto] + [fuente/caso].
   Ejemplo: "Una gestoría media dedica 15-25 horas semanales a procesamiento documental.
   Un agente IA automatiza el 70-80% en el primer mes."

3. FAQ LITERALES: las preguntas exactas que alguien escribe en ChatGPT o Google.
   No preguntas teóricas — preguntas reales con intención de compra.
   Ejemplo: "¿cuánto cuesta un agente IA para una gestoría en España?" NO "¿qué es un agente IA?"

4. ESTRUCTURA ESCANEABLE: H2 con números (01, 02...), listas con datos concretos,
   tablas con precios reales. Los LLMs prefieren contenido estructurado.

════════════════════════════════════════
ÁNGULO DIFERENCIADOR
════════════════════════════════════════

Antes de definir el ángulo, analiza qué NO tiene la competencia en esta keyword:
- ¿Alguien publica precios reales? (casi nadie lo hace)
- ¿Hay casos documentados con números del sector específico?
- ¿Alguien habla desde la perspectiva del dueño de negocio, no del técnico?
- ¿Hay comparativa honesta coste IA vs coste empleado?

El ángulo de Jonatan siempre es: datos reales + perspectiva del dueño + precio visible.

════════════════════════════════════════
OUTPUT — SOLO JSON VÁLIDO
════════════════════════════════════════

Responde ÚNICAMENTE con este JSON. Sin markdown, sin backticks, sin texto extra.

{
  "keyword": "keyword candidata original",
  "primary_keyword": "keyword principal optimizada (2-4 palabras)",
  "secondary_keywords": ["kw secundaria 1", "kw secundaria 2", "kw secundaria 3"],
  "category": "Automatización|IA para negocios|Casos reales|Formación",
  "slug": "slug-sin-tildes-con-guiones",
  "difficulty": "Fácil|Media|Alta",
  "angle": "en 1 frase: qué hace este artículo diferente a lo que ya existe",
  "target_audience": "descripción concreta del lector con intención de compra",
  "pain_points": [
    "dolor concreto en lenguaje de Manuel (no técnico)",
    "dolor concreto 2",
    "dolor concreto 3"
  ],
  "proof_points": [
    "dato real de Jonatan relevante para esta keyword",
    "dato real 2 si aplica"
  ],
  "geo_callouts": [
    "stat citable: número + contexto + caso. Ej: Las gestorías españolas dedican 15-25h semanales a clasificación documental. Un agente IA elimina el 70% en el primer mes (caso Navarra, 2025).",
    "stat citable 2"
  ],
  "intro_answer": "respuesta directa a la keyword en 2 líneas con dato concreto. Esta es la primera frase del artículo.",
  "cta": "qué acción quieres que haga el lector al final del artículo",
  "faq_questions": [
    "pregunta literal que alguien escribe en Google o ChatGPT con intención compradora",
    "pregunta literal 2",
    "pregunta literal 3",
    "pregunta literal 4",
    "pregunta literal 5"
  ],
  "content_notes": "observaciones para el Agente 2: qué incluir sí o sí, qué evitar, qué caso usar"
}
"""

def agent1_keyword(task: dict, dart: DartClient) -> dict:
    log.info(f"  [Agente 1] Investigando keyword: {task['title']}")
    brief_raw = task.get("description", "")
    result = call_claude(AGENT1_SYSTEM, f"Analiza esta keyword y enriquece el brief:\n\n{brief_raw}", max_tokens=2000)
    try:
        brief = json.loads(result)
    except json.JSONDecodeError:
        result = re.sub(r"^```json\s*", "", result)
        result = re.sub(r"\s*```$", "", result)
        brief = json.loads(result)
    # Actualiza la descripción con el brief enriquecido
    dart.update_description(task["id"], json.dumps(brief, ensure_ascii=False, indent=2))
    dart.add_comment(task["id"], f"✅ Agente 1 completado. Dificultad: {brief.get('difficulty')}. Ángulo: {brief.get('angle')}")
    return brief

# ── Agente 2: Writer SEO + GEO ───────────────────────────────────
AGENT2_SYSTEM = """
Eres el Agente 2 del sistema de blog de Jonatan Domínguez (jonatand.com / Negocios Inquietos).
Tu trabajo es escribir el artículo completo del blog en HTML, siguiendo el brief del Agente 1.
El artículo debe posicionar en Google Y ser citado por ChatGPT y Perplexity.

════════════════════════════════════════
VOZ DE JONATAN — REGLAS INAMOVIBLES
════════════════════════════════════════

- Directo, anticorporativo, basado en escena. Nunca "en el entorno empresarial actual".
- Párrafos cortos. MÁXIMO 3 líneas seguidas. Mucho espacio en blanco.
- La primera frase de cada sección arranca en la escena, nunca con contexto genérico.
- Patrones que funcionan: "Lo que veo siempre es…", "El problema raíz no es X, es Y"
- Números y casos concretos son el argumento. Nunca "muchas empresas" — siempre datos.
- Sin hashtags. Sin emojis. Sin relleno corporativo.
- Herramientas sin comillas: N8N, Make, Airtable, Claude, Supabase.
- No inventar casos o datos. Solo usar los proof points del brief.

════════════════════════════════════════
ESTRUCTURA DEL ARTICLE_BODY (obligatoria)
════════════════════════════════════════

5 secciones H2 con id, en este orden:

H2 #1 — Qué hace exactamente [el producto/servicio] en [contexto]
  → Concreto y específico. Listar los 3-4 procesos que automatiza con <ul class="ni-checklist">
  → Incluir 1 CALLOUT GEO con dato numérico citable

H2 #2 — Cuánto cuesta: rangos reales para [año]
  → SIEMPRE incluir la tabla de precios. Nadie más lo hace. Es el diferenciador.
  → 3 niveles: Básico / Medio / Completo con precios exactos
  → Frase de apertura: "El problema raíz no es el precio del X en sí, es que nadie publica números."

H2 #3 — Caso real: [dato 1], [dato 2], [dato 3]
  → Narrar el caso del brief como historia: situación → problema → solución → resultado
  → CALLOUT con los números exactos del caso (negrita en el dato clave)
  → Si no hay caso del brief, usar el caso de protección de datos Navarra si es relevante

H2 #4 — Cómo calcular el ROI antes de contratar
  → Fórmula paso a paso (lista <ol>) que Manuel pueda aplicar a su negocio
  → Ejemplo numérico concreto con el sector de la keyword

H2 #5 — Cómo funciona técnicamente (sin jerga)
  → Para el dueño de negocio que no sabe de tecnología
  → <ul class="ni-checklist"> con el flujo de integración paso a paso
  → Si aplica: sección sobre RGPD, legalidad, o integración con software existente

════════════════════════════════════════
COMPONENTES HTML OBLIGATORIOS
════════════════════════════════════════

CALLOUT GEO (1-2 por artículo):
<div class="callout"><p><strong>Dato clave:</strong> [número exacto + contexto + caso si aplica]</p></div>

CHECKLIST NARANJA:
<ul class="ni-checklist">
  <li><strong>Proceso 1.</strong> Descripción concreta de qué hace.</li>
</ul>

TABLA DE PRECIOS (obligatoria si el tema lo permite):
<table class="precio-table">
  <thead><tr><th>Nivel</th><th>Qué incluye</th><th>Precio implementación</th><th>Mantenimiento/mes</th></tr></thead>
  <tbody>
    <tr><td><strong>Básico</strong></td><td>descripción</td><td class="highlight">X.000€ – X.000€</td><td>XXX€ – XXX€</td></tr>
  </tbody>
</table>

H1 SPLIT — divide el H1 en tres partes para el serif accent naranja:
- H1_BEFORE_ACCENT: lo que va antes del énfasis (puede ser el inicio de la frase)
- H1_ACCENT: 1-3 palabras en serif italic naranja (el claim emocional o el dato clave)
- H1_AFTER_ACCENT: lo que va después (puede ser vacío "")
Ejemplo: "Agente IA para gestoría:" | "precio real" | ", qué automatiza y ROI en España"

FAQ ITEMS HTML:
<div class="faq-item">
  <div class="faq-question">[pregunta literal]<span class="faq-icon">+</span></div>
  <div class="faq-answer">[respuesta directa, 2-4 líneas, con dato si aplica]</div>
</div>

════════════════════════════════════════
REGLAS SEO
════════════════════════════════════════

- META_TITLE: keyword principal + beneficio concreto + año. Máximo 60 caracteres.
- META_DESCRIPTION: respuesta directa + dato numérico + CTA implícito. 120-160 caracteres EXACTOS.
- SLUG: sin tildes, sin mayúsculas, con guiones. Máximo 5 palabras.
- H1: keyword principal en los primeros 3 words. Con serif accent en el claim emocional.
- Keyword principal en el primer párrafo (INTRO_PARAGRAPH).
- Keywords secundarias del brief distribuidas naturalmente en H2s y párrafos.

════════════════════════════════════════
REGLAS GEO
════════════════════════════════════════

- INTRO_PARAGRAPH: respuesta directa a la keyword en 2-3 líneas con dato concreto.
  Los LLMs escanean el inicio — si no hay respuesta directa, no citan el artículo.
  Ejemplo: "Un agente IA para gestoría en España cuesta entre 2.500€ y 8.500€ de implementación..."

- CALLOUTS: datos numéricos exactos que un LLM puede extraer y citar directamente.
  Formato: número + contexto + fuente (caso real). Siempre en el componente .callout.

- FAQ_SCHEMA_ITEMS: preguntas literales en formato JSON-LD para FAQPage schema.
  Son las que indexa Google y las que leerán los LLMs para responder consultas.

════════════════════════════════════════
OUTPUT — SOLO JSON VÁLIDO
════════════════════════════════════════

Sin markdown, sin backticks, sin texto fuera del JSON.

{
  "META_TITLE": "máximo 60 caracteres con keyword",
  "META_DESCRIPTION": "120-160 caracteres exactos: respuesta + dato + CTA implícito",
  "SLUG": "keyword-principal-sin-tildes",
  "DATE_ISO": "YYYY-MM-DDTHH:MM:SS+02:00",
  "DATE_DISPLAY": "DD mes YYYY",
  "READ_TIME": "8",
  "CATEGORY": "Automatización",
  "PRIMARY_KEYWORD": "keyword principal del brief",
  "H1_BEFORE_ACCENT": "texto antes del énfasis naranja",
  "H1_ACCENT": "1-3 palabras clave en naranja",
  "H1_AFTER_ACCENT": "texto después del énfasis (o vacío)",
  "H1_SHORT": "versión corta para breadcrumb (3-4 palabras)",
  "H1": "H1 completo sin splits",
  "INTRO_PARAGRAPH": "respuesta directa 2-3 líneas con dato concreto — lo más importante del artículo",
  "TOC_ITEMS": "<li><a href='#id-seccion'>Texto de sección</a></li> x5",
  "ARTICLE_BODY": "HTML completo del cuerpo: 5 H2 + callouts + tablas + checklists",
  "FAQ_ITEMS": "HTML de los 5 faq-item con accordion",
  "FAQ_SCHEMA_ITEMS": "array JSON-LD de Question objects como string para el schema FAQPage"
}
"""

def agent2_writer(task: dict, dart: DartClient) -> dict:
    log.info(f"  [Agente 2] Escribiendo contenido para: {task['title']}")
    brief = task.get("description", "")
    now = datetime.now(timezone.utc)
    user_msg = f"""
Fecha de hoy: {now.strftime('%d %B %Y')}
Brief del artículo:
{brief}

Genera el post completo siguiendo todas las instrucciones.
"""
    result = call_claude(AGENT2_SYSTEM, user_msg, max_tokens=8000)
    result = re.sub(r"^```json\s*", "", result)
    result = re.sub(r"\s*```$", "", result)
    try:
        content_data = json.loads(result)
    except json.JSONDecodeError as e:
        log.error(f"  Error parseando JSON del Agente 2: {e}")
        raise
    dart.add_comment(task["id"], f"✅ Agente 2 completado. Slug: {content_data.get('SLUG')}. Meta: {content_data.get('META_TITLE')}")
    # Guarda el content_data en la descripción para el agente 3
    dart.update_description(task["id"], json.dumps(content_data, ensure_ascii=False, indent=2))
    return content_data

# ── Agente 3: Diseñador HTML ─────────────────────────────────────
def agent3_designer(task: dict, dart: DartClient) -> Path:
    log.info(f"  [Agente 3] Generando HTML para: {task['title']}")
    try:
        content_data = json.loads(task.get("description", "{}"))
    except json.JSONDecodeError:
        log.error("  La descripción no es JSON válido — ¿viene del Agente 2?")
        raise

    template = TEMPLATE_PATH.read_text(encoding="utf-8")
    now_iso = datetime.now(timezone.utc).isoformat()
    content_data.setdefault("DATE_ISO", now_iso)

    for key, value in content_data.items():
        template = template.replace(f"{{{{{key}}}}}", str(value))
    # Limpiar tokens no rellenados
    template = re.sub(r"\{\{[A-Z_]+\}\}", "", template)

    slug = content_data.get("SLUG", f"post-{task['id']}")
    output_path = BLOG_DIR / f"{slug}.html"
    BLOG_DIR.mkdir(exist_ok=True)
    output_path.write_text(template, encoding="utf-8")

    log.info(f"  HTML generado: {output_path} ({output_path.stat().st_size // 1024}KB)")
    dart.add_comment(task["id"], f"✅ Agente 3 completado. Archivo: blog/{slug}.html")
    return output_path

# ── Agente 4: QA ─────────────────────────────────────────────────
def agent4_qa(task: dict, html_path: Path, dart: DartClient) -> bool:
    log.info(f"  [Agente 4] QA del post: {html_path.name}")
    html = html_path.read_text(encoding="utf-8")
    issues = []

    # Checks automáticos
    if "<title>" not in html:
        issues.append("❌ Falta meta title")
    if 'name="description"' not in html:
        issues.append("❌ Falta meta description")
    if 'application/ld+json' not in html:
        issues.append("❌ Falta schema markup")
    if 'FAQPage' not in html:
        issues.append("❌ Falta FAQPage schema")
    if 'class="callout"' not in html:
        issues.append("⚠️  Sin callouts GEO")
    if 'class="ni-checklist"' not in html:
        issues.append("⚠️  Sin checklists")
    if len(html) < 15000:
        issues.append(f"⚠️  Post corto ({len(html)} chars)")

    # Cuenta H2s
    h2_count = html.count("<h2 ")
    if h2_count < 4:
        issues.append(f"⚠️  Solo {h2_count} H2 (mínimo 4)")

    score = 100 - (len([i for i in issues if i.startswith("❌")]) * 20) - (len([i for i in issues if i.startswith("⚠")]) * 5)

    if issues:
        comment = f"📋 **QA Report** — Score: {score}/100\n\n" + "\n".join(issues)
        comment += f"\n\n**Siguiente paso:** Revisa el post en `blog/{html_path.name}` y cambia el estado a **Publicar** para publicar, o a **Redactando** para corregir."
    else:
        comment = f"✅ **QA Report** — Score: {score}/100\n\nTodo correcto. Listo para publicar.\n\n**Siguiente paso:** Cambia el estado a **Publicar** para publicar."

    dart.add_comment(task["id"], comment)
    log.info(f"  QA Score: {score}/100. Issues: {len(issues)}")
    return score >= 60

# ── Agente 5: Publicador ──────────────────────────────────────────
def agent5_publisher(task: dict, dart: DartClient):
    log.info(f"  [Agente 5] Publicando: {task['title']}")

    try:
        content_data = json.loads(task.get("description", "{}"))
        slug = content_data.get("SLUG", "")
    except Exception:
        slug = ""

    if not slug:
        # Intenta encontrar el HTML por título
        title_slug = re.sub(r'[^a-z0-9]+', '-', task['title'].lower()).strip('-')
        slug = title_slug

    html_path = BLOG_DIR / f"{slug}.html"
    if not html_path.exists():
        log.error(f"  No encuentro el HTML: {html_path}")
        dart.add_comment(task["id"], f"❌ No se encontró el archivo `blog/{slug}.html`. Verifica que el Agente 3 lo generó correctamente.")
        return

    # Git add + commit + push
    try:
        subprocess.run(["git", "-C", str(REPO_PATH), "add", str(html_path.relative_to(REPO_PATH))], check=True)
        commit_msg = f"post: {slug}"
        result = subprocess.run(
            ["git", "-C", str(REPO_PATH), "commit", "-m", commit_msg],
            capture_output=True, text=True
        )
        if "nothing to commit" in result.stdout:
            log.info("  Git: nada nuevo que commitear (ya estaba subido)")
        else:
            subprocess.run(["git", "-C", str(REPO_PATH), "push", GITHUB_REMOTE, GITHUB_BRANCH], check=True)
            log.info(f"  Git push OK: {commit_msg}")
    except subprocess.CalledProcessError as e:
        log.error(f"  Error en git: {e}")
        dart.add_comment(task["id"], f"❌ Error al hacer git push: {e}")
        return

    live_url = f"{LIVE_URL_BASE}/{slug}.html"
    dart.add_comment(task["id"], f"🚀 **Publicado** — [{live_url}]({live_url})")
    log.info(f"  Live en: {live_url}")

# ── Pipeline principal ────────────────────────────────────────────
PIPELINE = {
    "Idea":         ("agent1", "Investigando"),
    "Investigando": ("agent2", "Redactando"),
    "Redactando":   ("agent3", "Diseñando"),
    "Diseñando":    ("agent4", "Revisar"),
    "Publicar":     ("agent5", "Publicado"),
    # "Revisar" no tiene paso automático — espera aprobación manual
}

def process_task(task: dict, dart: DartClient):
    task_id = task["id"]
    title   = task["title"]
    status  = task.get("customProperties", {}).get(STATUS_PROP, "")

    log.info(f"Procesando: [{status}] {title} ({task_id})")

    if status not in PIPELINE:
        log.info(f"  Estado '{status}' no tiene acción automática. Saltando.")
        return

    agent_name, next_status = PIPELINE[status]

    try:
        if agent_name == "agent1":
            agent1_keyword(task, dart)

        elif agent_name == "agent2":
            agent2_writer(task, dart)

        elif agent_name == "agent3":
            html_path = agent3_designer(task, dart)
            # Guardamos la ruta en el task para el agente 4
            task["_html_path"] = html_path

        elif agent_name == "agent4":
            # Reconstruye la ruta del HTML
            try:
                cd = json.loads(task.get("description", "{}"))
                slug = cd.get("SLUG", "")
            except Exception:
                slug = ""
            html_path = BLOG_DIR / f"{slug}.html" if slug else None
            if html_path and html_path.exists():
                agent4_qa(task, html_path, dart)
            else:
                dart.add_comment(task["id"], "⚠️  Agente 4: no encontré el HTML para hacer QA. Verifica el slug.")

        elif agent_name == "agent5":
            agent5_publisher(task, dart)

        # Mover al siguiente estado
        dart.update_status(task_id, next_status)
        log.info(f"  ✅ {title} → {next_status}")

    except Exception as e:
        log.error(f"  ❌ Error en {agent_name} para {task_id}: {e}")
        dart.add_comment(task_id, f"❌ Error en {agent_name}: {str(e)[:500]}")

def run(single_task_id: str = None):
    if not DART_TOKEN:
        log.error("Falta DART_TOKEN en variables de entorno")
        sys.exit(1)
    if not ANTHROPIC_KEY:
        log.error("Falta ANTHROPIC_API_KEY en variables de entorno")
        sys.exit(1)

    dart = DartClient(DART_TOKEN)
    log.info("── Blog Daemon arrancando ──")

    if single_task_id:
        task = dart.get_task(single_task_id)
        process_task(task, dart)
        return

    # Procesa en orden de pipeline
    for status in ["Idea", "Investigando", "Redactando", "Diseñando", "Publicar"]:
        tasks = dart.list_tasks(status)
        if tasks:
            log.info(f"Encontradas {len(tasks)} tareas en '{status}'")
            for task in tasks:
                process_task(task, dart)
        else:
            log.info(f"Sin tareas en '{status}'")

    log.info("── Blog Daemon completado ──")

# ── Entry point ───────────────────────────────────────────────────
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Blog Daemon — pipeline de publicación")
    parser.add_argument("--once",  action="store_true", help="Una sola pasada (para cron)")
    parser.add_argument("--task",  type=str,            help="Procesa solo esta tarea (ID de Dart)")
    args = parser.parse_args()
    run(single_task_id=args.task)
