# Lin Barcelona

Consultora especializada en metodología Lean aplicada al sector salud (lin.barcelona / Lin by Leanfontcus, +16 años de experiencia). Ayudan a hospitales y centros sanitarios a rediseñar procesos clínicos para ganar eficiencia sin perder foco en el paciente.

## Proyecto: dashboard de seguimiento de proyecto Lean

Caso de demostración para enseñar a un cliente final (un hospital): **HUMS**, sobre el circuito de trasplantamiento renal de donante vivo y derivación de pacientes ERCA.

- El punto de partida es la plantilla Excel "Seguiment del projecte (cronograma i indicadors)" (Vertex42 Gantt template adaptado), con dos hojas: **Cronograma** (propuestas de mejora → acciones → responsable → progreso 0/50/100% → fechas) e **Indicadors** (KPI con punto de partida, objetivo, responsable, fuente, frecuencia y seguimiento mensual/trimestral).
- Los datos viven en Google Sheets (no en el Excel local) para que el dashboard los lea en vivo: `1-8CarQuUiUSsb0JU1n9NXVThCaERngfTCEhBxqtrWBc`, pestañas `Cronograma` / `Indicadors` / `Acerca de`.
- Se rellenó con un caso realista de ejemplo (10 acciones repartidas en 5 propuestas de mejora, 5 indicadores) para que el dashboard no se vea vacío en la demo.

## Dashboard

`dashboard_lin_barcelona.py` — Streamlit, mismo estilo dark que Becier/DCORE pero con paleta neutra (acento teal `#14b8a6`, sin colores de plataformas Ads porque no es un dashboard de Ads).

Secciones: KPIs globales (acciones totales/fetes/en procés/pendents/indicadors monitoritzats), Gantt de acciones (plotly, coloreado por estado), tabla de acciones, desglose por responsable, desglose por propuesta de mejora, tarjetas de indicadores con evolución mensual/trimestral vs línea de objetivo (verde si va en la dirección correcta, rojo si no).

Lanzar con:
```
streamlit run dashboard_lin_barcelona.py --server.port 8502
```
Configurado en `.claude/launch.json` como `lin-barcelona-dashboard`.

## Notas técnicas

- Fetch de Google Sheets con doble lectura (`FORMATTED_VALUE` para etiquetas/meses/texto tipo "feb-26" o "45%", `UNFORMATTED_VALUE` para los valores numéricos mensuales) — necesario porque Sheets auto-formatea celdas con "%" como fracción y las fechas como serial en unformatted.
- El Gantt usa `go.Bar` horizontal con `base` en fecha ISO y `x` en milisegundos (no días) porque Plotly con eje de tipo fecha necesita la duración en ms para que las barras se dibujen.
- Rango de lectura del Cronograma limitado a `B11:G30` para no capturar la fila de instrucciones de la plantilla original ("Esta fila indica el final de la programación...").
