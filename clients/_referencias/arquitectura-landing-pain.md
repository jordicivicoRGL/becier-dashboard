# Arquitectura tipo para landings de pain

> Fuente: documento interno del jefe de Jordi. No describe ninguna landing existente — es la plantilla de bloques obligatoria para cualquier landing nueva de este arquetipo, usada como checklist antes de dar por cerrada una landing y a la hora de briefear una nueva.
> Redactado pensando en Food for Joe (alergias, cansancio, u otros pains futuros), pero el criterio es general para cualquier cliente cuya landing encaje en el arquetipo descrito abajo — no exclusivo de FFJ.

## Cuándo aplica este arquetipo

- **Tipo de landing**: lead gen de compromiso medio — el formulario (quiz) es de baja fricción, pero desemboca en una decisión de mayor compromiso (suscripción o trial de pago). No es un simple "deja tu email".
- **Temperatura de audiencia**: fría. Llega desde un anuncio de Meta centrado en un síntoma/pain concreto; parte de la audiencia ni siquiera sabe que la causa raíz (ej. la comida) puede estar detrás del síntoma.

Si el proyecto no encaja en este perfil (compromiso medio + audiencia fría + landing centrada en un síntoma/pain concreto), este documento no aplica y la landing sigue el proceso adaptativo normal de la skill.

## Consecuencia para la arquitectura

- Al ser audiencia fría + compromiso medio, la landing necesita bloques de **educación y confianza** antes del CTA — no vale la versión corta de "hero + formulario".
- Cada bloque debe seguir ligado al pain concreto del anuncio (message match), no solo a la marca en general.

---

## 1. Header

**Objetivo**: dar contexto de marca sin distraer del objetivo único de la página.

**Debe contener**
- Logo (enlaza a la web corporativa, no rompe la landing)
- Como mucho, un botón de CTA — el mismo texto que el CTA principal de la página

**Evitar**
- Menú de navegación completo, enlaces a otras secciones de la web, redes sociales — cada enlace de salida es una fuga de conversión

**Por qué**: es tráfico pagado con un único objetivo (completar el quiz); el header no debe ofrecer ninguna salida alternativa.

## 2. Hero / Above the fold

**Objetivo**: que en menos de 5 segundos, sin hacer scroll (mobile primero), el visitante entienda qué se ofrece, a quién y qué tiene que hacer.

**Debe contener**
- Titular que nombra el síntoma/pain de forma literal y reconocible — no una versión abstracta o solo de marca
- Subtítulo que conecta ese síntoma con la causa (la alimentación) y adelanta la solución, en una frase
- Imagen o visual que refuerza el pain (idealmente coherente con el creativo del anuncio que trae el tráfico)
- CTA principal visible sin scroll
- Micro-garantías bajo el CTA (sin permanencia, formulado por veterinarias, envío a domicilio...) — y si existe, mención del trial/precio de entrada

**Notas UX/UI**
- En mobile, el CTA tiene que verse sin necesidad de hacer scroll
- El hero no debe ser solo una imagen grande sin jerarquía de texto clara

**Por qué**: es el primer punto de continuidad con el anuncio — si el titular no refleja el síntoma exacto que motivó el clic, se rompe el message match y sube el rebote.

## 3. Barra de confianza rápida

**Objetivo**: dar credibilidad instantánea antes de que seguir leyendo cueste esfuerzo.

**Debe contener**
- Cifra de mascotas/clientes reales (ej. +X.XXX mascotas)
- % natural / % sin ultraprocesados u otro claim de producto verificable
- Rating agregado si existe (nº de reseñas + valoración media)

**Por qué**: reduce la fricción de "¿esto es de fiar?" antes de invertir tiempo en leer el resto de la página.

## 4. Problema / solución

**Objetivo**: hacer consciente al visitante de una causa que quizá no conocía (que el pienso puede estar detrás del síntoma), antes de presentar la solución o la prueba social.

**Debe contener**
- Explicación breve de por qué el pienso ultraprocesado puede causar o agravar ese síntoma concreto (aditivos, proceso de extrusión, proteínas genéricas, mezclas...)
- Consecuencia de no actuar, sin exagerar hasta sonar alarmista o poco creíble

