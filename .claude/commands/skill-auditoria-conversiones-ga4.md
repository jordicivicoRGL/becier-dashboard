# Skill: Auditoría y Arreglo de Conversiones GA4

Se invoca cuando un cliente pide "verificar que las conversiones están bien medidas", "activar reporting de SEO/Ads sobre conversiones", "por qué no me cuadran los leads con lo que veo en Analytics", o cualquier variante de auditar/arreglar el tracking de conversiones en GA4 antes de reportar sobre ellas.

**Premisa de la skill:** la mayoría de auditorías de tracking se quedan mirando GTM y GA4 por dentro, ven que "algo se dispara", y dan el visto bueno. Eso da una falsa sensación de seguridad. El fallo real casi siempre aparece al cruzar GA4 con el sistema real del cliente (el formulario del CMS, el CRM, la agenda de reservas...) — ahí es donde se descubre que GA4 mide una fracción mínima de los leads reales, o que está midiendo la cosa equivocada. Esta skill existe para forzar ese cruce, que es el paso que nadie hace.

---

## PASO 0 — Carga de contexto

1. **Lee `memory.md`** para el contexto de Jordi.
2. **Pregunta por el cliente** si no se ha especificado, y lee `clients/[cliente].md` si existe — plataforma web, herramientas de analytics, notas de tracking previas.
3. Confirma acceso: GA4 de la propiedad, Google Tag Manager (todos los contenedores, no solo el que "se supone" que es el activo), y el backend del cliente (WordPress admin, CRM, lo que aplique).

Si falta algún acceso, pídelo antes de avanzar — sin el backend real no se puede completar el Paso 2, que es el que de verdad importa.

---

## FASE 1 — Diagnóstico inicial en GA4

Ve a **Administrar → Eventos** de la propiedad y construye una foto completa:

- Qué eventos están marcados como **Evento clave** ahora mismo, y cuáles no.
- Qué eventos aparecen definidos pero **sin datos de flujo en los últimos 28 días** — son restos de integraciones antiguas (agencia anterior, herramienta que se quitó de la web, campaña que ya no existe). No los toques todavía, solo anótalos.
- Para cada evento con nombre "prometedor" (`Lead_Thank_You_Page`, `form_submit`, `conversion`...), **no des por hecho lo que mide por el nombre**. Comprueba la condición real que lo dispara — puede ser un `page_view` filtrado por URL que coincide con una página que ya no es la única fuente de leads, o puede estar midiendo un formulario completamente distinto al que crees.

No emitas ningún veredicto todavía. Esto es solo inventario.

---

## FASE 2 — Cruce con la fuente de verdad del cliente (el paso crítico)

Antes de confiar en nada de lo visto en GA4, busca dónde vive el **registro real** de conversiones fuera de Analytics:

- Plugin de formularios de WordPress (Elementor Forms → *Envíos*, Gravity Forms → *Entradas*, WPForms, Contact Form 7 + un CRM, etc.)
- CRM o base de datos de reservas/citas.
- Cualquier sistema que reciba el lead independientemente de si el tracking funciona (normalmente el email de notificación al equipo, o la entrada en el propio backend).

**Compara volumen y fechas** de ese registro real contra lo que GA4 dice medir en el mismo periodo:

- Si GA4 mide muchísimo menos que el backend real → hay una fuga de tracking. Esto es la norma, no la excepción, en clientes que nunca han pasado por esta auditoría.
- Coteja **fechas concretas**: coge 2-3 envíos reales del backend con fecha exacta y busca si ese mismo día, en esa misma página, hay algo en GA4. Si no hay nada, confirma que el evento de GA4 no está capturando ese formulario en absoluto.
- Ojo con **formularios homónimos o duplicados**: puede haber más de un formulario con un nombre parecido (una encuesta de satisfacción post-venta con "formulario de contacto" en el nombre, por ejemplo). Identifica cada uno por su ID de widget/formulario, no por el nombre que le puso quien lo creó. El caso real que motivó esta skill: un cliente con 590 envíos históricos de un formulario de leads en WordPress, y GA4 solo registraba 9 eventos en 28 días — porque el evento de GA4 en realidad medía una encuesta de satisfacción distinta, no el formulario de leads.

