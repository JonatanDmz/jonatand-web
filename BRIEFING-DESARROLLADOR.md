# Briefing Técnico - jonatand.com

## Visión General

**Proyecto:** Web personal de Jonatan Domínguez para captar leads (newsletter) y nutrir hacia el Curso WhatsApp IA.

**Cliente objetivo:** Lucas - consultor/autónomo formado en IA que no sabe vender servicios.

**Modelo de negocio:** Contenido gratuito (lead magnets) → Newsletter → Curso de pago.

**Referencia:** pabloypunto.com (mismo modelo de recursos gratuitos + CTAs)

---

## Stack Tecnológico

**Actual:**
- HTML + CSS vanilla (sin framework)
- Sin JavaScript (mantenerlo simple)
- Hosting: Vercel
- Repo: https://github.com/JonatanDmz/jonatand-web

**Mantener:**
- HTML semántico
- CSS en archivo separado
- Sin build tools innecesarios
- Deploy automático en Vercel al push

---

## Páginas a Implementar

### 1. Home (/)

**Objetivo:** Presentar a Jonatan y captar suscriptores.

**Estructura:**
```
[Hero]
- Título principal: "Ayudo a consultores de IA a vender servicios"
- Subtítulo: "Sin sonar a vendedor, sin proyectos a medida que te consumen"
- CTA principal: "Suscríbete a la newsletter" → /newsletter

[Problema]
- "Si tienes conocimientos técnicos pero no sabes cómo empaquetarlos..."
- 3 bullets de problemas típicos de Lucas

[Propuesta]
- Qué hace Jonatan diferente:
  - No vende herramientas, vende resultados
  - Servicios replicables, no proyectos a medida
  - Método SCREAMS para detectar oportunidades

[Recursos destacados]
- 2-3 lead magnets con:
  - Título
  - Descripción corta (2 líneas)
  - "Leer más" → /recursos/[slug]

[Testimonios / Casos - opcional por ahora]
- Placeholder para futuro

[CTA final]
- "¿Quieres aprender a vender servicios de IA?"
- Formulario simple: nombre + email
- Botón: "Suscribirme"

[Footer]
- Links: Recursos | Newsletter | Sobre mí
- Redes: LinkedIn | TikTok
- Copyright
```

**Diseño:**
- Colores marca Negocios Inquietos (ver skill branding-ni si aplica)
- Tipografía clara, profesional
- Hero con foto de Jonatan
- Responsive obligatorio

---

### 2. Página de Recursos (/recursos)

**Objetivo:** Listar todos los lead magnets disponibles.

**Estructura:**
```
[Intro]
- Título: "Recursos gratuitos para consultores de IA"
- Subtítulo: "Artículos, guías y herramientas para vender más y mejor"

[Lista de recursos]
- Cada recurso como card con:
  - Icono o imagen
  - Título
  - Descripción (2-3 líneas)
  - Etiqueta: "Lead Magnet" | "Artículo" | "Herramienta"
  - Botón: "Leer" → /recursos/[slug]

[CTA]
- "¿Te ha servido algo?"
- "Suscríbete para recibir más contenido cada semana"
- Formulario: nombre + email

[Footer]
```

**Recursos iniciales:**
1. Sistema de WhatsApp IA → /recursos/sistema-whatsapp-ia
2. 10 preguntas para detectar oportunidades → /recursos/10-preguntas-oportunidades

---

### 3. Páginas de Lead Magnet (/recursos/[slug])

**Objetivo:** Entregar valor y convertir a suscriptor.

**Estructura:**
```
[Header recurso]
- Título del lead magnet
- Subtítulo si aplica
- Tiempo de lectura: "X min de lectura"

[Contenido]
- Artículo completo (ver archivos en lead-magnets/)
- Formato: tipografía clara, párrafos cortos
- Headings bien estructurados (H2, H3)
- Destacados para frases clave
- Listas con bullets

[CTA intermedio - opcional]
- "¿Quieres aprender esto paso a paso?"
- Link al curso

[CTA final]
- "Si esto te ha servido, suscríbete"
- Formulario: nombre + email
- Beneficios de suscribirse (3 bullets)

[CTA secundario]
- "¿Quieres implementar esto con ayuda?"
- Link al curso o Kaizen Room

[Navegación]
- "← Volver a recursos"
- "Siguiente recurso →"

[Footer]
```

