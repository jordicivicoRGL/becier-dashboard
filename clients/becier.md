# Becier

**Tipo de cliente**: Grupo empresarial
**Web**: https://www.becier.ad/
**Email de contacto**: jordi@rocketgrowthlab.com

---

## Empresas del grupo

| Empresa | Carpeta de outputs | Descripción |
|---|---|---|
| Vehicles | `outputs/becier/vehicles/` | Concesionario multimarca: nuevos, ocasión y renting |
| Becar | `outputs/becier/becar/` | Alquiler de vehículos (Avis + Easirent): corta y larga duración, particulares y empresas |
| OCS | `outputs/becier/ocs/` | Landing activa |
| Becser | `outputs/becier/becser/` | Correduría de seguros del grupo: particulars i empreses |

---

## Servicios activos

- Landings (OCS)
- Meta Ads (Becier Vehicles)
- Meta Ads (Becar)
- Meta Ads (Becser)

---

## Notas para `/reporte-meta`

- **Idioma del reporte: siempre en català** (mercado 100% andorrano), tanto el `htmlBody` como el `body` de texto plano del borrador de Gmail — no en castellano.
- **Frecuencia como señal secundaria, no protagonista.** Es correcto mencionarla si supera el umbral, pero nunca como el primer punto de "Puntos de atención" — va después de CPL/CTR/rendimiento de creatividad.
- **Vehicles: las campañas cambian de coche cada mes** (nuevo stock, ofertas puntuales tipo Renault Days/Dacia Days), salvo **VO** que siempre tiene campañas evergreen (premium y/o generalistes). Por eso, una frecuencia alta en Vehicles **no debe traducirse en "renueva la creatividad"** — el creativo ya rota solo cada mes por diseño, no por fatiga. En Vehicles el foco del análisis y de "Próximos pasos" tiene que estar en **CPL, CTR y qué formato de creatividad rinde mejor (vídeo / imagen / carrusel)**, no en pedir un cambio de creativo por frecuencia.

---

## Becier Vehicles — Contexto

**Tipo de negocio**: Concesionario multimarca en Andorra. Vende coches nuevos, de ocasión y rentings.

**Marcas**: Multimarca amplia. Entre las principales: Renault, Dacia, Mitsubishi. En ocasión también gama premium: Mercedes, BMW y similares.

**Gama de precios**:
- Mayoría de stock: gama generalista/media (Renault Clio, Dacia Sandero, etc.)
- Vehículos premium de ocasión: pueden superar los 100.000 €

**Servicios complementarios**: Seguros, taller mecánico, neumáticos y otros servicios postventa. No son solo venta de coches.

**Diferencial / USPs**:
- Más de 75 años de presencia en el mercado andorrano (experiencia y confianza)
- Gran variedad de marcas y modelos en un solo concesionario
- Servicio integral: compra, seguro, taller, neumáticos
- Conocimiento profundo del mercado local andorrano

**Geografía**: Solo Andorra

**Público objetivo (Meta Ads)**:
- Hombres, 30-50 años
- Residentes o con conexión con Andorra

---

## Becar — Contexto

**Tipo de negocio**: Empresa de alquiler de vehículos. Fusión entre Avis y Easirent.

**Modalidades**: Corta duración (días/semanas) y larga duración (meses). Clientes particulares y empresas.

**Geografía**: Andorra

---

## Tracking y Conversiones (GA4) — Becier Vehicles

