# Food for Joe

## Sector
Pet food — comida natural cocinada para perros y gatos.

## Web
- Web principal: https://www.foodforjoe.es/
- Tienda: https://store.foodforjoe.es/
- Quiz plan personalizado: https://www.foodforjoe.es/quiz/pet?pet=new&step=0&kind=dog

## Propuesta de valor
Comida húmeda natural, cocinada y congelada, personalizada por raza/peso/edad/condición. Diseñada por veterinarios y nutricionistas siguiendo estándares FEDIAF. Sin conservantes artificiales. Fabricada en Galicia con ingredientes españoles y nórdicos (salmón).

## Diferenciadores
- Recetas formuladas por veterinarios y nutricionistas (FEDIAF)
- Fabricado en Galicia, ingredientes de proveedores seleccionados
- Sin conservantes artificiales — pasteurización natural
- Plan 100% personalizado mediante quiz (raza, peso, edad, condición)
- Envío con frío controlado 2–8°C (GLS, Correos Express, SEUR Frío)
- Packaging 100% reciclable

## Productos y precios
- Perro 400g: €4.19–€4.39
- Perro 800g: €6.59–€6.99
- Perro 1200g (Giant): €8.69
- Gato 200g: €2.69
- Proteínas: pollo (Roosterbooster), ternera (Beefit), pavo (Turkeat), cerdo (Porkilicious), pescado (Bigfish)
- Envío gratuito a partir de €49 (€5.95 por debajo)
- Pedido mínimo en alimentación: €24
- Descuento bienvenida: €5 con código WELCOME5 (compra ≥€59)

**Nota de naming (2026-07-13):** las fichas reales de `store.foodforjoe.es` usan "Chick Peasy" para la receta de pollo, mientras que la landing de referencia `go.foodforjoe.es` (funnel de ads) la llama "Roosterbooster". Puede ser rebranding de campaña — confirmar con Jordi/cliente cuál usar en materiales nuevos.

**Humedad real por receta (2026-07-13, de fichas técnicas en store.foodforjoe.es):**
- Beefit (ternera): 73,1%
- Chick Peasy / Roosterbooster (pollo): 72,5%
- Turkeat (pavo): 71,5%
- Porkilicious (cerdo): 71,7%
- Pienso seco (referencia genérica del sector, no de FFJ): 8-12%
- Usar "más del 70% de humedad natural" como claim seguro y verificado — nunca cifras exactas tipo "78%" sin confirmar antes con la ficha técnica real del producto.

## Público objetivo
"Pet parents" que tratan a su perro/gato como un familiar. Perfil consciente de la salud animal, dispuesto a invertir en alimentación de calidad.

## Tono de comunicación
Cercano, emocional, educativo. El animal es el protagonista. Vínculo emocional dueño-perro como eje central.

**Actualización 2026-07-02 (creatividades Meta imagen)**: análisis de los anuncios reales activos en la Ads Library mostró que la marca usa consistentemente "peludo"/"mascota" (no "compañero"/"amigo") en su copy real. Para Header/Subheader de imagen estática, usar "peludo"/"mascota" alineado con el uso real de la marca en Meta Ads, y estructura corta/directa tipo benefit-first (ej. "Recetas 100% personalizadas para tu peludo"). Sin emojis en el texto de la imagen (los emojis sí aparecen en el copy del post/caption, que es una capa distinta no cubierta por este Sheet).

## Paleta de colores
- Fondo oscuro / texto: #163C37 (verde marca — confirmado en el CSS real de go.foodforjoe.es 2026-07-13; versión anterior guardada era #193F37, muy cercana pero no exacta)
- Fondo claro: #F8F3EB
- Acento/highlight/CTA: #F4B221
- Blanco: #FFFFFF
- Texto sobre botón CTA: blanco (no verde)