**Archivos de contenido:**
- `/lead-magnets/sistema-whatsapp-ia.md`
- `/lead-magnets/10-preguntas-detectar-oportunidades.md`

---

### 4. Página Newsletter (/newsletter)

**Objetivo:** Página dedicada a suscripción.

**Estructura:**
```
[Hero]
- Título: "Newsletter para consultores de IA"
- Subtítulo: "Cada semana, una idea que puedes aplicar"

[Qué recibes]
- 3-5 bullets de contenido típico:
  - Casos reales de automatizaciones
  - Estrategias para vender servicios
  - Errores que te hacen perder clientes
  - Prompts y plantillas útiles

[Frecuencia]
- "Un email por semana. Sin spam."

[Formulario]
- Nombre
- Email
- Botón: "Suscribirme"

[Social proof - opcional]
- "X consultores suscritos"
- Testimonio corto

[Footer]
```

---

### 5. Sobre mí (/sobre-mi) - opcional por ahora

**Objetivo:** Credibilidad y conexión.

**Contenido mínimo:**
- Foto
- Bio corta (3-4 párrafos)
- Experiencia relevante
- Links a redes

---

## Formulario de Newsletter (GoHighLevel)

**Requisitos:**
- Integración con GoHighLevel (GHL)
- Campos: nombre + email
- Redirect a página de gracias: /gracias
- Confirmation email automático (configurar en GHL)

**Implementación:**
```html
<form action="https://api.gohighlevel.com/v1/forms/[FORM_ID]" method="POST">
  <input type="text" name="name" placeholder="Tu nombre" required>
  <input type="email" name="email" placeholder="Tu email" required>
  <button type="submit">Suscribirme</button>
</form>
```

**Página de gracias (/gracias):**
```
[Mensaje]
- "¡Gracias por suscribirte!"
- "Revisa tu email para confirmar"

[Siguiente paso]
- "Mientras, puedes leer estos recursos:"
- Links a 2-3 lead magnets

[Redes]
- "Sígueme en LinkedIn | TikTok"
```

**✅ Datos de GoHighLevel confirmados:**
- **Location ID:** `zOr5yw5OQZWEXc5ePhc6`
- **Form ID:** `lE0EpNUS2vvUrEc1UrdS`
- **Form URL:** `https://app.funnels.top/v2/location/zOr5yw5OQZWEXc5ePhc6/form-builder-v2/lE0EpNUS2vvUrEc1UrdS`

**Implementación sugerida:**
```html
<form action="https://app.funnels.top/v2/location/zOr5yw5OQZWEXc5ePhc6/form-builder-v2/lE0EpNUS2vvUrEc1UrdS" method="POST">
  <input type="text" name="name" placeholder="Tu nombre" required>
  <input type="email" name="email" placeholder="Tu email" required>
  <button type="submit">Suscribirme →</button>
</form>
```

**Pendiente:** Confirmar redirect post-submit y email de bienvenida en GHL.

---

## Estructura de Archivos

```
jonatand-web/
├── index.html              # Home
├── recursos/
│   ├── index.html          # Lista de recursos
│   ├── sistema-whatsapp-ia.html
│   └── 10-preguntas-oportunidades.html
├── newsletter/
│   └── index.html          # Página de suscripción
├── gracias/
│   └── index.html          # Página post-suscripción
├── sobre-mi/
│   └── index.html          # Bio (opcional)
├── css/
│   └── styles.css          # Estilos principales
├── images/
│   ├── jonatan.jpg         # Foto principal
│   └── og-image.jpg        # Open Graph
└── README.md
```

---

## SEO Básico

**Cada página debe tener:**

