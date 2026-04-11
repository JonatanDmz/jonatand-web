# Análisis CRO — jonatand.com Home

**Fecha:** 2026-04-09  
**Analista:** Agente CRO (Paperclip)  
**Página:** https://jonatand.com  
**Objetivo principal:** Captar suscriptores newsletter (Lucas: consultor IA que no sabe vender servicios)

---

## Puntuación global: 6.5/10

La web tiene una base sólida: diseño limpio, buen branding, copy honesto que conecta con el público. Pero tiene problemas estructurales de conversión que le están costando suscriptores. Lo más grave: el hero no tiene un CTA claro orientado a la audiencia, el formulario de newsletter no funciona, y no hay prueba social visible.

---

## Top 5 mejoras priorizadas por impacto

### 1. 🚨 El formulario de newsletter NO funciona (Impacto: CRÍTICO)

**Qué pasa:** El `<form>` no tiene `action` ni hay JavaScript que lo procese. El botón "Quiero recibirla" literalmente no hace nada. Recarga la página y punto.

**Principio CRO:** Una conversión nula por fricción técnica. No importa cuánto optimices el copy si el mecanismo de conversión está roto.

**Sugerencia:**
- Conectar a un servicio real (Mailchimp, ConvertKit, Beehiiv, etc.)
- Si no hay backend, usar un formulario externo (e.g., Beehiiv embed) como solución rápida
- Añadir feedback visual: mensaje de confirmación tras enviar ("¡Apuntado! Revisa tu email")
- Mientras tanto, poner un link directo a la landing de suscripción del email service como workaround

---

### 2. 🎯 El hero habla de Jonatan, no del visitante (Impacto: ALTO)

**Qué pasa:** "Estoy construyendo un negocio de IA y te cuento todo el proceso" → centrado en Jonatan. El visitante piensa "¿y esto para mí qué?" en los primeros 3 segundos.

**Principio CRO:** La regla del "tú" — el visitante necesita entender qué gana en menos de 5 segundos. El hero es tu inmueble más valioso.

**Sugerencia:** Reformular orientando al visitante:
- Headline tipo: "Aprende a vender servicios de IA aunque no sepas por dónde empezar"
- O: "De consultor a consultizador: construye un negocio de automatización que funcione"
- Mantener el subtítulo actual como apoyo (la historia personal da credibilidad)
- El CTA del hero debería ir directo al lead magnet más concreto, no a la newsletter genérica

---

### 3. 👤 No hay foto real (Impacto: ALTO)

**Qué pasa:** El hero tiene `<img src="assets/jonatan-hero.jpg">` y la sección "Sobre mí" tiene un placeholder gris. Si la foto no existe o falla, se ve un hueco vacío. Y aunque exista, en "Sobre mí" sigue siendo placeholder.

**Principio CRO:** La confianza se construye con rostro. Una web de marca personal sin foto real es como un perfil de LinkedIn sin cara — genera desconfianza subconsciente.

**Sugerencia:**
- Foto profesional en el hero (ya está referenciada, verificar que existe y se ve bien)
- Foto real también en "Sobre mí" (eliminar el placeholder gris)
- La foto debería transmitir cercanía + competencia (no necesariamente traje)

---

### 4. 🔒 Cero prueba social (Impacto: ALTO)

**Qué pasa:** No hay un solo testimonial, logo de cliente, número de suscriptores, o mención de resultados de otros. Solo cifras propias (60k€, +20 industrias) que son buenas pero no suficientes.

**Principio CRO:** Prueba social = reducción de riesgo percibido. La gente no cree lo que tú dices de ti; cree lo que otros dicen de ti.

**Sugerencia:**
- Añadir 2-3 testimonial quotes reales (aunque sean de Kaizen Room o clientes de servicios)
- "Únete a X lectores" junto al formulario de newsletter (si hay suficientes)
- Logos de empresas donde ha trabajado (SEAT, etc.) como credibilidad previa
- Número de seguidores totales si es decente ("+10k entre TikTok y LinkedIn")

---

### 5. 📱 CTAs de recursos son genéricos y no capturan (Impacto: MEDIO-ALTO)

**Qué pasa:** Los links a guías ("Descargar guía →") apuntan a páginas internas, pero no hay gating ni mecanismo de captura de email. O sea: das valor gratis sin pedir nada a cambio. Además, la primera tarjeta de recursos ("Newsletter semanal") es redundante — ya hay una sección newsletter más abajo.

**Principio CRO:** Cada punto de contacto de alto valor debería ser una oportunidad de conversión. Las guías deberían ser lead magnets que capturen email.

**Sugerencia:**
- Convertir las guías en lead magnets reales: email a cambio de descarga
- Eliminar la tarjeta redundante de newsletter de la sección Recursos
- Priorizar el lead magnet más potente (probablemente la guía WhatsApp IA) con un CTA más prominente
- Añadir un segundo CTA de newsletter entre secciones (sticky o interstitial suave)

---

## Qué está bien y NO tocar

✅ **Branding y diseño visual** — Paleta coherente, tipografía cuidada, animaciones sutiles sin exceso. Se ve profesional sin ser corporativo.

✅ **Copy de "Sobre mí"** — El storytelling funciona. La progresión (fábricas → SEAT → digital) es creíble y diferenciadora. La frase "La diferencia no está en las herramientas..." es potente.

✅ **Tono general** — "Sin humo", "sin filtros", "no soy un gurú" conecta bien con la audiencia que está cansada de marketing agresivo.

✅ **Navegación sticky** — Funciona bien, con blur y opacidad. Los links internos están bien elegidos.

✅ **Responsive CSS** — Los breakpoints cubren móvil, tablet y desktop. El hero pasa a columna en móvil correctamente. El formulario de newsletter apila verticalmente en móvil. Bien pensado.

✅ **Accesibilidad básica** — `lang="es"`, `viewport` meta, `alt` en imagen hero, `prefers-reduced-motion` respetado.

✅ **Sección "Lo que comparto"** — Sencilla y clara. Las tres categorías dan contexto sin abrumar.

✅ **Footer** — Limpio con los links esenciales. El email directo funciona.

---

## Problemas adicionales (menor prioridad)

- **Title tag:** "Automatización e IA para negocios (sin humo)" — demasiado genérico. Debería incluir la propuesta única o el nombre para SEO: "Jonatan Domínguez — Aprende a monetizar la IA como consultor"
- **Meta description:** No existe. Añadir una que incluya la propuesta de valor y un CTA.
- **No hay favicon** — Se ve la pestaña genérica del navegador. Detalle que resta profesionalidad.
- **No hay Open Graph tags** — Cuando alguien comparte el link en redes, no se verá una preview bonita. Perdemos click-through.
- **Velocidad:** Carga 3 fuentes de Google Fonts (Instrument Sans, Serif, JetBrains Mono). JetBrains Mono no se usa en ningún sitio visible — eliminarla ahorra ~30KB.
- **Hero photo path:** Si `assets/jonatan-hero.jpg` no existe, el visitante ve un hueco vacío. Añadir fallback o alt text más descriptivo.
- **El link `mailto:jonatan@jonatand.com`** en servicios abre el cliente de email. Mejor un formulario de contacto o un link a Calendly para reducir fricción.
- **No hay analytics** — Sin Google Analytics, Plausible o similar, no hay forma de medir conversión real. Imposible optimizar lo que no mides.