**Cuándo es obligatorio**: siempre, porque parte de la audiencia no sabe que la alimentación puede ser la causa — sin este bloque, la solución (comida natural) aparece sin justificación para ese segmento.

**Por qué va antes que la prueba social**: en frío, un testimonio solo convence si el visitante ya entiende el mecanismo que ese testimonio confirma — enseñar la prueba antes de explicar la causa le pide que confíe en un resultado sin saber todavía por qué pasa.

**Por qué está en esta landing**: es tráfico frío con distintos niveles de conocimiento del problema; sin agitación explícita justo después del hero, el salto directo a la prueba social o a "la solución es nuestra comida" no convence a quien todavía no ve la conexión pienso-síntoma.

## 5. Prueba social (reseñas/testimonios)

**Objetivo**: que otros validen la promesa concreta de esa landing, ahora que el visitante ya entiende el mecanismo por el que puede funcionar.

**Debe contener**
- Testimonios con nombre y detalle concreto (raza, edad) — nunca genéricos tipo "muy buen servicio"
- Como mínimo 1-2 testimonios que mencionen explícitamente el síntoma/pain de esa landing (picor, energía, digestión...), no solo satisfacción general

**Notas UX/UI**: colocarla justo después del bloque de problema/agitación (primera validación del mecanismo ya explicado) y/o repetida cerca del CTA final.

**Por qué**: en frío, la prueba social específica del síntoma pesa más que la prueba social genérica de marca — pero solo rinde su máximo efecto una vez que el visitante ya sabe por qué el pienso puede causar ese síntoma; de ahí que vaya después del bloque de agitación, no antes.

## 6. Cómo funciona / mecanismo del producto

**Objetivo**: mostrar qué hace el producto y traducir cada característica en un beneficio concreto para el síntoma de esa landing.

**Debe contener**
- 3-5 pasos o características del proceso (ingredientes, cocción, formulación veterinaria, conservación)
- Cada característica traducida a "esto significa que tu perro...", conectado siempre al pain de la landing, no solo a beneficios genéricos de "comida natural"
- Apoyo visual real por paso (foto del proceso, no solo icono) cuando sea posible

**Por qué**: conecta el mecanismo del producto con el síntoma concreto — sin esta traducción, el visitante entiende que la comida es "mejor" en general pero no por qué le sirve a ÉL.

## 7. Antes / después (resultado esperado)

**Objetivo**: visualizar el cambio que se puede esperar, específico del síntoma de esa landing.

**Debe contener**
- 2-3 escenarios de mejora ligados al síntoma (ej. distintos niveles de gravedad o distintos perfiles de perro/edad)
- Si se usa formato "antes/ahora" con fotos: deben ser reales y del mismo perro, o no usarse — es un claim de resultado, no decoración

**Por qué**: ayuda a proyectar el resultado, pero solo si es honesto — un antes/después con fotos de stock o de perros distintos genera el riesgo de credibilidad opuesto al que se busca.

## 8. Producto / Recetas

**Objetivo**: mostrar que la oferta es un producto real y variado, no una promesa abstracta.

**Debe contener**
- Listado de recetas/opciones disponibles, con su ingrediente principal
- Mención de que la selección final se personaliza según el caso de cada perro (conecta con el bloque de proceso, punto 10)

**Por qué**: da concreción a la oferta antes de pedir el formulario — el visitante ve que hay opciones reales detrás del quiz, no solo un plan genérico.

## 9. Oferta detallada (precio / trial / condiciones)

**Objetivo**: eliminar cualquier ambigüedad sobre qué recibe el usuario, cuándo y en qué condiciones, antes de pedirle que dé el paso.

**Debe contener**
- Mención explícita del trial (14 días, mitad de dosis, mitad de precio) y/o de la suscripción mensual
- Condiciones clave: sin permanencia, cómo funciona el envío, cómo cancelar
- Si se puede dar un ancla de precio honesta (ej. "desde X€/día"), mejor que dejarlo completamente abierto

**Notas UX/UI**: no dejar la oferta repartida en frases sueltas por la página — el visitante no debería tener que reconstruirla mentalmente.