## Tipografía
**Landings de funnel (go.foodforjoe.es)**: fuentes de marca de pago (Adobe Fonts) — **Cooper** (serif, tipo Georgia) para todo el texto, **Quentin** (script/cursiva) solo para el "Joe" del logo en amarillo. Sin licencia disponible, usar fallback: Playfair Display (serif) + Dancing Script (cursiva) vía Google Fonts.
**Resto de materiales (web principal, landing longevidad)**: Montserrat (Google Fonts) — weights 300, 400, 500, 600, 700, 800.

## Prueba social
- Valoración Trustpilot: 4.2/5
- Valoración Trustedshops: 4.7/5 (confirmado por Jordi, 2026-07-23)
- +760 puntos de venta (España, Francia, Portugal, Italia, Andorra)
- Reseñas verificadas disponibles en: https://www.trustpilot.com/review/foodforjoe.es

## Contacto
- Email: info@foodforjoe.es
- WhatsApp: +34 638 02 69 56 (Lun–Vie 10:00–18:00)

## Métodos de pago
Visa, Mastercard, PayPal.

## Zona de envío
Península Ibérica únicamente (no Canarias, Baleares, Ceuta, Melilla).

## Conservación del producto
Una vez descongelado, guardar en nevera 1–4°C hasta 60 días.

## Arquitectura de landings de pain
Las landings de síntoma/pain (quiz → trial/suscripción, tráfico frío de Meta) siguen la arquitectura obligatoria de 15 bloques definida por el jefe de Jordi en `clients/_referencias/arquitectura-landing-pain.md`. La skill `/skill-experto-landing-page` la detecta y aplica sola cuando el proyecto encaja en ese arquetipo — no es específica de FFJ, pero este es el cliente para el que se redactó.

## Landings
| Fecha | Ángulo | URL | Archivo |
|---|---|---|---|
| 2026-06-09 | Longevidad — más tiempo juntos | https://foodforjoe-longevidad.vercel.app | outputs/food-for-joe/landings/food-for-joe-2026-06-09.html |
| 2026-07-13 | Heces/digestión — comida natural (referencia go.foodforjoe.es/comida-natural-perros) | https://foodforjoe-heces.vercel.app | outputs/food-for-joe/landings/food-for-joe-2026-07-13.html |
| 2026-07-13 | Verano/deshidratación — comida fresca vs. pienso seco | https://foodforjoe-verano.vercel.app | outputs/food-for-joe/landings/food-for-joe-2026-07-13-verano.html |
| 2026-08-11 | Falta de tiempo para cocinarle/darle de comer | https://foodforjoe-falta-tiempo.vercel.app | outputs/food-for-joe/landings/food-for-joe-2026-08-11-tiempo.html |
| 2026-08-26 | Comparativo BARF vs comida natural cocinada (brief de Adri, pendiente de verificación veterinaria) | https://foodforjoe-barf.vercel.app | outputs/food-for-joe/landings/food-for-joe-2026-08-26-barf.html |

## Landings de funnel (go.foodforjoe.es)
- Comida natural: https://go.foodforjoe.es/comida-natural/
- Problemas digestivos: https://go.foodforjoe.es/problemas-digestivos/
- Comida para cachorros: https://go.foodforjoe.es/comida-para-cachorros/
- Senior: https://go.foodforjoe.es/senior/
- Problemas de piel: https://go.foodforjoe.es/problemas-de-piel/
- Adiós pienso: https://go.foodforjoe.es/adios-pienso/
- Mi perro no quiere comer: https://go.foodforjoe.es/mi-perro-no-quiere-comer/
- Comida para perros con sobrepeso: https://go.foodforjoe.es/comida-para-perros-con-sobrepeso/
- Sin huesos: https://go.foodforjoe.es/sin-huesos/
- Comida natural perros (variante): https://go.foodforjoe.es/comida-natural-perros/

## Sheets

