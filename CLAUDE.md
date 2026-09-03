# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Comandos principales

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar el asistente
python main.py
```

La primera ejecución con Google APIs abrirá un flujo OAuth2 en el navegador. Las credenciales se guardan en `credentials/token.json`.

## Variables de entorno

El proyecto requiere un archivo `.env` con:
```
ANTHROPIC_API_KEY=...
TOGETHER_API_KEY=...
```

Las credenciales de Google OAuth van en `credentials/client_secret.json`.

## Arquitectura

**main.py** es el punto de entrada: implementa un loop de conversación multi-turno con Claude (Opus 4.7, thinking adaptativo activado). Llama a la API de Anthropic con 8 herramientas registradas y gestiona el ciclo completo de tool use (recibe `tool_use` blocks, ejecuta la función Python correspondiente, devuelve `tool_result`).

**tools/** contiene los módulos de integración:
- `calendar_tools.py` / `gmail_tools.py` — Usan Google API con OAuth2; comparten el mismo flujo de autenticación. El token se cachea en `credentials/token.json`.
- `pdf_tools.py` — Genera propuestas PDF con ReportLab y las guarda en `outputs/[cliente]/proposals/`.
- `image_tools.py` — Genera imágenes con Together AI (FLUX.1-schnell) y las guarda en `outputs/[cliente]/images/`.

## Comandos personalizados

`/redactar-propuesta` — flujo de 3 pasos para crear propuestas comerciales en PDF. Definido en `.claude/commands/skill-redactar-propuesta.md`.

`/skill-experto-mailing` — experto en email marketing para cualquier cliente. Genera mailings completos (asunto, preencabezado, cuerpo, CTAs y sugerencias visuales) a partir de links de producto reales. Carga el perfil del cliente desde `clients/` si existe, y pregunta si guardar el perfil al terminar cuando el cliente es nuevo. Definido en `.claude/commands/skill-experto-mailing.md`.

`/skill-experto-google-ads` — experto en Google Ads y copywriting. Ayuda con la configuración de campañas (estructura, pujas, keywords, extensiones) y con la creación de anuncios RSA (títulos y descripciones optimizados para CTR). Guarda el perfil Google Ads de cada cliente en `clients/`. Definido en `.claude/commands/skill-experto-google-ads.md`.

`/skill-experto-copies-meta-ads` — experto en copywriting de respuesta directa para Meta Ads (Facebook e Instagram). Genera copies en catalán para Becier y en el idioma adecuado para otros clientes. Frameworks PAS/AIDA, hooks de pain point, límites técnicos de Meta y checklist de calidad integrados. Definido en `.claude/commands/skill-experto-copies-meta-ads.md`.

`/reporte-meta` — reporting semanal de Meta Ads a nivel de campaña. Extrae métricas clave (gasto, impresiones, alcance, CPM, CPC, CTR, clics en enlace, resultados, coste por resultado, conversion rate, frecuencia), calcula variación semana a semana y genera un email listo para copiar y enviar al cliente. Guarda histórico en `clients/[cliente].md`. Definido en `.claude/commands/reporte-meta.md`.

`/propuesta-creatividades` — genera propuestas de creatividades para Meta Ads (imagen, carrusel, vídeo) y las escribe directamente en el Google Sheet del cliente. Tres fases: (1) análisis opcional de winners/losers de las últimas 4 semanas, (2) generación de N propuestas con los 7 campos core — Producto, Problema, Ángulo, Hook, Desenlace, Cierre, Tamaños — más notas de producción, (3) escritura automática en el Sheet leyendo primero las cabeceras para adaptarse a la estructura de cada cliente. Definido en `.claude/commands/propuesta-creatividades.md`.

`/skill-experto-landing-page` — crea landing pages de alta conversión para campañas de Meta Ads. Clientes activos: **DCORE** (reformas lujo Madrid, `clients/dcore.md`) con landings pendientes: presupuesto sin sobrecostes y reforma chalets. Dos flujos: si hay copy, genera el HTML directamente; si no, hace las preguntas necesarias, propone texto y estructura, y tras el OK genera el HTML. Tipografía Montserrat, diseño mobile-first, animaciones suaves, imágenes con FLUX. Guarda el archivo en `outputs/[cliente]/landings/[cliente]-[fecha].html`. Definido en `.claude/commands/skill-experto-landing-page.md`.

`/reporte-seo-diagonalcq` — genera el informe SEO mensual para Diagonal CQ. El usuario adjunta el PDF exportado de Looker Studio (4 páginas: histórico GSC + mensual GSC + GA general + GA cirugía) y la skill produce el texto completo sección por sección, listo para pegar en Canva. Incluye Resumen Ejecutivo, análisis de visibilidad, brand vs no brand, keywords, rendimiento de páginas de cirugía (prioridad estratégica), métricas GA, demografía y conclusiones con next steps. Output directamente en el chat. Definido en `.claude/commands/skill-reporte-seo-diagonalcq.md`.

`/skill-experto-generacion-imagenes` — generación profesional de imágenes estáticas para campañas Meta Ads. Panel de 4 expertos: Estratega de campaña, Director de arte, Especialista en prompts FLUX y Copy visual. Acepta transcripción de vídeo o brief libre. Genera 2 variaciones conceptuales en los 3 formatos estándar de Meta (1:1, 9:16, 4:5) con overlay de texto integrado. Guarda imagen base + imagen con overlay en `outputs/[cliente]/imagenes-meta/`. Definido en `.claude/commands/skill-experto-generacion-imagenes.md`.

`/skill-traductor` — traduce landing pages HTML y copies de texto plano a cualquier idioma. Carga el perfil del cliente desde `clients/` para mantener el tono de marca. Para HTML preserva toda la estructura/código y solo traduce el contenido visible. Guarda el archivo traducido en `outputs/[cliente]/landings/[cliente]-[idioma]-[fecha].html`. Definido en `.claude/commands/skill-traductor.md`.

`/skill-presupuesto` — ayuda a calcular cuánto cobrar por proyectos de marketing digital (landing pages, SEO, Meta Ads, Google Ads, estrategia omnicanal, email marketing, consultoría). Distingue entre clientes que ya saben qué quieren y clientes que solo tienen un objetivo (descubrimiento). Recoge cliente, país (España/Andorra), tipo de servicio y posicionamiento de precio en un único mensaje inicial. Hace búsqueda de mercado real adaptada al sector y geografía del cliente, analiza factores de complejidad, detecta oportunidades de upsell, calcula valor total del contrato en servicios mensuales y aplica la nota fiscal correcta (IVA 21% / IGI 4,5%). Tras confirmar el precio, genera el PDF del presupuesto y guarda el historial en `clients/[cliente].md`. Definido en `.claude/commands/skill-presupuesto.md`.

`/skill-analisis-cuenta-google-ads` — auditoría completa de una cuenta de Google Ads. Panel de 5 expertos (Auditor de estructura, Especialista en keywords/search terms, Especialista en anuncios/assets, Estratega de presupuesto/conversiones, Director de cuenta). Extrae datos vía API con las funciones ampliadas de `tools/ads_tools.py` (resumen de cuenta, grupos de anuncios, keywords con Quality Score, search terms, Ad Strength, cobertura de extensiones, rendimiento por dispositivo y recomendaciones nativas de Google). Entrega un informe único en el chat con salud de cuenta por semáforo, hallazgos por área y oportunidades priorizadas por impacto/esfuerzo. Guarda histórico de auditorías en `clients/[cliente].md`. Definido en `.claude/commands/skill-analisis-cuenta-google-ads.md`.

`/skill-experto-etiquetado` — experto en tracking y etiquetado digital. Panel de 4 expertos: Auditor de Tracking, Especialista GTM+GA4, Especialista Conversiones Google Ads y Especialista Meta Pixel+CAPI. Flujo: (1) diagnóstico estructurado del problema (síntoma, causa raíz, conflictos, plan de acción), (2) implementación técnica por módulo (GTM, Google Ads, Meta), (3) validación con checklist completo. Cubre thank-you page, clic en botón, dataLayer/AJAX, conversiones duplicadas, Enhanced Conversions, deduplicación CAPI y Event Match Quality. Guarda IDs y configuración de tracking en `clients/[cliente].md`. Definido en `.claude/commands/skill-experto-etiquetado.md`.

`/skill-auditoria-conversiones-ga4` — auditoría y arreglo de conversiones GA4 para cualquier cliente, antes de reportar sobre ellas. El paso diferenciador frente a `/skill-experto-etiquetado`: cruza siempre GA4 contra el backend real del cliente (formulario del CMS, CRM, agenda) para detectar fugas de tracking o eventos que miden la cosa equivocada, en vez de fiarse de lo que "parece" estar bien dentro de GTM/GA4. Flujo: diagnóstico de eventos en GA4 → cruce con backend real → auditoría técnica en GTM (todos los contenedores) → implementación del fix (listener dataLayer + evento GA4) → verificación obligatoria en preview y producción, en más de una página → marcar Eventos clave sin duplicar señales → reporting desglosado por canal en Looker Studio → comunicación al cliente. Guarda IDs, contenedores y eventos verificados en `clients/[cliente].md`. Definido en `.claude/commands/skill-auditoria-conversiones-ga4.md`.

## Memoria del usuario

El archivo `memory.md` en la raíz del proyecto contiene información persistente sobre Jordi: condiciones comerciales, preferencias y contexto personal. **Consúltalo siempre** antes de redactar propuestas, hablar de precios o tomar decisiones que puedan verse afectadas por sus reglas y preferencias.

## Notas de diseño

- El asistente está configurado para Jordi Civico, responde en español y usa la zona horaria `Europe/Madrid`.
- El modelo se especifica directamente en `main.py` como `claude-opus-4-7`; cambiar el modelo aquí afecta a todas las llamadas.
- `adaptive_thinking` está habilitado en las llamadas a la API.