- **GA4 Measurement ID**: G-9BJ71MJGEQ (propiedad "Becier Vehicles", ID 489271404) — dominio real **beciervehicles.ad**. Ojo: no confundir con la propiedad "Becier - GA4" (ID 358016734, G-NEHJ6VL7KC), que es de **becier.ad** (web corporativa del grupo), un dominio distinto.
- **GTM**: el contenedor `GTM-M3WNQ4NX` existe en la cuenta pero **no está instalado en la web** (no aparece en el HTML, "no se han recibido datos"). El tracking real se inyecta directo por plugins/tema, sin pasar por GTM.
- **Sistema de leads real**: formulario de **Bitrix24 CRM** embebido por HTML en las fichas de vehículo. Al enviarse con éxito redirige a `https://www.beciervehicles.ad/gracies/` (ya configurado en Bitrix, no requiere tocar código).
- **Auditoría 2026-09-02**: el único Evento clave que existía (`purchase`) tenía 0 datos desde que se creó la propiedad — Vehicles no reportaba ninguna conversión real en GA4. Prueba de envío real de formulario confirmó que el envío en sí no generaba ningún evento de GA4 (solo `user_engagement`).
- **Causa de la duplicidad de eventos históricos** (`Ver formulario`, `Finalizar el llenado del formulario`, etc., sin marcar como clave): el plugin **"GA Google Analytics" (Jeff Starr)** estaba activo en paralelo a **MonsterInsights**, inyectando el mismo Measurement ID (`G-9BJ71MJGEQ`) dos veces desde `wp_head` — duplicaba el tag de GA4. Desactivado el 2026-09-02.
- **Fix aplicado (2026-09-02)**: creado evento personalizado `generate_lead` en GA4 (condición: `event_name=page_view` AND `page_location contiene /gracies/`) y marcado como Evento clave. Es el único evento de conversión fiable de Vehicles a partir de esta fecha.
- **Eventos con doble conteo potencial**: ninguno tras el fix — `purchase` sigue existiendo como evento clave pero sin datos, no se usa.
- **Fecha de arreglo del tracking**: 2026-09-02 — datos de conversión de formulario anteriores a esta fecha no existen en GA4 (si se necesita histórico, está en el CRM de Bitrix, ver Sheet "Ventes i negociacions" más abajo, aunque **ese Sheet dejó de actualizarse el 2026-07-09** — pendiente de que Becier lo reactive).
- **Próxima revisión sugerida**: 2026-09-10, para confirmar que `generate_lead` ya tiene datos de flujo real.
- **Google Ads (cuenta Grup Becier Bona, 1632468817)**: existe una conversión activa y sana para Vehicles, **"Formulari (beciervehicles.ad)"** (WEBPAGE_CODELESS, objetivo principal, 13 conversiones jun-ago 2026). Hay además 17 conversion actions heredadas de Universal Analytics (Pla Engega, Maserati França, Assegurances Covid, Page Véhicules Confirmation, etc.), todas en estado `HIDDEN` y sin actividad — **Google Ads bloquea su edición/eliminación por API** ("Mutates are not allowed"), así que se quedan tal cual (no afectan a pujas ni informes activos); si algún día se quieren archivar de verdad, sería manual desde la UI de Google Ads.
- **Mapa completo de conversiones/fuentes**: ver `outputs/becier/vehicles/becier-vehicles-mapa-conversiones-2026-09-02.xlsx`.

---

## Meta Ads — Becier Vehicles

- **Sector**: Automoción (concesionario multimarca)
- **Objetivo habitual**: Lead Ad (formulario nativo de Meta → comerciales llaman al lead)
- **Productos anunciados**: Vehículos concretos (nuevo, ocasión, renting) que varían cada mes
- **Público objetivo**: Hombres, 30-50 años, Andorra
- **Zona geográfica**: Solo Andorra
- **Tono y registro**: Directo, específico, confianza. No agresivo. Basado en datos reales. Sin lenguaje de IA.
- **USPs a usar en copy**: Variedad de marcas, servicio integral, experiencia en el mercado andorrano, servicio postventa
- **Precio medio o rango**: Variable. Generalista desde ~8.000-20.000 €. Premium de ocasión hasta +100.000 €.
- **Condiciones habituales**: Financiación disponible, garantía incluida (confirmar con Jordi en cada caso). NO mencionar cuotas ni financiación explícita (Meta penaliza).

