# -*- coding: utf-8 -*-
import io
import scratch_read_ffj_sheet as s

CTA_GENERAL = "Descubre el plan ideal para tu gato en menos de 2 minutos."
CTA_PRECIO = "Calcula el plan de tu gato en menos de 2 minutos."
CTA_RACION = "Calcula el plan de tu gato en menos de 2 minutos."

cierres_ctas = {
42: ("El primer síntoma no está en su plato. Está en su pelo.", CTA_GENERAL),
43: ("No esperes a que el problema vaya a más. Empieza por lo que le pones en el bol.", CTA_GENERAL),
44: ("El cambio se ve. Y se nota.", CTA_GENERAL),
45: ("El problema nunca fue el pelo. Era lo que comía.", CTA_GENERAL),
46: ("Menos pelo por el suelo, más salud en el bol.", CTA_GENERAL),
47: ("Cocinar por él, sin tener que cocinar tú.", CTA_GENERAL),
48: ("La comida casera que no tienes que hacer.", CTA_GENERAL),
49: ("Cuando la comida es de verdad, no hace falta insistir.", CTA_GENERAL),
50: ("Lo que huele a comida real, se come.", CTA_GENERAL),
51: ("Su olfato no se equivoca.", CTA_GENERAL),
52: ("La aceptación empieza por el olor.", CTA_GENERAL),
53: ("Si no lo reconoce como comida, no se lo va a comer.", CTA_GENERAL),
54: ("No adivines. Calcula.", CTA_RACION),
55: ("La ración correcta empieza por saber qué necesita.", CTA_RACION),
56: ("Cada ración, pensada para él. Ni una caloría de más.", CTA_RACION),
57: ("Natural sí, pero verificado.", CTA_GENERAL),
58: ("Completo no es casualidad. Es formulación.", CTA_GENERAL),
59: ("Sus necesidades, calculadas por profesionales.", CTA_GENERAL),
60: ("Nada al azar. Todo pensado para él.", CTA_GENERAL),
61: ("El cambio, sin sobresaltos.", CTA_GENERAL),
62: ("Ir despacio también es una forma de acertar.", CTA_GENERAL),
63: ("Pensado para gatos, hecho por quienes los entienden.", CTA_GENERAL),
64: ("Dale algo pensado para su salud, no para ahorrar costes.", CTA_GENERAL),
65: ("Ahora que lo sé, no hay vuelta atrás.", CTA_GENERAL),
66: ("Sus heces también hablan. Escúchalas.", CTA_GENERAL),
67: ("Una buena digestión empieza por lo que le pones en el bol.", CTA_GENERAL),
68: ("Menos olor, mejor digestión.", CTA_GENERAL),
69: ("Hidratarlo no depende solo de que beba agua.", CTA_GENERAL),
70: ("Que se hidrate comiendo, no solo bebiendo.", CTA_GENERAL),
71: ("No es gastar más. Es invertir en su salud, cada día.", CTA_PRECIO),
72: ("El beneficio se nota, aunque no se vea en el precio.", CTA_PRECIO),
73: ("No es pagar más por lo mismo. Es pagar por algo distinto.", CTA_PRECIO),
74: ("Lo mejor para tu gato, ajustado a lo que realmente necesita.", CTA_PRECIO),
}

rows = sorted(cierres_ctas.keys())
assert rows == list(range(42, 75)), "Faltan filas"

cierre_values = [[cierres_ctas[r][0]] for r in rows]
cta_values = [[cierres_ctas[r][1]] for r in rows]

body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "'VIDEO'!M42:M74", "values": cierre_values},
        {"range": "'VIDEO'!N42:N74", "values": cta_values},
    ],
}

result = s.service.spreadsheets().values().batchUpdate(spreadsheetId=s.SHEET_ID, body=body).execute()

with io.open("scratch_write_ffj_gato_cierre_cta_result.txt", "w", encoding="utf-8") as f:
    f.write(str(result))

print("OK - filas actualizadas:", len(cierre_values))
