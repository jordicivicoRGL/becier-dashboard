import base64

html = """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body>

<h1>Informe de Rendimiento Google Ads &mdash; Becier Vehicles &amp; Becar</h1>
<h2>Abril 2026 &mdash; Análisis completo</h2>
<p><em>Elaborado por Jordi Civico / Rocket Growth Lab &mdash; 30 de abril de 2026</em></p>

<hr>

<h2>1. Resumen ejecutivo</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Métrica</th><th>Valor abril</th></tr>
<tr><td>Gasto total</td><td>216,35 €</td></tr>
<tr><td>Presupuesto asignado</td><td>~252 € (vehicles 147 + becar 55 + grup 50)</td></tr>
<tr><td>Impresiones</td><td>9.143</td></tr>
<tr><td>Clics</td><td>1.110</td></tr>
<tr><td>CTR medio cuenta</td><td>12,14 %</td></tr>
<tr><td>CPC medio cuenta</td><td>0,19 €</td></tr>
<tr><td>Conversiones totales</td><td>11</td></tr>
<tr><td>CPL medio cuenta</td><td>19,67 €</td></tr>
</table>

<p>La cuenta está técnicamente bien configurada para el volumen de Andorra. El CTR del 12% es sólido. El problema central es que <strong>el 91% de las conversiones las genera una sola campaña (Becar)</strong> con apenas el 24% del gasto, mientras que las campañas de Vehicles concentran el 76% del presupuesto y producen 1 conversión.</p>
<p>La buena noticia: Becar demuestra que el canal funciona. El mercado es pequeño y los CPC son bajos, lo que hace que los ajustes tengan impacto rápido y barato.</p>

<hr>

<h2>2. Rendimiento por campaña &mdash; Abril 2026</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr>
<th>Campaña</th><th>Gasto</th><th>Clics</th><th>CTR</th><th>CPC</th><th>Conv.</th><th>CPL</th><th>IS%</th><th>IS perdida rank</th><th>IS perdida budget</th><th>Valoración</th>
</tr>
<tr><td>VEHICLES_BRAND</td><td>6,27 €</td><td>330</td><td>39,3%</td><td>0,02 €</td><td>1</td><td>6,27 €</td><td>55,6%</td><td>31,2%</td><td>13,1%</td><td>✅ Excelente</td></tr>
<tr><td>BECAR_GENERIC</td><td>51,71 €</td><td>100</td><td>10,2%</td><td>0,52 €</td><td>10</td><td>5,17 €</td><td>31,2%</td><td>32,5%</td><td>36,4%</td><td>✅ Mejor ROI</td></tr>
<tr><td>VEHICLES_GENERIC #2</td><td>92,15 €</td><td>430</td><td>11,9%</td><td>0,21 €</td><td>0</td><td>—</td><td>14,9%</td><td>66,5%</td><td>18,6%</td><td>⚠️ A revisar</td></tr>
<tr><td>PLA-ENGEGA</td><td>30,25 €</td><td>81</td><td>9,5%</td><td>0,37 €</td><td>0</td><td>—</td><td>21,2%</td><td>64,0%</td><td>14,9%</td><td>⚠️ QS crítico</td></tr>
<tr><td>VEHICLES_COMPETITORS</td><td>23,09 €</td><td>129</td><td>8,6%</td><td>0,18 €</td><td>0</td><td>—</td><td>10,0%</td><td>63,8%</td><td>28,8%</td><td>⚠️ Canibalización</td></tr>
<tr><td>GRUP-BECIER_GENERIC</td><td>12,88 €</td><td>40</td><td>3,0%</td><td>0,32 €</td><td>0</td><td>—</td><td>23,0%</td><td>46,9%</td><td>30,0%</td><td>🔴 CTR bajo</td></tr>
</table>

<hr>

<h2>3. Análisis detallado por campaña</h2>

<h3>3.1 SEARCH_TRAFIC_VEHICLES_BRAND — ✅ No tocar (casi)</h3>
<p><strong>Qué hace bien:</strong> CTR del 39%, CPL de 6,27 €, keywords con QS 10. Es la campaña más eficiente de la cuenta por coste por clic (0,02 €). Captura usuarios que ya conocen la marca y tienen alta intención.</p>
<p><strong>Problema detectado:</strong> Los términos "becier" y "becier andorra" tienen status NONE (no están añadidos como keyword explícita) pero generan clics. Además, "becier vehicles" aparece como término activado también en las campañas de Competitors y Pla-Engega, generando canibalización interna.</p>
<p><strong>Acciones:</strong></p>
<ul>
<li>Añadir "becier" y "becier andorra" como [exacta]</li>
<li>Añadir "becier vehicles" como negativa en Competitors y Pla-Engega</li>
<li>Revisar QS 0 de "becier vehicles taller" y "renault becier andorra"</li>
</ul>

<h3>3.2 SEARCH_TRAFIC_BECAR_GENERIC — ✅ Estrella de la cuenta</h3>
<p><strong>Qué hace bien:</strong> 10 conversiones con 51,71 €. CPL de 5,17 € en alquiler de coches en Andorra es un resultado excelente. CTR sólido del 10%.</p>
<p><strong>Problema crítico — limitada por presupuesto:</strong> Está perdiendo el <strong>36,4% de las impresiones disponibles por falta de presupuesto</strong>. A CPL de 5,17 €, cada euro adicional debería generar aproximadamente 0,19 conversiones más. Es el dinero mejor invertido de toda la cuenta.</p>
<p><strong>Problemas de Quality Score:</strong></p>
<ul>
<li>"alquiler vehiculo" PHRASE → QS 0 (genera 1 conversión, pero el QS bajo encarece el CPC)</li>
<li>"alquiler de coches" BROAD → QS 0 (2 conversiones a 0,30 €/conv — muy eficiente a pesar del QS)</li>
<li>"alquiler coche" PHRASE → QS 3</li>
</ul>
<p><strong>Otros problemas:</strong> "avis andorra" (competidor) recibe 3 clics y 1,77 € sin conversión. "alquiler furgoneta andorra" tiene intención distinta (B2B/comercial) y debería tener su propio grupo con landing específica.</p>
<p><strong>Acciones:</strong></p>
<ul>
<li><strong>Subir presupuesto de 55 € a 80 € (+25 €) — acción de mayor retorno de toda la cuenta</strong></li>
<li>Revisar y actualizar anuncios para mejorar QS de keywords con puntuación baja</li>
<li>Crear grupo separado para furgonetas</li>
<li>Añadir "avis", "europcar", "hertz" como negativas (o crear grupo competidores)</li>
</ul>

<h3>3.3 SEARCH_TRAFIC_VEHICLES_GENERIC #2 — ⚠️ Mayor gasto, 0 conversiones</h3>
<p><strong>El problema:</strong> Es la campaña con mayor gasto (92 €) y 0 conversiones. Pierde el <strong>66,5% de impresiones por calidad y ranking</strong>, no por presupuesto. Los Quality Scores son el cuello de botella.</p>
<p><strong>Quality Scores preocupantes:</strong></p>
<ul>
<li>"cotxes km 0" → QS 0 (576 impresiones, 64 clics, 13,71 € — gasto sin retorno)</li>
<li>"furgonetas renault" → QS 0</li>
<li>"renting andorra" → QS 10 pero 0 conversiones (posible problema de landing o intención)</li>
</ul>
<p><strong>Problema estructural:</strong> Un solo grupo de anuncios mezcla tres intenciones distintas:</p>
<ul>
<li>Compra de vehículo (coches segunda mano, cotxes ocasió, concesionario)</li>
<li>Marcas específicas (renault, dacia, kia, ford, hyundai, seat, citroen, mitsubishi)</li>
<li>Renting y leasing (renting andorra, leasing andorra, renting coches)</li>
</ul>
<p>Con un único anuncio para todas estas intenciones, la relevancia cae y el QS sufre. Además los términos de renting/alquiler canibalizan Becar.</p>
<p><strong>Hipótesis sobre 0 conversiones:</strong> Con 430 clics y 0 conversiones hay que revisar en Analytics la tasa de rebote y el comportamiento en la landing de vehículos usados. Es posible que el tráfico sea mayoritariamente informacional o que el formulario tenga fricción.</p>
<p><strong>Acciones:</strong></p>
<ul>
<li>Añadir keywords de renting/alquiler como negativas (evita overlap con Becar)</li>
<li>Añadir "buscocotxe" como negativa (marketplace, intent diferente al concesionario)</li>
<li>Pausar "cotxes km 0" (QS 0, 13,71 € gastados, 0 conv) hasta tener anuncio y landing específicos</li>
<li>Verificar funcionamiento del formulario con tráfico de segunda mano en Analytics</li>
<li><em>A futuro:</em> dividir en 3 grupos por intención</li>
</ul>

<h3>3.4 SEARCH_VEHICLES_PLA-ENGEGA_ALL — ⚠️ QS 0 en keyword principal</h3>
<p><strong>Contexto:</strong> Campaña de apoyo al Pla Engega del Govern d'Andorra: subvenciones de hasta 4.000 € en turismos eléctricos, 2.500 € en híbridos enchufables y 8.500 € en furgonetas. La propuesta de valor es muy fuerte. Vigente hasta junio 2026.</p>
<p><strong>Problema crítico:</strong> La keyword principal "cotxe electric" tiene <strong>QS 0</strong>. También "cotxes elèctrics" QS 0 y "furgoneta electrica" QS 3. Los anuncios actuales no incluyen estas palabras en los títulos, de ahí la bajísima relevancia.</p>
<p><strong>Pérdida de IS por ranking: 64%</strong> — prácticamente todo por QS bajo.</p>
<p><strong>Otros problemas:</strong></p>
<ul>
<li>Término "buscocotxe" activándose — negativa urgente</li>
<li>Término "becier vehicles" activándose — no tiene intención eléctrico/subvención</li>
<li>"vehicle híbrid" QS 6 con CTR 4,8% — el anuncio no conecta con la intención del buscador</li>
</ul>
<p><strong>Acciones:</strong></p>
<ul>
<li>Reescribir anuncios: Título 1 "Cotxe Elèctric Andorra", Título 2 "Subvenció fins 4.000 €", Título 3 "Pla Engega 2026"</li>
<li>Añadir "buscocotxe" y "becier vehicles" como negativas</li>
<li>Separar eléctricos e híbridos en grupos de anuncio distintos</li>
<li>Añadir keywords específicas: "subvencio vehicle electric andorra", "renault 5 electric andorra", "dacia spring andorra"</li>
</ul>

<h3>3.5 SEARCH_TRAFIC_VEHICLES_COMPETITORS — ⚠️ Canibalización y QS bajo</h3>
<p><strong>Problema principal:</strong> "becier vehicles" tiene status ADDED en esta campaña. La cuenta está pujando contra su propia marca en la campaña de competidores.</p>
<p><strong>Sobre buscocotxe:</strong> Es un marketplace de anuncios de coches. La intención del usuario es navegar listados, no ir a un concesionario físico. El CTR del 4% en estos términos lo confirma. Probablemente no genera conversiones nunca.</p>
<p><strong>Competidores identificados:</strong> buscocotxe, seuwagen, trompo, byd andorra. Los más interesantes para mantener son seuwagen y trompo (competidores directos locales).</p>
<p><strong>Acciones:</strong></p>
<ul>
<li>Añadir "becier" y variantes como negativas — urgente</li>
<li>Evaluar pausar keywords de buscocotxe (intent incorrecto para conversiones)</li>
<li>Reforzar anuncios en seuwagen y trompo con mensaje diferenciador claro</li>
</ul>

<h3>3.6 SEARCH_TRAFIC_GRUP-BECIER_GENERIC — 🔴 Reevaluar</h3>
<p><strong>El problema:</strong> CTR del 3% (el más bajo de la cuenta), 1.339 impresiones, 0 conversiones. No tiene un objetivo de conversión claro.</p>
<p><strong>Hallazgo:</strong> La keyword "assegurances" genera 13 clics a 0,43 €/clic. Con Becier Seguros arrancando en mayo, esta keyword debería trasladarse a la nueva campaña.</p>
<p><strong>Términos "becier" y "becier andorra" con status NONE</strong> se están activando aquí en lugar de en Brand, fragmentando el presupuesto.</p>
<p><strong>Acciones:</strong></p>
<ul>
<li>Añadir "becier" y "becier andorra" como negativas para redirigir tráfico a Brand</li>
<li>Mover keyword "assegurances" a Becier Seguros en mayo</li>
<li>Considerar reducir presupuesto a 20 € y reasignar 30 € a Becar</li>
</ul>

<hr>

<h2>4. Hallazgos críticos transversales</h2>

<h3>IS baja es normal en Andorra</h3>
<p>Una IS del 14-31% en campañas genéricas es esperable en un mercado de ~77.000 habitantes con inversión baja. No hay que perseguir IS alta; el foco debe estar en CPL y calidad del tráfico.</p>

<h3>Estructura de un solo grupo de anuncios por campaña</h3>
<p>Todas las campañas tienen únicamente "Grupo de anuncios 1". Mezclar intenciones distintas en el mismo grupo es la causa directa de los QS 0 en múltiples keywords importantes. Es el problema estructural más costoso de la cuenta a largo plazo.</p>

<h3>Canibalización entre campañas</h3>
<p>Varios términos activan anuncios en múltiples campañas a la vez, encareciendo CPCs y fragmentando el presupuesto:</p>
<ul>
<li>"becier vehicles" → Brand + Competitors + Pla-Engega</li>
<li>"buscocotxe" → Generic + Competitors</li>
<li>"renting andorra" → Generic + Becar</li>
<li>"dacia andorra" → Generic + Competitors</li>
</ul>

<h3>Keywords NONE sin gestionar</h3>
<p>Términos con muchos clics en status NONE (no añadidos explícitamente): "becier", "becier andorra", "mazda andorra", "skoda andorra", entre otros. Se activan por concordancia amplia sin control directo.</p>

<h3>0 conversiones en Vehicles: ¿tracking o landing?</h3>
<p>640 clics y 0 conversiones en campañas de Vehicles. Antes de hacer cambios estructurales grandes, conviene revisar en Analytics: tasa de rebote, tiempo en página y embudo del formulario para descartar problemas técnicos de tracking.</p>

<hr>

<h2>5. Plan de acción</h2>

<h3>Acciones inmediatas — Esta semana</h3>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>#</th><th>Acción</th><th>Campaña</th><th>Impacto esperado</th></tr>
<tr><td>1</td><td>Subir presupuesto Becar de 55 € a 80 €</td><td>Becar Generic</td><td>+4-5 conversiones/mes estimadas a CPL ~5 €</td></tr>
<tr><td>2</td><td>Reescribir anuncios Pla-Engega con keywords eléctricas en títulos</td><td>Pla-Engega</td><td>Mejorar QS 0 en keyword principal, reducir CPC</td></tr>
<tr><td>3</td><td>Añadir "becier vehicles" como negativa</td><td>Competitors + Pla-Engega</td><td>Elimina canibalización, reduce CPCs</td></tr>
<tr><td>4</td><td>Añadir "buscocotxe" como negativa</td><td>Generic + Pla-Engega</td><td>Elimina tráfico de marketplace de baja intención</td></tr>
<tr><td>5</td><td>Añadir "becier" y variantes como negativas</td><td>Competitors + Grup Becier</td><td>Redirige tráfico de marca a campaña Brand</td></tr>
<tr><td>6</td><td>Añadir keywords renting/alquiler como negativas</td><td>Generic #2</td><td>Evita overlap con Becar, mejora relevancia</td></tr>
<tr><td>7</td><td>Verificar funcionamiento del formulario en Analytics</td><td>Vehicles (todas)</td><td>Confirmar si hay problema técnico de tracking</td></tr>
</table>

<h3>Acciones a medio plazo — Mayo-Junio 2026</h3>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>#</th><th>Acción</th><th>Campaña</th><th>Justificación</th></tr>
<tr><td>1</td><td>Dividir Generic en 3 grupos: segunda mano | marcas | renting</td><td>Generic #2</td><td>Mejorar QS, relevancia y conversiones</td></tr>
<tr><td>2</td><td>Crear grupo "Furgonetas" en Becar</td><td>Becar Generic</td><td>Intent B2B distinto, merece anuncio y landing propios</td></tr>
<tr><td>3</td><td>Separar Pla-Engega: eléctricos | híbridos | furgonetas</td><td>Pla-Engega</td><td>QS 0 actual requiere más relevancia por segmento</td></tr>
<tr><td>4</td><td>Mover keyword "assegurances" a nueva campaña Becier Seguros</td><td>Grup Becier → Seguros</td><td>Aprovechar búsqueda existente en vertical nueva</td></tr>
<tr><td>5</td><td>Implementar seguimiento de llamadas</td><td>Todas</td><td>Conversiones de Vehicles pueden ser por teléfono y no registrarse</td></tr>
<tr><td>6</td><td>Reducir Grup Becier Generic a 20 € y reasignar a Becar</td><td>Grup Becier</td><td>CTR 3%, 0 conv — presupuesto mejor invertido en Becar</td></tr>
</table>

<h3>Nota sobre Becier Seguros (mayo)</h3>
<ul>
<li>Keywords base sugeridas: "assegurances andorra", "assegurança cotxe andorra", "seguro coche andorra", "seguro moto andorra"</li>
<li>Objetivo: formulario de contacto o llamada directa</li>
<li>Presupuesto inicial de 50 €/mes es ajustado pero suficiente para validar el canal</li>
<li>Competidores a vigilar: AXA Andorra, Crèdit Andorrà Assegurances</li>
</ul>

<hr>

<h2>6. Resumen de prioridades</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Prioridad</th><th>Acción</th><th>Cuándo</th></tr>
<tr><td>🔴 Alta</td><td>Subir presupuesto Becar de 55 € a 80 €</td><td>Esta semana</td></tr>
<tr><td>🔴 Alta</td><td>Reescribir anuncios Pla-Engega (QS 0 en keyword principal)</td><td>Esta semana</td></tr>
<tr><td>🟠 Media</td><td>Negativas: becier vehicles en Competitors y Pla-Engega</td><td>Esta semana</td></tr>
<tr><td>🟠 Media</td><td>Negativas: buscocotxe en todas las campañas</td><td>Esta semana</td></tr>
<tr><td>🟠 Media</td><td>Verificar tracking conversiones Vehicles en Analytics</td><td>Esta semana</td></tr>
<tr><td>🟡 Baja</td><td>Dividir Generic en grupos por intención</td><td>Mayo</td></tr>
<tr><td>🟡 Baja</td><td>Grupo furgonetas en Becar</td><td>Mayo</td></tr>
<tr><td>🟡 Baja</td><td>Reducir presupuesto Grup Becier y reasignar a Becar</td><td>Mayo</td></tr>
</table>

<hr>
<p><em>Documento generado con datos en tiempo real de la Google Ads API. Periodo: abril 2026 (mes en curso a fecha de extracción: 30/04/2026).</em></p>

</body>
</html>"""

encoded = base64.b64encode(html.encode('utf-8')).decode('utf-8')
print(encoded)
