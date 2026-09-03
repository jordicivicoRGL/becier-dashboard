# Properfy

**Sector:** Inmobiliaria sin comisiones  
**Web:** https://www.properfy.es/  
**Teléfono:** 93 159 19 04  
**WhatsApp:** 622 39 73 15  
**Email:** clientes@properfy.es

## Propuesta de valor
Inmobiliaria de tarifa fija (desde 1.990€) que cobra solo si vende. Sin porcentaje sobre el precio. Posicionamiento: "del lado del propietario".

## Datos clave
- +3.000 pisos vendidos
- 30 días de media hasta venta (vs. 6+ meses del sector)
- 30 años de experiencia en Barcelona
- Tarifas: 1.990€ – 12.990€ según precio del inmueble
- Oficinas en Barcelona y Madrid

## Marca
- **Logo:** https://www.properfy.es/wp-content/uploads/2023/03/logo-elementor.svg
- **Colores:** Accent #E84D68 (coral/rosa-rojo) · Fondo blanco · Texto oscuro #54595F · Dark #312828 · Claro #FFF3EE
- **Tipografía:** Roboto (body) + Roboto Slab (headings)
- **Tono:** Profesional, transparente, empático ("te acompañamos")

## SEM
- **Keywords principales:** "vender piso barcelona", "inmobiliaria sin comisiones barcelona"
- **CTA:** Formulario de valoración gratuita (nombre + email + teléfono + comentarios)
- **Landing SEM activa:** `outputs/properfy/landings/properfy-vender-piso-barcelona-2026-05-27.html`
- **Google Ads Customer ID:** 3929043521 (bajo MCC Rocket, login customer 9198804727)

## Sheets

- **Propuestas de creatividades:** https://docs.google.com/spreadsheets/d/14KmAxQEIvtCTzxhB0vpsWB5_UV5nMR0lyWrniDF8LHQ

## Outputs
- `outputs/properfy/landings/` — landings SEM/SEO

## Historial de propuestas de creatividades

| Fecha | ADs | Producto | Estado |
|-------|-----|----------|--------|
| 2026-06-02 | 12 (4 ángulos × 3 hooks) | Properfy — venta de pisos Barcelona tarifa fija | Propuesto |

## Conversiones / tracking (auditoría 2026-08-27)

- GTM container: **GTM-T598J23** (cuenta "Properfy" en Tag Manager) — Google tag AW-11208707904.
- 19 de 20 campañas estaban en PAUSED (solo SEARCH_TASACION activa) → explica los "errores" de conversión reportados (falta de datos recientes, no fallo técnico).
- **Doble conteo corregido:** las acciones "Lead" (webpage codeless) y "Lead_Vender_GTM" (tag GTM) se disparaban ambas en la misma página `/gracias-vender/` y las dos contaban como principal. Se cambió "Lead" a acción secundaria (ya no pesa en pujas/columna Conversiones); "Lead_Vender_GTM" queda como única acción principal de venta.
- **2 landings rotas sin thank you page:** `/vender-piso-rapido/` y `/vender-landing/` usan formularios Contact Form 7 sin redirección tras enviar (las páginas que funcionan usan Elementor Forms con acción "Redirigir a" → `/gracias-vender/`). Por eso nunca disparan GTM ni conversión. Pendiente decisión de Juan Luis sobre si deben unificarse con el resto o mantener comportamiento propio; no se ha tocado.
- Trigger GTM "Activador form Madrid /gracias-vender/" exige `Referrer contiene /vender-piso-en-madrid/` — sin cruce con Barcelona, correcto.
- "Conversiones mejoradas" en la acción "Lead" mostraba advertencia de configuración (gestionada vía GTM) — quedó resuelta al pasar "Lead" a secundaria.
