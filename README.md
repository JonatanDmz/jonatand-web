# Blog automatizado — jonatand.com

Sistema de publicación de blog con agentes Claude Code.
Stack: GitHub Pages + Python + Anthropic API.

## Estructura

```
jonatand-blog/
├── post-template.html        # Template base con branding NI y schema markup
├── agent3_designer.py        # Agente 3: brief JSON → post HTML completo
├── briefs/                   # Briefs de keywords a trabajar
│   └── brief_gestoria.json   # Ejemplo
├── _posts/                   # Posts generados listos para publicar
│   └── agente-ia-gestoria-precio-espana.html
└── .github/
    └── workflows/
        └── deploy.yml        # Auto-deploy a GitHub Pages en cada push
```

## Setup inicial (una sola vez)

```bash
# 1. Instalar dependencias
pip install anthropic

# 2. Configurar tu API key de Anthropic
export ANTHROPIC_API_KEY="sk-ant-..."

# 3. Inicializar repositorio GitHub
git init
git remote add origin https://github.com/TU_USUARIO/jonatand-blog.git

# 4. Crear rama gh-pages y activar GitHub Pages en Settings > Pages
git checkout -b gh-pages
git push -u origin gh-pages
```

## Generar un nuevo post

```bash
# 1. Crea un brief JSON en briefs/
cp briefs/brief_gestoria.json briefs/brief_NUEVO.json
# Edita brief_NUEVO.json con la keyword y datos del nuevo tema

# 2. Genera el post con el agente
python agent3_designer.py --brief briefs/brief_NUEVO.json --preview

# 3. Revisa el post en el navegador
# Si está OK, publica:
git add _posts/
git commit -m "post: SLUG-DEL-POST"
git push origin gh-pages
```

## Flujo completo semanal (cuando añadamos los agentes 1, 2, 4 y 5)

```
Lunes 8:00  → Agente 1 busca las mejores keywords de la semana (web search)
              → Guarda top 3 en briefs/ automáticamente

Lunes 9:00  → Agente 2 genera el contenido SEO+GEO para el brief #1
              → Guarda el brief enriquecido

Lunes 10:00 → Agente 3 (este script) convierte el brief en HTML
              → Genera preview local

Lunes 10:30 → Revisión manual (5-10 min) + aprobación
              → python agent3_designer.py --brief ... && git push
```

## Variables de entorno

| Variable | Descripción |
|----------|-------------|
| `ANTHROPIC_API_KEY` | API key de Anthropic (obligatoria) |

## Branding

El template usa el sistema visual de Negocios Inquietos:
- Colores: negro `#0a0a0a` + naranja `#FF8200`
- Tipografía: Instrument Sans + Instrument Serif italic (naranja)
- Secciones alternando oscuro/claro

## Schema markup incluido por defecto

Cada post generado incluye:
- `Article` con author, publisher, dates
- `BreadcrumbList` (3 niveles)
- `FAQPage` con todas las preguntas del brief
- Open Graph + Twitter Card

## GEO (Generative Engine Optimization)

Para que ChatGPT y Perplexity citen tus artículos:
1. Respuesta directa en el primer párrafo del post
2. Callouts con datos concretos y citables
3. FAQ con preguntas literales que la gente escribe
4. Schema FAQPage en JSON-LD