- **Propuestas de creatividades (IMG)**: https://docs.google.com/spreadsheets/d/184rmbYW9bDLeMbJBt2EvE6gR40ZS4Kpn9QtsnozKfJ4/edit?gid=1613894543#gid=1613894543
- **Propuestas de creatividades (VIDEOS)**: https://docs.google.com/spreadsheets/d/184rmbYW9bDLeMbJBt2EvE6gR40ZS4Kpn9QtsnozKfJ4/edit?gid=1681992808#gid=1681992808
- Cabeceras de la pestaña IMG (actualizadas 2026-07-02): Funnel, Ángulo, A-Roll/B-Roll, Problema, Header, Subheader, CTA, Landing, Referencia, Activo, Enlace, Resultados (columnas renombradas de Hook/Desenlace/Cierre; se eliminó Tipo)
- Cabeceras de la pestaña VIDEOS (confirmadas 2026-08-14): Target, Funnel, Ángulo, Tipo, A-Roll/B-Roll, Problema, Hook, Desenlace, Cierre, Landing, Referencia, Activo, Enlace, Resultados — usa **Tipo** (quién sale: Persona/Veterinario/Testimonio) en vez de Editor; columna **Target** distingue Perro/Gato
- Criterio de Funnel por ángulo: TOF = Dato/Estadística, Emocional, Founder, Tutorial · MOF = Problema→Solución, Comparativo, Testimonial, Before/After, Demostración · BOF = Social proof
- Jerarquía de overlay en imagen estática: Header = headline corto (3-7 palabras, máximo impacto) · Subheader = 5-9 palabras que refuerzan el header · CTA = botón de 2-4 palabras. Problema no va en imagen, es solo contexto interno de producción.

## Historial de propuestas de creatividades

| Fecha | Semana | ADs | Producto | Estado |
|-------|--------|-----|----------|--------|
| 2026-07-02 | — | 30 (3 imágenes × 10 landings de funnel) | Comida natural para perros — todas las landings de problema/ángulo | Propuesto |
| 2026-07-02 | — | +6 (AD 31–36, revisión de experto: fix de 3 hooks con dato inventado + ángulos nuevos Myth-busting, Vet explica, Reseña real, Relatable/humor, Unboxing, Pregunta directa) | Comida natural para perros | Propuesto |
| 2026-07-02 | — | +30 (AD 37–66, 3 por landing con ángulos nuevos: Testimonial, Demostración, Before/After, Founder, Tutorial, Comparativo, Emocional, Dato/Estadística, Social proof) + fix de 12 claims sin respaldo en las 36 anteriores | Comida natural para perros | Propuesto |
| 2026-08-14 | 45 (pestaña VIDEOS, filas 28-72, Target=Gato) — 9 pain points × 5 vídeos, priorizando los pains dados por la Head of Marketing (Dana) sobre pelo/piel, "quiere lo mejor sin cocinar", selectividad, sobrepeso, miedo a que "natural" sea incompleto y dificultad para cambiar de comida, más 3 pains generales (culpa por ultraprocesado, heces/olor, hidratación) | Comida natural para gatos — primera campaña de vídeo para este target | Propuesto |
| 2026-08-14 | Revisión de copy (skill-experto-copies-meta-ads, modo revisión) sobre los 45 anteriores: 4 fixes aplicados (hook AD41 sin claim de riesgo veterinario no confirmado; agitation añadida en Desenlace de AD1/6/16/36/42 para completar framework PAS; cierres diversificados en AD1/8/16) + 2 ADs nuevos (AD46-47, filas 73-74, ángulo Comparativo) cubriendo la objeción de precio/valor no atacada hasta ahora, ancladas solo en datos confirmados (FEDIAF, código WELCOME5) | Comida natural para gatos | Propuesto |

### Pendiente antes de publicar
- **AD 32** (landing problemas-digestivos, ángulo "Vet explica"): necesita cita real de un veterinario del equipo, o eliminar la referencia a "profesional" si no hay disponible
- **AD 33** (landing senior, ángulo "Reseña real"): necesita una reseña real de Trustpilot para sustituir el testimonio de ejemplo (nombre ficticio)