### Reglas de copy — OBLIGATORIAS

1. **Idioma**: SIEMPRE en catalán. El mercado es Andorra.
2. **Estructura**: Títol primero, text principal después.
3. **Títol (hook)**: Siempre una pregunta que conecte con un pain point del usuario.
   - Ejemplos de referencia: "Estàs pensant en canviar el cotxe però no tens clar quin model triar? 🤔", "Vols un cotxe d'ocasió que no sembli de segona mà? 🚗"
   - El títol debe detener el scroll generando identificación inmediata.
   - **Aplica a TODAS las variantes (A, B, C), incluida la de "hook directo/dato"**: un dato o cifra concreta también puede (y debe) formularse en pregunta. Detectado en análisis de DACIA-DAYS vs RENAULT-DAYS (julio 2026): RENAULT-DAYS usaba pregunta + invitación a explorar el carrusel, DACIA-DAYS empezaba en afirmación directa — CTR 1,11% vs 0,66%. Si el copy es carrusel con varios modelos, añadir además invitación explícita a explorar ("Fes un cop d'ull al carrussel...").
4. **Emojis**: Sí, tanto en el títol como en el text principal cuando refuercen el mensaje. No abusar.
5. **Cierre estándar** (siempre al final del text principal):
   - `📩 Informa't sense compromís amb l'equip de Becier.` ← el más habitual y genérico
   - `📩 Consulta com reservar-lo abans de la seva arribada amb l'equip de Becier.` ← para vehículos de próxima llegada
6. **Disclaimer** (siempre tras el cierre):
   - `*Consulta les condicions amb els nostres assessors comercials. Preu amb IGI inclòs.`
7. **Sin mención de financiación, cuotas ni condiciones de pago** en el copy (Meta penaliza).

- **Notas de copies anteriores**: _(añadir según vayan acumulándose resultados)_

---

## Tracking y Conversiones (GA4) — Becar

- **GA4 Measurement ID**: G-9X2VY539FH (propiedad "Becar", ID 530050014) — dominio **becar.ad** (marca AVIS Andorra).
- **Sistema de leads real**: mismo patrón que Vehicles — formulario embebido (probablemente Bitrix, sin confirmar backend) que redirige a `https://www.becar.ad/gracies/` al enviarse con éxito. Esa página ya recibía tráfico real (75 vistas en 90 días) antes del fix.
- **Auditoría 2026-09-02**: mismo problema que Vehicles — único Evento clave (`purchase`) sin datos, y señal de formulario repartida en eventos duplicados sin marcar (`Ver formulario #537`, `Finalizar el llenado del formulario #537` vs `Form completion finished #537` — dos implementaciones en paralelo, mismo patrón que Vehicles, sin confirmar el origen exacto).
- **Fix aplicado (2026-09-02)**: creado evento personalizado `generate_lead` (condición: `event_name=page_view` AND `page_location contiene /gracies/`) y marcado como Evento clave.
- **Google Ads (cuenta Grup Becier Bona, 1632468817)**: conversión activa y sana, **"Formulari de reserva Becar"** (tipo WEBPAGE, objetivo principal), ~46 conversiones en jun-ago 2026. No requiere ninguna acción.
- **Fecha de arreglo del tracking**: 2026-09-02 — datos de conversión de formulario anteriores a esta fecha no existen en GA4 como `generate_lead`.
- **Próxima revisión sugerida**: 2026-09-10 (junto con la de Vehicles), para confirmar que `generate_lead` ya tiene datos de flujo real.

---

## Meta Ads — Becar