**Por qué**: es compromiso medio, no un simple email: si el usuario no sabe qué se compromete a hacer al completar el quiz, es fricción para arrancar el formulario, no solo para pagar al final.

## 10. Cómo funciona el proceso tras el formulario

**Objetivo**: reducir la incertidumbre de "¿qué pasa si relleno esto?" antes de que el usuario le dé al CTA.

**Debe contener**
- 2-3 pasos simples: qué se pregunta en el quiz → cómo se elige la receta → qué recibe el usuario al final

**Por qué**: el formulario pide datos sobre el perro (raza, peso, síntomas); explicar el proceso reduce la sensación de compromiso antes de empezar a rellenarlo.

## 11. Autoridad / equipo

**Objetivo**: reforzar la credibilidad del producto con quién está detrás, especialmente relevante en salud/alimentación animal.

**Debe contener**
- Formulación por veterinarias con nombre y credenciales reales
- Estándares o certificaciones que cumple el producto (ej. FEDIAF)

**Notas UX/UI**: valorar adelantar una versión resumida (badge) a un punto más alto de la página — no hace falta esperar a un bloque dedicado tan abajo para dar la primera señal de autoridad.

**Por qué**: en salud/alimentación, la audiencia fría necesita saber quién avala la recomendación antes de confiar en ella, no solo al final de la página.

## 12. Manejo de objeciones / FAQ

**Objetivo**: responder directamente las dudas que más frenan la conversión en este tipo de producto, antes de que el usuario decida sin esa información.

**Debe contener dos tipos de preguntas, no solo uno**
- Preguntas médicas/de producto: cómo saber si es el pienso, diferencia entre causas, cuándo consultar al veterinario, si sirve para su caso
- Preguntas comerciales: precio, cómo funciona el trial, cómo cancelar, qué pasa si no convence

**Notas UX/UI**: ordenar de más a menos frecuente/importante para la decisión, no como un totum revolutum.

**Por qué**: un FAQ solo médico deja sin resolver las dudas que impiden completar el quiz o convertir el trial; un FAQ solo comercial no genera la confianza que necesita una categoría de salud.

## 13. Garantías / reducción de riesgo

**Objetivo**: bajar la percepción de riesgo justo antes de pedir la acción.

**Debe contener**
- Trial de bajo compromiso (14 días, mitad de precio) presentado como reductor de riesgo, no solo como oferta
- Sin permanencia / cancelación fácil
- Sellos de pago seguro, protección de datos

**Por qué**: el compromiso pedido (suscripción) es mayor que un simple email — sin garantías explícitas cerca del CTA, ese salto de compromiso frena la conversión.

## 14. CTA final

**Objetivo**: dar una última oportunidad de conversión a quien llegó hasta el final de la página sin actuar antes.

**Debe contener**
- Recapitulación breve del valor (una frase), no un CTA seco sin contexto
- Mismo texto de CTA que el resto de la página
- Si hay urgencia real (oferta con fecha límite), mencionarla aquí — nunca urgencia inventada

**Por qué**: cierra la página con una síntesis del argumento completo para quien ha leído todo pero aún no ha actuado.

## 15. Footer

**Objetivo**: cumplimiento legal y contacto, nada más.

**Debe contener**
- Aviso legal, política de privacidad
- Sellos de envío/pago/fabricación si aportan confianza (frío, origen, medios de pago)

**Evitar**
- Enlaces de salida a otras secciones de la web corporativa

---

## Resumen — checklist rápido

Para validar que una landing nueva de este arquetipo está completa, antes de publicarla debería poder responder "sí" a esto:

- ¿El titular nombra el síntoma de forma literal, igual que lo hará el anuncio?
- ¿Hay un bloque que explique por qué el pienso puede causar ese síntoma concreto, para la audiencia que no lo sabe?
- ¿La prueba social menciona el síntoma específico, no solo satisfacción genérica?
- ¿Se explica el trial/precio/condiciones antes del CTA, no solo al final o en ningún sitio?
- ¿Se explica qué pasa después de rellenar el formulario?
- ¿El FAQ cubre tanto dudas médicas como comerciales?
- ¿Todas las fotos de "antes/ahora" y testimonios son reales, no stock ni inventados?
- ¿El CTA usa el mismo texto en toda la página?
