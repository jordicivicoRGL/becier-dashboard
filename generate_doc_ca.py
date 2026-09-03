import base64

html = """<!DOCTYPE html>
<html>
<head><meta charset="UTF-8"></head>
<body>

<h1>Becier: Anàlisi de Performance Google Ads</h1>
<h2>Abril 2026 &mdash; Anàlisi completa</h2>
<p><em>Elaborat per Jordi Civico / Rocket Growth Lab &mdash; 30 d'abril de 2026</em></p>

<hr>

<h2>1. Resum executiu</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Mètrica</th><th>Valor abril</th></tr>
<tr><td>Despesa total</td><td>216,35 €</td></tr>
<tr><td>Pressupost assignat</td><td>~252 € (vehicles 147 + becar 55 + grup 50)</td></tr>
<tr><td>Impressions</td><td>9.143</td></tr>
<tr><td>Clics</td><td>1.110</td></tr>
<tr><td>CTR mitjà compte</td><td>12,14 %</td></tr>
<tr><td>CPC mitjà compte</td><td>0,19 €</td></tr>
<tr><td>Conversions totals</td><td>11</td></tr>
<tr><td>CPL mitjà compte</td><td>19,67 €</td></tr>
</table>

<p>El compte està tècnicament ben configurat per al volum d'Andorra. El CTR del 12% és sòlid. El problema central és que <strong>el 91% de les conversions les genera una sola campanya (Becar)</strong> amb tan sols el 24% de la despesa, mentre que les campanyes de Vehicles concentren el 76% del pressupost i produeixen 1 conversió.</p>
<p>La bona notícia: Becar demostra que el canal funciona. El mercat és petit i els CPC són baixos, fet que fa que els ajustos tinguin impacte ràpid i barat.</p>

<hr>

<h2>2. Rendiment per campanya &mdash; Abril 2026</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr>
<th>Campanya</th><th>Despesa</th><th>Clics</th><th>CTR</th><th>CPC</th><th>Conv.</th><th>CPL</th><th>IS%</th><th>IS perduda rank</th><th>IS perduda budget</th><th>Valoració</th>
</tr>
<tr><td>VEHICLES_BRAND</td><td>6,27 €</td><td>330</td><td>39,3%</td><td>0,02 €</td><td>1</td><td>6,27 €</td><td>55,6%</td><td>31,2%</td><td>13,1%</td><td>✅ Excel·lent</td></tr>
<tr><td>BECAR_GENERIC</td><td>51,71 €</td><td>100</td><td>10,2%</td><td>0,52 €</td><td>10</td><td>5,17 €</td><td>31,2%</td><td>32,5%</td><td>36,4%</td><td>✅ Millor ROI</td></tr>
<tr><td>VEHICLES_GENERIC #2</td><td>92,15 €</td><td>430</td><td>11,9%</td><td>0,21 €</td><td>0</td><td>—</td><td>14,9%</td><td>66,5%</td><td>18,6%</td><td>⚠️ A revisar</td></tr>
<tr><td>PLA-ENGEGA</td><td>30,25 €</td><td>81</td><td>9,5%</td><td>0,37 €</td><td>0</td><td>—</td><td>21,2%</td><td>64,0%</td><td>14,9%</td><td>⚠️ QS crític</td></tr>
<tr><td>VEHICLES_COMPETITORS</td><td>23,09 €</td><td>129</td><td>8,6%</td><td>0,18 €</td><td>0</td><td>—</td><td>10,0%</td><td>63,8%</td><td>28,8%</td><td>⚠️ Canibalització</td></tr>
<tr><td>GRUP-BECIER_GENERIC</td><td>12,88 €</td><td>40</td><td>3,0%</td><td>0,32 €</td><td>0</td><td>—</td><td>23,0%</td><td>46,9%</td><td>30,0%</td><td>🔴 CTR baix</td></tr>
</table>

<hr>

<h2>3. Anàlisi detallada per campanya</h2>

<h3>3.1 SEARCH_TRAFIC_VEHICLES_BRAND — ✅ No tocar (gairebé)</h3>
<p><strong>Què fa bé:</strong> CTR del 39%, CPL de 6,27 €, keywords amb QS 10. És la campanya més eficient del compte per cost per clic (0,02 €). Captura usuaris que ja coneixen la marca i tenen alta intenció.</p>
<p><strong>Problema detectat:</strong> Els termes "becier" i "becier andorra" tenen status NONE (no estan afegits com a keyword explícita) però generen clics. A més, "becier vehicles" apareix com a terme activat també a les campanyes de Competitors i Pla-Engega, generant canibalització interna.</p>
<p><strong>Accions:</strong></p>
<ul>
<li>Afegir "becier" i "becier andorra" com a [exacta]</li>
<li>Afegir "becier vehicles" com a negativa a Competitors i Pla-Engega</li>
<li>Revisar QS 0 de "becier vehicles taller" i "renault becier andorra"</li>
</ul>

<h3>3.2 SEARCH_TRAFIC_BECAR_GENERIC — ✅ L'estrella del compte</h3>
<p><strong>Què fa bé:</strong> 10 conversions amb 51,71 €. CPL de 5,17 € en lloguer de cotxes a Andorra és un resultat excel·lent. CTR sòlid del 10%.</p>
<p><strong>Problema crític — limitada per pressupost:</strong> Està perdent el <strong>36,4% de les impressions disponibles per falta de pressupost</strong>. A CPL de 5,17 €, cada euro addicional hauria de generar aproximadament 0,19 conversions més. És els diners millor invertits de tot el compte.</p>
<p><strong>Problemes de Quality Score:</strong></p>
<ul>
<li>"alquiler vehiculo" PHRASE → QS 0 (genera 1 conversió, però el QS baix encareix el CPC)</li>
<li>"alquiler de coches" BROAD → QS 0 (2 conversions a 0,30 €/conv — eficient malgrat el QS)</li>
<li>"alquiler coche" PHRASE → QS 3</li>
</ul>
<p><strong>Altres problemes:</strong> "avis andorra" (competidor) rep 3 clics i 1,77 € sense conversió. "alquiler furgoneta andorra" té intenció diferent (B2B/comercial) i hauria de tenir el seu propi grup amb landing específica.</p>
<p><strong>Accions:</strong></p>
<ul>
<li><strong>Pujar pressupost de 55 € a 80 € (+25 €) — acció de major retorn de tot el compte</strong></li>
<li>Revisar i actualitzar anuncis per millorar QS de keywords amb puntuació baixa</li>
<li>Crear grup separat per a furgonetes</li>
<li>Afegir "avis", "europcar", "hertz" com a negatives (o crear grup competidors)</li>
</ul>

<h3>3.3 SEARCH_TRAFIC_VEHICLES_GENERIC #2 — ⚠️ Major despesa, 0 conversions</h3>
<p><strong>El problema:</strong> És la campanya amb major despesa (92 €) i 0 conversions. Perd el <strong>66,5% d'impressions per qualitat i ranking</strong>, no per pressupost. Els Quality Scores són el coll d'ampolla.</p>
<p><strong>Quality Scores preocupants:</strong></p>
<ul>
<li>"cotxes km 0" → QS 0 (576 impressions, 64 clics, 13,71 € — despesa sense retorn)</li>
<li>"furgonetes renault" → QS 0</li>
<li>"renting andorra" → QS 10 però 0 conversions (possible problema de landing o intenció)</li>
</ul>
<p><strong>Problema estructural:</strong> Un sol grup d'anuncis barreja tres intencions molt diferents:</p>
<ul>
<li>Compra de vehicle (cotxes de segona mà, cotxes d'ocasió, concessionari)</li>
<li>Marques específiques (renault, dacia, kia, ford, hyundai, seat, citroen, mitsubishi)</li>
<li>Renting i leasing (renting andorra, leasing andorra, renting cotxes)</li>
</ul>
<p>Amb un únic anunci per a totes aquestes intencions, la rellevància cau i el QS pateix. A més, els termes de renting/lloguer canibalitzen Becar.</p>
<p><strong>Hipòtesi sobre 0 conversions:</strong> Amb 430 clics i 0 conversions cal revisar a Analytics la taxa de rebot i el comportament a la landing de vehicles de segona mà. És possible que el trànsit sigui majoritàriament informacional o que el formulari tingui fricció.</p>
<p><strong>Accions:</strong></p>
<ul>
<li>Afegir keywords de renting/lloguer com a negatives (evita overlap amb Becar)</li>
<li>Afegir "buscocotxe" com a negativa (marketplace, intenció diferent al concessionari)</li>
<li>Pausar "cotxes km 0" (QS 0, 13,71 € gastats, 0 conv) fins tenir anunci i landing específics</li>
<li>Verificar funcionament del formulari amb trànsit de segona mà a Analytics</li>
<li><em>A futur:</em> dividir en 3 grups per intenció</li>
</ul>

<h3>3.4 SEARCH_VEHICLES_PLA-ENGEGA_ALL — ⚠️ QS 0 a la keyword principal</h3>
<p><strong>Context:</strong> Campanya de suport al Pla Engega del Govern d'Andorra: subvencions de fins a 4.000 € en turismes elèctrics, 2.500 € en híbrids endollables i 8.500 € en furgonetes. La proposta de valor és molt forta. Vigent fins al juny de 2026.</p>
<p><strong>Problema crític:</strong> La keyword principal "cotxe electric" té <strong>QS 0</strong>. També "cotxes elèctrics" QS 0 i "furgoneta electrica" QS 3. Els anuncis actuals no inclouen aquestes paraules als títols, d'aquí la baixíssima rellevància.</p>
<p><strong>Pèrdua d'IS per ranking: 64%</strong> — pràcticament tot per QS baix.</p>
<p><strong>Altres problemes:</strong></p>
<ul>
<li>Terme "buscocotxe" activant-se — negativa urgent</li>
<li>Terme "becier vehicles" activant-se — no té intenció elèctric/subvenció</li>
<li>"vehicle híbrid" QS 6 amb CTR 4,8% — l'anunci no connecta amb la intenció del cercador</li>
</ul>
<p><strong>Accions:</strong></p>
<ul>
<li>Reescriure anuncis: Títol 1 "Cotxe Elèctric Andorra", Títol 2 "Subvenció fins 4.000 €", Títol 3 "Pla Engega 2026"</li>
<li>Afegir "buscocotxe" i "becier vehicles" com a negatives</li>
<li>Separar elèctrics i híbrids en grups d'anunci distints</li>
<li>Afegir keywords específiques: "subvenció vehicle elèctric andorra", "renault 5 electric andorra", "dacia spring andorra"</li>
</ul>

<h3>3.5 SEARCH_TRAFIC_VEHICLES_COMPETITORS — ⚠️ Canibalització i QS baix</h3>
<p><strong>Problema principal:</strong> "becier vehicles" té status ADDED en aquesta campanya. El compte està pujant contra la seva pròpia marca a la campanya de competidors.</p>
<p><strong>Sobre buscocotxe:</strong> És un marketplace d'anuncis de cotxes. La intenció de l'usuari és navegar llistats, no anar a un concessionari físic. El CTR del 4% en aquests termes ho confirma. Probablement no generarà mai conversions.</p>
<p><strong>Competidors identificats:</strong> buscocotxe, seuwagen, trompo, byd andorra. Els més interessants per mantenir són seuwagen i trompo (competidors directes locals).</p>
<p><strong>Accions:</strong></p>
<ul>
<li>Afegir "becier" i variants com a negatives — urgent</li>
<li>Avaluar pausar keywords de buscocotxe (intenció incorrecta per a conversions)</li>
<li>Reforçar anuncis a seuwagen i trompo amb missatge diferenciador clar</li>
</ul>

<h3>3.6 SEARCH_TRAFIC_GRUP-BECIER_GENERIC — 🔴 Reevaluar</h3>
<p><strong>El problema:</strong> CTR del 3% (el més baix del compte), 1.339 impressions, 0 conversions. No té un objectiu de conversió clar.</p>
<p><strong>Troballa interessant:</strong> La keyword "assegurances" genera 13 clics a 0,43 €/clic. Amb Becier Seguros arrencant al maig, aquesta keyword s'hauria de traslladar a la nova campanya.</p>
<p><strong>Termes "becier" i "becier andorra" amb status NONE</strong> s'estan activant aquí en lloc de a Brand, fragmentant el pressupost.</p>
<p><strong>Accions:</strong></p>
<ul>
<li>Afegir "becier" i "becier andorra" com a negatives per redirigir trànsit a Brand</li>
<li>Moure keyword "assegurances" a Becier Seguros al maig</li>
<li>Considerar reduir pressupost a 20 € i reassignar 30 € a Becar</li>
</ul>

<hr>

<h2>4. Troballes crítiques transversals</h2>

<h3>IS baixa és normal a Andorra</h3>
<p>Una IS del 14-31% en campanyes genèriques és esperable en un mercat de ~77.000 habitants amb inversió baixa. No cal perseguir IS alta; el focus ha d'estar en CPL i qualitat del trànsit.</p>

<h3>Estructura d'un sol grup d'anuncis per campanya</h3>
<p>Totes les campanyes tenen únicament "Grup d'anuncis 1". Barrejar intencions distintes al mateix grup és la causa directa dels QS 0 en múltiples keywords importants. És el problema estructural més costós del compte a llarg termini.</p>

<h3>Canibalització entre campanyes</h3>
<p>Diversos termes activen anuncis en múltiples campanyes alhora, encarint CPCs i fragmentant el pressupost:</p>
<ul>
<li>"becier vehicles" → Brand + Competitors + Pla-Engega</li>
<li>"buscocotxe" → Generic + Competitors</li>
<li>"renting andorra" → Generic + Becar</li>
<li>"dacia andorra" → Generic + Competitors</li>
</ul>

<h3>Keywords NONE sense gestionar</h3>
<p>Termes amb molts clics en status NONE (no afegits explícitament): "becier", "becier andorra", "mazda andorra", "skoda andorra", entre d'altres. S'activen per concordança ampla sense control directe.</p>

<h3>0 conversions a Vehicles: ¿tracking o landing?</h3>
<p>640 clics i 0 conversions a les campanyes de Vehicles. Abans de fer canvis estructurals grans, convé revisar a Analytics: taxa de rebot, temps a la pàgina i embut del formulari per descartar problemes tècnics de tracking.</p>

<hr>

<h2>5. Pla d'acció</h2>

<h3>Accions immediates — Aquesta setmana</h3>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>#</th><th>Acció</th><th>Campanya</th><th>Impacte esperat</th></tr>
<tr><td>1</td><td>Pujar pressupost Becar de 55 € a 80 €</td><td>Becar Generic</td><td>+4-5 conversions/mes estimades a CPL ~5 €</td></tr>
<tr><td>2</td><td>Reescriure anuncis Pla-Engega amb keywords elèctriques als títols</td><td>Pla-Engega</td><td>Millorar QS 0 a keyword principal, reduir CPC</td></tr>
<tr><td>3</td><td>Afegir "becier vehicles" com a negativa</td><td>Competitors + Pla-Engega</td><td>Elimina canibalització, redueix CPCs</td></tr>
<tr><td>4</td><td>Afegir "buscocotxe" com a negativa</td><td>Generic + Pla-Engega</td><td>Elimina trànsit de marketplace de baixa intenció</td></tr>
<tr><td>5</td><td>Afegir "becier" i variants com a negatives</td><td>Competitors + Grup Becier</td><td>Redirigeix trànsit de marca a campanya Brand</td></tr>
<tr><td>6</td><td>Afegir keywords renting/lloguer com a negatives</td><td>Generic #2</td><td>Evita overlap amb Becar, millora rellevància</td></tr>
<tr><td>7</td><td>Verificar funcionament del formulari a Analytics</td><td>Vehicles (totes)</td><td>Confirmar si hi ha problema tècnic de tracking</td></tr>
</table>

<h3>Accions a mig termini — Maig-Juny 2026</h3>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>#</th><th>Acció</th><th>Campanya</th><th>Justificació</th></tr>
<tr><td>1</td><td>Dividir Generic en 3 grups: segona mà | marques | renting</td><td>Generic #2</td><td>Millorar QS, rellevància i conversions</td></tr>
<tr><td>2</td><td>Crear grup "Furgonetes" a Becar</td><td>Becar Generic</td><td>Intenció B2B diferent, mereix anunci i landing propis</td></tr>
<tr><td>3</td><td>Separar Pla-Engega: elèctrics | híbrids | furgonetes</td><td>Pla-Engega</td><td>QS 0 actual requereix més rellevància per segment</td></tr>
<tr><td>4</td><td>Moure keyword "assegurances" a nova campanya Becier Seguros</td><td>Grup Becier → Seguros</td><td>Aprofitar cerca existent en vertical nova</td></tr>
<tr><td>5</td><td>Implementar seguiment de trucades</td><td>Totes</td><td>Conversions de Vehicles poden ser per telèfon i no registrar-se</td></tr>
<tr><td>6</td><td>Reduir Grup Becier Generic a 20 € i reassignar a Becar</td><td>Grup Becier</td><td>CTR 3%, 0 conv — pressupost millor invertit a Becar</td></tr>
</table>

<h3>Nota sobre Becier Seguros (maig)</h3>
<ul>
<li>Keywords base suggerides: "assegurances andorra", "assegurança cotxe andorra", "seguro coche andorra", "seguro moto andorra"</li>
<li>Objectiu: formulari de contacte o trucada directa</li>
<li>Pressupost inicial de 50 €/mes és ajustat però suficient per validar el canal</li>
<li>Competidors a vigilar: AXA Andorra, Crèdit Andorrà Assegurances</li>
</ul>

<hr>

<h2>6. Resum de prioritats</h2>
<table border="1" cellpadding="6" cellspacing="0">
<tr><th>Prioritat</th><th>Acció</th><th>Quan</th></tr>
<tr><td>🔴 Alta</td><td>Pujar pressupost Becar de 55 € a 80 €</td><td>Aquesta setmana</td></tr>
<tr><td>🔴 Alta</td><td>Reescriure anuncis Pla-Engega (QS 0 a keyword principal)</td><td>Aquesta setmana</td></tr>
<tr><td>🟠 Mitja</td><td>Negatives: becier vehicles a Competitors i Pla-Engega</td><td>Aquesta setmana</td></tr>
<tr><td>🟠 Mitja</td><td>Negatives: buscocotxe a totes les campanyes</td><td>Aquesta setmana</td></tr>
<tr><td>🟠 Mitja</td><td>Verificar tracking conversions Vehicles a Analytics</td><td>Aquesta setmana</td></tr>
<tr><td>🟡 Baixa</td><td>Dividir Generic en grups per intenció</td><td>Maig</td></tr>
<tr><td>🟡 Baixa</td><td>Grup furgonetes a Becar</td><td>Maig</td></tr>
<tr><td>🟡 Baixa</td><td>Reduir pressupost Grup Becier i reassignar a Becar</td><td>Maig</td></tr>
</table>

<hr>
<p><em>Document generat amb dades en temps real de la Google Ads API. Període: abril 2026 (mes en curs a data d'extracció: 30/04/2026).</em></p>

</body>
</html>"""

encoded = base64.b64encode(html.encode('utf-8')).decode('utf-8')
print(encoded)