- **Sector**: Alquiler de vehículos (marca AVIS)
- **Objetivo habitual**: Lead Ad
- **Público objetivo**: Broad 25-65, Andorra
- **Idioma del copy**: Catalán
- **Cierre estándar**: `📩 Reserva la teva furgoneta amb AVIS.` + `*Consulta la disponibilitat i les condicions amb els nostres assessors comercials.` (sin mención de precio salvo que se indique lo contrario)
- **Regla obligatoria — NUNCA mencionar "Becier"**: los anuncios de Becar van a nombre de **AVIS**, no del grupo Becier. AVIS es la empresa/marca de alquiler, no una marca de furgonetas — evitar frases tipo "furgoneta AVIS" que suenen a modelo de vehículo; usar "a AVIS", "amb AVIS", "furgoneta d'AVIS".
- **Notas**: Primera campaña de furgonetes (juliol 2026) — 4 creatividades cubriendo 3 casos de uso: mudances, feina/professionals, grup/aventura (Spaceclass) + carrusel general.

---

## Becser — Contexto

**Tipo de negocio**: Correduría de seguros del grupo Becier. Web: https://becser.ad/
**Sector**: Seguros (particulares y empresas)

**Productos**: Llar, Cotxe, Moto, Viatges, Accidents, Defensa, RC, Comerç, Professionals.

**Diferencial / USPs**:
- +30 anys d'experiència al mercat andorrà
- Cobertura total: particulars i empreses en un sol lloc
- Sinergia de grup: els clients poden centralitzar tots els seus serveis (vehicle, seguro, alquiler…) dins del grup Becier
- Atenció personalitzada i gestió d'incidències local

**Geografía**: Solo Andorra

---

## Tracking y Conversiones (GA4/GTM) — Becser