Si el volumen cuadra razonablemente (±20-30%), anótalo como validado y pasa a la Fase 3 solo para los eventos que no cuadren.

---

## FASE 3 — Auditoría técnica en Google Tag Manager

1. **Busca TODOS los contenedores GTM** presentes en el código fuente de la web (todas las cadenas `GTM-XXXXXXX`), no asumas que solo hay uno. Es habitual encontrar un contenedor de una agencia anterior que sigue cargado sin que nadie lo sepa.
2. Para cada evento que no cuadró en la Fase 2, localiza en GTM qué activador y qué etiqueta lo disparan. La pregunta clave: **¿mide un clic (intención) o una confirmación real de éxito?**
   - Un clic en "Enviar" no es lo mismo que un envío completado — puede fallar la validación del formulario, el reCAPTCHA, o simplemente el usuario cambiar de idea a mitad.
   - Señales de confirmación real: evento de éxito nativo del sistema de formularios (`submit_success` de Elementor Pro, respuesta AJAX 200 de WPForms/Gravity Forms, redirección a página de agradecimiento).
3. Verifica que las integraciones configuradas siguen siendo relevantes **en la web tal como está hoy**, no como estaba cuando se configuró. Ejemplo típico: una etiqueta de Calendly sigue en GTM aunque el cliente quitó Calendly de la web hace meses. Compruébalo navegando la web en vivo, no fiándote de que "la etiqueta existe, luego debe seguir usándose".

---

## FASE 4 — Implementación del fix

Cuando falta la señal de éxito real, el patrón que ha funcionado de forma fiable:

**Listener genérico en GTM** (etiqueta HTML personalizada, disparador "All Pages"), que escuche el evento nativo de éxito del sistema de formularios del cliente y lo empuje al dataLayer con un nombre propio, en vez de depender de que cada página redirija a una thank-you page (muchas páginas de tratamiento/producto no lo hacen, solo muestran un mensaje inline):

```javascript
<script>
(function(){
  function bind(){
    if (window.jQuery) {
      jQuery(document).on('submit_success', '.elementor-form', function(){
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
          event: 'form_submit_success',
          form_id: this.closest('[data-id]')?.getAttribute('data-id') || '',
          form_page_path: window.location.pathname
        });
      });
    } else {
      setTimeout(bind, 300);
    }
  }
  bind();
})();
</script>
```

(Adapta el selector/evento al sistema real del cliente — WPForms, Gravity Forms y Contact Form 7 disparan sus propios eventos jQuery de éxito con nombres distintos; búscalos en su documentación si no es Elementor.)

**Antes de crear el evento de GA4:**
- Comprueba si el ID de medición de GA4 (`G-XXXXXXXXXX`) ya se carga desde OTRO contenedor GTM del sitio (frecuente si hay más de uno, ver Fase 3). Si es así, y vas a crear una etiqueta de configuración de GA4 nueva en el contenedor que sí controlas, añade el parámetro **`send_page_view: false`** para no duplicar el `page_view` en cada carga de página.