```html
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[Título página] | Jonatan Domínguez</title>
  <meta name="description" content="[Descripción 150-160 caracteres]">
  
  <!-- Open Graph -->
  <meta property="og:title" content="[Título]">
  <meta property="og:description" content="[Descripción]">
  <meta property="og:image" content="/images/og-image.jpg">
  <meta property="og:url" content="https://jonatand.com/[path]">
  
  <!-- Favicon -->
  <link rel="icon" href="/favicon.ico">
  
  <!-- CSS -->
  <link rel="stylesheet" href="/css/styles.css">
</head>
```

---

## Responsive Design

**Breakpoints:**
- Mobile: < 768px
- Tablet: 768px - 1024px
- Desktop: > 1024px

**Prioridad mobile-first.**

---

## Checkboxes para Desarrollador

### Fase 1: Estructura base
- [ ] Configurar repo local y conectar con Vercel
- [ ] Crear estructura de carpetas
- [ ] Implementar CSS base (colores marca, tipografía, espaciado)

### Fase 2: Páginas principales
- [ ] Home (index.html)
- [ ] Página /recursos (lista)
- [ ] Página /newsletter
- [ ] Página /gracias

### Fase 3: Lead magnets
- [ ] Convertir `sistema-whatsapp-ia.md` a HTML
- [ ] Convertir `10-preguntas-detectar-oportunidades.md` a HTML
- [ ] Crear plantilla reutilizable para futuros lead magnets

### Fase 4: Integración GHL
- [ ] Implementar formulario newsletter
- [ ] Conectar con GoHighLevel
- [ ] Probar flujo completo de suscripción
- [ ] Configurar redirect a /gracias

### Fase 5: SEO y optimización
- [ ] Meta tags en todas las páginas
- [ ] Open Graph images
- [ ] Favicon
- [ ] Sitemap.xml
- [ ] robots.txt

### Fase 6: Deploy
- [ ] Push a main branch
- [ ] Verificar deploy en Vercel
- [ ] Probar en mobile
- [ ] Verificar formularios en producción

---

## Recursos para Desarrollador

**Contenido:**
- `/lead-magnets/sistema-whatsapp-ia.md`
- `/lead-magnets/10-preguntas-detectar-oportunidades.md`
- `ESTRATEGIA-CAPTACION.md`

**Branding:**
- **Sistema visual Negocios Inquietos** (ver skill `branding-ni`)
- **Colores principales:**
  - Negro: `#0a0a0a` (fondos oscuros)
  - Naranja: `#FF8200` (acentos, CTAs, énfasis) - EXACTO, no aproximar
  - Blanco: `#ffffff` (texto sobre oscuro)
  - Gris claro: `#f2f2f0` (secciones alternas)
- **Tipografía:**
  - Instrument Sans (body, headlines)
  - Instrument Serif italic (énfasis emocional, siempre en naranja `#FF8200`)
  - JetBrains Mono (código)
- **Patrón de diseño:** Alternar secciones negro / gris claro
- **Botones:** Siempre con `→` al final
- **Logo proporcionado:** Usar el enviado por Jonatan

**Assets disponibles:**
- [x] Logo Negocios Inquietos → `assets/logo-ni.jpg`
- [x] Foto profesional de Jonatan (hero) → `assets/jonatan-hero.jpg`
- [x] Foto secundaria → `assets/jonatan-foto.jpg`
- [ ] Imágenes para Open Graph (pueden esperar)

---

## Timeline Sugerido

**Semana 1:**
- Estructura base + CSS
- Home page
- Deploy inicial

**Semana 2:**
- Página /recursos
- Páginas de lead magnets
- Formulario newsletter

**Semana 3:**
- Integración GHL completa
- Testing
- SEO básico

---

## Contacto

**Propietario:** Jonatan Domínguez
**Email:** jonatan@negociosinquietos.com (temporal)
**Web actual:** https://jonatand.com
**Repo:** https://github.com/JonatanDmz/jonatand-web

---

**Documento creado:** 2026-04-07
**Última actualización:** 2026-04-07