- **GA4 Measurement ID**: G-EYR44FR24K (propiedad "Becser", ID 538286512) — dominio **becser.ad**. Ojo: existe una **segunda propiedad duplicada y abandonada** ("BECSER", G-Q3R5MT42E2, ID 513032509, creada en noviembre 2025) que ya no está instalada en la web — no confundirla con la real.
- **GTM instalado**: `GTM-TL2MSGS2` (a diferencia de Vehicles, aquí sí está realmente en uso). Contiene: etiqueta de conversión de Google Ads ("Conversión Formulario GADS", activador "Thank You Page" = `/gracies/`, verificada correcta), FB Pixel (All Pages, sin auditar), Etiqueta de Google y Vinculación de conversiones. La etiqueta de GA4 NO pasa por este GTM (va por fuera, probablemente plugin de WordPress, mismo patrón que Vehicles/Becar).
- **Auditoría 2026-09-02**: mismo problema estructural que Vehicles y Becar — único Evento clave (`purchase`) sin datos nunca. Señal real de formulario (varios formularios: #507, #509, #555, #569) sin marcar como conversión.
- **Fix aplicado (2026-09-02)**: creado evento personalizado `generate_lead` en GA4 (condición: `event_name=page_view` AND `page_location contiene /gracies/`) y marcado como Evento clave.
- **Google Ads (cuenta Grup Becier Bona, 1632468817)**: conversión activa y sana, **"Lead Form Becser"** (WEBPAGE, objetivo principal), 17 conversiones jun-ago 2026. Confirmado técnicamente en GTM que dispara solo en la página de éxito real. No requiere ninguna acción.
- **Fecha de arreglo del tracking**: 2026-09-02 — datos de conversión de formulario anteriores a esta fecha no existen en GA4 como `generate_lead`.
- **Próxima revisión sugerida**: 2026-09-10 (junto con Vehicles y Becar).
- **Mapa completo de conversiones/fuentes**: ver `outputs/becier/vehicles/becier-vehicles-mapa-conversiones-2026-09-02.xlsx` (pestaña "Conversiones Becser").

---

## Meta Ads — Becser

- **Sector**: Seguros (todos los tipos)
- **Idioma del copy**: Catalán (mercado andorrano)
- **Objetivo habitual**: Tráfico web a landing y/o Lead Ad — detectar por nombre de campaña en cada reporte (sufijo `_LE`/`TRAFIC` = Landing, `_LEAD AD` = Lead Ad, ver `tools/campaign_naming.py`), no asumir uno fijo. A cierre de julio 2026 todas las campañas activas eran Landing (0 leads en el acumulado del año, 15 resultados de landing a 18,44 € de CPR), pero esto puede cambiar en cuanto se active una campaña `_LEAD AD`.
- **Público objetivo**: Hombres y mujeres, 30+, residentes en Andorra
- **Zona geográfica**: Solo Andorra
- **Tono y registro**: Confianza, cercanía, conocimiento local. Sin tecnicismos. Sin lenguaje de IA.
- **USPs a usar en copy**: +30 anys d'experiència, cobertura per a particulars i empreses, tot en un sol lloc, mercat andorrà
- **Precio**: No mencionar precios en copy (varían por producto y perfil)
- **Cierre estándar**: Por definir — pendiente confirmación de Jordi. Provisional para campañas de tráfico: integrar CTA en el cuerpo del texto.
- **Disclaimer**: No aplica cuando no hay precio. Si se introduce precio en futuras campañas, definir con Jordi.
- **Botó CTA**: Sempre **Més informació** — ha de ser coherent amb el botó real que l'usuari veu a l'anunci.
- **Notas de copies anteriores**: Primera campaña (mayo 2026): lanzamiento nueva web. Objetivo tráfico. 3 variantes testadas: pain point dispersió, descoberta cobertura, credencial +30 anys.

### Producto: Assegurança de Llar / Seguro de Hogar

- **Modalidades**: **Esencial / Integral / Prestigio** (mismo patrón que Viatjes con Vacacional/Integral/Prestige) — permite comparar coberturas y ampliar protección con opciones adicionales.
- **Landing català**: https://becser.ad/asseguranca-llar/
- **Landing castellano**: https://becser.ad/es/seguro-hogar/
- **Objetivo (agosto 2026)**: Tráfico web a landing (carrusel), campaña bilingüe català + castellano con dos landings distintas por idioma.
- **Ángulo de campaña**: Primer seguro de hogar (mudanza, primera vivienda) — pain point de desconocimiento/letra pequeña, resuelto comparando las 3 modalidades.

---

## Google Ads — Becser

- **Web**: https://becser.ad/
- **Servicio/producto anunciado**: Todos los seguros (llar, cotxe, moto, viatge, patinete, RC, pimes, comerços, professionals)
- **Objetivo de campaña**: Lead — formulario en cada página de producto
- **Presupuesto**: 100 €/mes (~3,30 €/día)
- **Ubicación geográfica**: Andorra
- **Público objetivo**: Particulares y empresas residentes en Andorra
- **USPs principales**: +30 anys d'experiència, cobertura total (particulars i empreses), gestió local, tot en un sol lloc
- **Estrategia de puja**: Maximizar conversiones (`MAXIMIZE_CONVERSIONS`), verificado vía API el 2026-09-02 — sin techo de CPC fijo, Google puja automáticamente por subasta. El dato anterior ("CPC máx. 0,60 €") estaba desactualizado, la cuenta cambió de estrategia en algún momento tras la config inicial.
- **Estructura de campaña**: Campaña activa real: `SEARCH_TRAFIC_BECSER_GENERIC` (grupos por idioma, ej. "Catala"). Existen otras 2 campañas antiguas con keywords de seguros solapadas pero **pausadas**: `SEM Assegurances` y `Becser Autos tot risc 150€` — no compiten con la activa, pero conviene revisar si conviene eliminarlas para limpiar la cuenta.
- **Keywords validadas (català)**: [assegurança llar], [assegurança cotxe], [assegurances cotxe], "assegurança moto", "assegurança responsabilitat civil", "assegurança viatge", "millor assegurança llar"
- **Keywords validadas (castellano)**: [seguro de coche], [seguro coche], [seguro hogar], [seguro de casa], [seguro de moto], "seguro de viaje", "seguro de viajeros", "seguro viajes", "seguro de viaje internacional", "seguros de viajeros internacional", "seguro patinete", "seguro responsabilidad civil", "seguro de auto"
- **Keywords negativas**: gratis, gratuïta, gratuito, trabajo, empleo, beca, formación, accidente, denuncia, reclamación, seguro de vida (Becser no lo ofrece)
- **Notas**: Campaña nueva (mayo 2026). URL de anuncio → home becser.ad; keywords de producto → URL específica de cada producto a nivel keyword.

---

## Umbrales de alerta Meta Ads

_Usados por la skill `/reporte-meta`. Vehicles y Becar basados en un único mes de histórico (julio 2026) — revisar tras 2-3 reportes más. Becser validado con el acumulado anual (ver nota abajo)._

**⚠️ Pendiente de separar por objetivo (Vehicles y Becar):** los CPR de Vehicles y Becar de esta sección están calculados sobre el histórico blended (Lead Ad + Landing mezclados en una sola cifra), porque el reporte de julio 2026 aún no separaba resultados por objetivo. Ambos verticales tienen campañas de los dos tipos (ej. Vehicles: `VEHICLES_LE` es Landing, `VO_LEAD_AD`/`RENAULT-DAYS_LEAD_AD` son Lead Ad), así que un CPR de Lead Ad (más caro por definición) y uno de Landing (más barato) no deberían compartir el mismo umbral. En cuanto haya 2-3 reportes con el desglose por objetivo ya correcto, sustituir estos valores únicos por uno por objetivo (como ya se hizo con Becser).

### Vehicles
- Frecuencia: alerta si supera 3,0
- CPM: alerta si sube >30 % sin resultados proporcionales
- CTR bajo: alerta si <0,8 %
- CPR disparado: alerta si supera **3,50 €** (blended Lead Ad + Landing — ver aviso arriba)

### Becar
- Frecuencia: alerta si supera 3,0
- CPM: alerta si sube >30 % sin resultados proporcionales
- CTR bajo: alerta si <0,8 %
- CPR disparado: alerta si supera **7,00 €** (blended Lead Ad + Landing — ver aviso arriba)

### Becser
- Frecuencia: alerta si supera **2,5** (audiencia Andorra pequeña, satura más rápido — ya tocó 4,5 en julio)
- CPM: alerta si sube >30 % sin resultados proporcionales
- CTR bajo: alerta si <0,8 % (ya tocó 0,59-0,67 %, señal más fiable que el % de CPR dado el bajo volumen de leads)
- CPR Landing disparado: alerta si supera **23,00 €** (el CPR Landing acumulado del año es 18,44 €, muy cercano al baseline de ~17 € estimado a partir de la alerta de julio — 24,75 € ese mes ya fue la propia anomalía. Ceiling ajustado a 23 € para dejar margen sobre el rango real 17-19 € sin generar ruido)

## Objetivos Meta Ads

| Vertical | CPR objetivo |
|---|---|
| Vehicles | ~2,50 € |
| Becar | ~4,50 € |
| Becser | ~18,44 € (CPR Landing, validado con acumulado anual: 15 resultados) |

## Historial de reportes Meta Ads

### Becier Vehicles

| Mes | Objetivo | Gasto | Resultados | CPR | Conv. rate | Nota |
|---|---|---|---|---|---|---|
| Julio 2026 | (blended) | 264,81 € | 115 | 2,30 € | 4,58 % | Caída de leads explicada por fin de "Pla Engega" (180 leads en junio); RENAULT-DAYS mejora CPR -62% |
| 01/07–30/07 (recalculado) | (blended) | 264,91 € | 169 | 1,57 € | 6,73 % | Recalculado tras corregir bug de mapeo `action_type` en RENAULT-DAYS/DACIA-DAYS/LEAD_AD-2 (contaban 0 leads en vez de 14/16/11/74); CPR dentro de objetivo (2,50€) pese a subir +28% vs junio; frecuencia alta (5,76, umbral 3,0) en varias campañas |
| 01/07–30/07 | Landing | 3,46 € | 54 | 0,06 € | 88,52 % | Primer desglose limpio por objetivo; gasto muy bajo, no es señal de rendimiento |
| 01/07–30/07 | Lead Ad | 261,49 € | 115 | 2,27 € | 4,69 % | Dentro de objetivo (2,50€); frecuencia >3,0 en las 4 campañas (VO 8,41 la más saturada); CTR bajo (0,66%) en DACIA-DAYS, carrusel de catálogo sin copy propio |
| 01/07–30/07 (reporte /reporte-meta, 30/07) | Landing | 3,46 € | 54 | 0,06 € | 88,52 % | Confirma el dato anterior — mismo período re-generado tras cambios en la skill |
| 01/07–30/07 (reporte /reporte-meta, 30/07) | Lead Ad | 261,88 € | 115 | 2,28 € | 4,68 % | Confirma el dato anterior; caída de gasto (-24%) y resultados (-28%) proporcional vs junio, no es anomalía; DACIA-DAYS sigue con CTR bajo (0,66%), mismo diagnóstico de carrusel dinámico sin copy propio |
| 01/08–20/08 (reporte /reporte-meta, 21/08) | Lead Ad | 104,34 € | 46 | 2,27 € | 4,98 % | Solo VO_LEAD_AD activa (VEHICLES_LE, RENAULT-DAYS y DACIA-DAYS de julio ya finalizadas); caída de gasto/leads (-60%) proporcional, CPR estable y dentro de objetivo; ninguna campaña de "coche del mes" activa en agosto — pendiente confirmar con Becier si hay una nueva prevista |

### Becar

| Mes | Objetivo | Gasto | Resultados | CPR | Conv. rate | Nota |
|---|---|---|---|---|---|---|
| Julio 2026 | (blended) | 24,72 € | 6 | 4,12 € | 4,88 % | Frecuencia sube a 3,8 (saturación); CTR baja a 0,59 % — **este dato era correcto** |
| 01/07–30/07 (recalculado) | Landing | 24,72 € | 72 | 0,34 € | 58,54 % | ⚠️ **ERROR**: se asumió objetivo Landing y se usó `landing_page_view` como resultado, pero el adset real tiene `optimization_goal=OFFSITE_CONVERSIONS` con evento de píxel LEAD — el resultado real son los leads por píxel (6), no las visitas a landing (72). Esta fila y la siguiente quedan invalidadas. |
| 01/07–30/07 (reporte /reporte-meta, 30/07) | Landing | 24,72 € | 72 | 0,34 € | 58,54 % | ⚠️ **ERROR** (mismo motivo que la fila anterior, arrastrado sin detectar) |
| 01/07–30/07 (corregido, 31/07) | Lead (píxel) | 24,72 € | 6 | 4,12 € | 4,88 % | Corrección definitiva tras detectar el error: `pick_result_count` para objetivo Landing ahora prueba primero `offsite_conversion.fb_pixel_lead` (ver `tools/campaign_naming.py`). CPL casi idéntico a junio (4,42€→4,12€, ▼6,8%), leads suben de 5 a 6; dentro de objetivo (4,50€) y lejos del sostre (7,00€) |
| 01/08–20/08 (reporte /reporte-meta, 21/08) | — | 0,00 € | 0 | — | — | Sin ninguna campaña activa en el período (AND_PROS_AVIS-BECAR_LE, la única de julio, ya no estaba activa) — pendiente confirmar con Becier/AVIS si es pausa intencionada o hay que reactivar |

### Becser

| Mes | Objetivo | Gasto | Resultados | CPR | Conv. rate | Nota |
|---|---|---|---|---|---|---|
| Julio 2026 | Landing | 74,24 € | 3 | 24,75 € | 1,02 % | Alerta: CPR +45,5% y leads caen de 9 a 3; frecuencia 4,5 y CTR 0,67% indican fatiga — **este dato era correcto** |
| 01/07–30/07 (recalculado) | Landing | 74,24 € | 12 | 6,19 € | 4,08 % | ⚠️ **ERROR**: mismo motivo que en Becar — se usó `landing_page_view` (12) en vez del evento de píxel LEAD real (3). Esta fila y las dos siguientes quedan invalidadas, incluida la narrativa de "3 períodos consecutivos" (construida sobre el dato erróneo). |
| 01/07–30/07 (reporte /reporte-meta) | Landing | 74,24 € | 12 | 6,19 € | 4,08 % | ⚠️ **ERROR** (arrastrado) |
| 01/07–30/07 (reporte /reporte-meta, 30/07) | Landing | 74,24 € | 12 | 6,19 € | 4,08 % | ⚠️ **ERROR** (arrastrado) |
| 01/07–30/07 (corregido, 31/07) | Lead (píxel) | 74,24 € | 3 | 24,75 € | 1,02 % | Corrección definitiva: `pick_result_count` para objetivo Landing ahora prueba primero `offsite_conversion.fb_pixel_lead`. **CPL ya supera el sostre de alerta (23€)** — CPR sube de 17,01€ (junio, solo BECSER_LE) a 24,75€ (+45,5%), leads caen de 9 a 3 (-66,7%); CPM/CTR bajan solo ~15%, así que el problema es sobre todo post-clic (landing/oferta), no de tráfico. Alerta más seria de toda la cuenta este período |
| 01/08–20/08 (reporte /reporte-meta, 21/08) | Lead (píxel) | 51,97 € | 2 | 25,99 € | 1,16 % | CPR sube +5% (24,75€→25,99€), 3er período consecutivo por encima del sostre (23€), pero volumen muy bajo (2 leads) y sin comparación limpia: producto cambió por completo (viatges/creuers → assegurança de llar). Drill-down: el anuncio CARR_1 sigue mostrando el creativo antiguo "Viatja amb Becser" (CTR 0,33%, peor de los 2 activos) — parece no haberse pausado al lanzar la campaña de Llar. El anuncio nuevo de Llar además mezcla català+castellà en un mismo copy, cuando el perfil preveía dos landings separadas por idioma |

## Sheets

- **Master Paid Media / Copies Ads**: https://docs.google.com/spreadsheets/d/1o3lEYtHApJPZjS3tstufbUOAtjXicszlAVWLAJ2jcnE
  - Pestaña `Copies Ads`: J = Títol, K = Copy, L = Copy v2, M = Copy v3

## Historial de propuestas de creatividades

| Fecha | Semana | ADs | Producto | Estado |
|-------|--------|-----|----------|--------|
| 2026-06-18 | Juny | 2 | Dacia Duster + Dacia Bigster (Dies Únics Dacia) | Propuesto |
| 2026-07-06 | Juliol | 4 | Furgonetes AVIS (Becar) — mudances, feina, Spaceclass, carrusel | Propuesto |
| 2026-07-09 | — | 10 | Becser Llar — segmentado Propietaris (5) / Llogaters (4) / General (1), imagen + carrusel | Propuesto |

## Historial de presupuestos

| Fecha | Empresa | Servicio | Precio | Estado |
|---|---|---|---|---|
| 2026-05-28 | Becser | Auditoría SEO + Estrategia + Ejecución on-page | 1.700 € | Sustituido (no ejecutado, ver 2026-07-11) |
| 2026-07-11 | Vehicles | Colaboración SEO Blog (revisión/optimización, redacción a cargo del cliente) — 50 €/artículo, 10 artículos (500 €) | 500 € | Propuesto |
| 2026-07-11 | Becser | SEO completo: auditoría + estrategia + on-page + plan de contenidos (fase inicial) + blog continuado (opción A 100 €/post redacción completa, opción B 50 €/post colaborativo como Vehicles, sin fecha de fin) | 2.000 € + 50-100 €/post | Propuesto (versión CA) |