**Etiqueta del evento:**
- Tipo "Google Analytics: evento de GA4", nombre de evento recomendado (`generate_lead`, `schedule`, etc. — usa los [nombres recomendados de GA4](https://support.google.com/analytics/answer/9267735) cuando exista uno que encaje).
- Parámetros útiles para poder auditar después: `page_path`, `form_id` o equivalente.

---

## FASE 5 — Verificación obligatoria (no te saltes ningún punto)

Nada se da por bueno sin pasar por aquí:

- [ ] Envío de prueba real con **Vista previa de GTM (Tag Assistant)** — confirma que el dataLayer.push ocurre y que la etiqueta de GA4 se marca como "Completada".
- [ ] Envío de prueba real **también en producción publicada**, no solo en preview — publica el contenedor y repite la prueba fuera del modo debug.
- [ ] Prueba en **más de una página/instancia del formulario** si está duplicado en varias páginas (es habitual que el mismo widget de formulario esté insertado en decenas de páginas de tratamiento/producto). No asumas que funciona igual en todas por haberlo probado una vez.
- [ ] Confirma en **GA4 → Informes en tiempo real** que el evento llega a la propiedad correcta con los parámetros esperados.
- [ ] **Limpia después los envíos de prueba** del sistema real del cliente (borra el lead falso de WordPress/CRM a la papelera). Probablemente disparó un email de notificación real al equipo del cliente — avísales de que fue una prueba, no un lead real, si hace falta.

---

## FASE 6 — Marcar Eventos clave sin duplicar señales

- Marca como Evento clave únicamente lo verificado en la Fase 5, y lo que ya venía funcionando bien de la Fase 2 (canales de contacto directo tipo teléfono/email/WhatsApp suelen estar sanos incluso cuando el formulario no lo está).
- **Alerta de doble conteo:** si ya existía una señal de "clic en enviar" marcada como clave y ahora añades el evento de "envío confirmado", a partir de ahora ambas se dispararán para el mismo lead real. Sumar el total de "Eventos clave" sin desglosar por nombre de evento **duplicará el conteo** de cada lead de formulario. Explícalo con claridad a quien vaya a leer los informes.
- Marcar un evento como clave es **retroactivo** sobre el histórico que ese evento ya tenía recogido. Pero un evento **nuevo** (creado hoy) no tiene datos de antes de existir — no hay manera de reconstruir en GA4 la conversión histórica de una señal que no existía. Si hace falta ese histórico, viene del backend real del cliente (Fase 2), no de GA4.

---

## FASE 7 — Reporting (Looker Studio u otro)

- **Nunca uses un totalizador agregado tipo "Eventos clave" sin desglosar** cuando hay varios canales de conversión (formulario, teléfono, email, WhatsApp, chat...). Mezclarlos en una sola cifra impide saber qué canal aporta qué, y hace la cifra imposible de auditar a simple vista.
- Usa la métrica **"Número de eventos"** (Event count) con un filtro explícito de "Nombre del evento" por canal — es transparente y auditable.
- Evita campos especiales tipo `keyEvents:NombreEvento` como métrica suelta en una tarjeta: en la práctica han dado error de conexión ("Data Studio no se puede conectar a tu conjunto de datos") de forma repetida.
- Al crear tarjetas nuevas, **arrastra el campo directamente desde el panel de Datos** a un hueco vacío del lienzo en vez de duplicar una tarjeta existente y cambiarle la métrica — duplicar y remapear ha dado el mismo error de conexión en la práctica.
- Reutiliza los filtros ya existentes en el informe (p. ej. un filtro de "Medio de la sesión contiene organic" que ya usa el resto del informe) en lugar de crear filtros nuevos redundantes.

---

## FASE 8 — Comunicación al cliente/equipo

Formato: **qué problema hemos detectado → qué solución hemos aplicado**, sin tecnicismos, en primera persona si quien lo envía es Jordi solo.

Puntos que no pueden faltar:
- Las cifras de conversión van a **empezar a aparecer o a cambiar** simplemente porque antes no se medían bien — no perder de vista y dejar muy claro que esto **no significa que haya más negocio real de repente**. Es fácil que el cliente lo malinterprete como una mejora de resultados si no se explica.
- El histórico de antes del fix **no se puede reconstruir en GA4** para la señal nueva. Decir explícitamente dónde SÍ está ese histórico real (el backend del cliente).
- Si las pruebas de verificación llegaron al equipo del cliente por email como leads falsos, una disculpa breve y confirmación de que ya están limpiados.

---

## Guardar en el perfil del cliente

Al terminar, actualiza `clients/[cliente].md` con una sección de tracking (créala si no existe):

```markdown
## Tracking y Conversiones (GA4)

- **GA4 Measurement ID**: G-XXXXXXXXXX
- **Contenedores GTM detectados**: GTM-XXXXXXX (activo/gestionado), GTM-YYYYYYY (externo, sin acceso)
- **Sistema de formularios / backend real**: [Elementor Forms / Gravity Forms / CRM / ...]
- **Eventos clave verificados**: [lista con qué mide cada uno de verdad]
- **Eventos con doble conteo potencial**: [ej. Click Enviar + generate_lead — no sumar juntos]
- **Fecha de arreglo del tracking de formulario**: [fecha] — datos de formulario antes de esta fecha no existen en GA4
- **Próxima revisión sugerida**: [fecha, ej. a los 30 días para confirmar que el volumen cuadra con el backend]
```
