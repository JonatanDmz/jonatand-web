# SOP: Landing Lista de Espera — Comunidad IA para Negocios

## Objetivo
Crear una landing page de captura de lista de espera para validar el interés de mercado en una comunidad/club de IA aplicada a negocios. Inspirada en el formato Skool pero SIN flujo de pago. El objetivo es capturar emails + nombre + información de contexto del interesado.

## Público Objetivo
- Profesionales +40 años con negocios propios o posiciones de gestión
- Dueños de PYME que quieren escalar operaciones sin contratar más personal
- Perfil: cansados del hype de "IA para marketing", buscan IA de verdad para procesos internos
- NO es para emprendedores digitales ni creadores de contenido

## Propuesta de Valor del Proyecto (Copy Core)
- "Escala tu negocio con IA sin añadir más personal al equipo"
- Énfasis en: automatización de procesos, reducción de carga operativa, decisiones más rápidas
- Diferenciar: esto NO es IA para hacer vídeos o posts, es IA para el negocio real
- Tono: directo, maduro, sin promesas de enriquecerse rápido, basado en casos reales

## Estructura de la Landing

### 1. Hero
- Headline impactante con la propuesta de valor principal
- Subheadline que clarifique el público y el enfoque anti-hype
- CTA principal → formulario lista de espera (inline o modal)
- Elemento de escasez/exclusividad: "Acceso limitado", "plazas contadas"

### 2. El Problema (Pain Points)
- Sección que narre los dolores del público objetivo:
  - "Tu equipo está al límite pero no puedes contratar más"
  - "Llevas meses oyendo hablar de IA pero nadie te explica cómo aplicarla a TU negocio"
  - "Las herramientas de IA que ves por ahí son para influencers, no para empresas"

### 3. Qué Es (y qué NO es)
- Formato tipo "Esto SÍ / Esto NO" para diferenciar la propuesta
- SÍ: procesos, operaciones, automatización interna, ahorro de horas
- NO: marketing, vídeos virales, chatbots genéricos, cursos de IA genérica

### 4. Para quién es
- Descripción clara del perfil ideal
- Bullet points con casos de uso concretos por tipo de negocio

### 5. Formato / Lo que encontrarás (beneficios)
- Comunidad de pares (no gurús)
- Casos reales, implementaciones reales
- Sin tecnicismos innecesarios

### 6. Sobre el creador
- Breve credencial de Jonatan como implementador de IA en negocios reales
- Sin exagerar, enfoque en experiencia práctica

### 7. CTA Final + Formulario Lista de Espera
- Campos: Nombre, Email, Tipo de negocio (select), Pregunta de cualificación
- Mensaje tras envío: confirmación y expectativa de cuándo se contactará

## Entradas Técnicas
- Archivo de salida: `comunidad/index.html` (nueva carpeta en el repo)
- CSS: archivo propio `comunidad/style.css` o inline en el HTML
- JS: inline o archivo `comunidad/script.js`
- Formulario: integración con Tally.so (recomendado, gratis) o mailto como fallback
- Sin dependencias de frameworks pesados. HTML/CSS/JS vanilla.

## Estética y Diseño
- Referencia visual: Skool.com pero más premium y serio
- Paleta: oscura/premium. Sin colores eléctricos. Tonos profundos + un acento cálido (ej: dorado, cobre, ámbar)
- Tipografía: display serif para headlines (elegancia y madurez), sans-serif moderno para cuerpo
- Animaciones: sutiles, profesionales. Nada de efectos llamativos o infantiles
- Sensación general: "club exclusivo para profesionales serios", no startup tech
- Mobile-first: debe verse perfecto en móvil (tráfico RRSS es mayoritariamente móvil)

## Restricciones y Advertencias
- No usar frameworks CSS (Tailwind, Bootstrap). Vanilla CSS únicamente.
- El formulario NO debe redirigir a pago. Solo captura de datos.
- No prometer fechas de lanzamiento específicas en el copy (aún es validación)
- El copy debe sonar a persona real (Jonatan), no a copy genérico de agencia
- Evitar palabras como "revolucionario", "disruptivo", "game-changer"
- Mobile-first: probar en viewport 375px como mínimo

## Verificación
- Revisar que el formulario envía correctamente (test submission)
- Verificar que se ve bien en móvil (Chrome DevTools, viewport iPhone 12)
- Confirmar que no hay dependencias externas que puedan fallar
- Publicar en Vercel y compartir URL de preview antes de distribuir en RRSS
