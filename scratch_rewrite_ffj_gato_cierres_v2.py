# -*- coding: utf-8 -*-
import io
import scratch_read_ffj_sheet as s

cierres = {
42: "Su piel refleja lo que come cada día. Dale grasas buenas y va a notarse por fuera.",
43: "No dejes que lo que ves por fuera te avise demasiado tarde. Empieza por lo que le pones en el bol.",
44: "Tres semanas. Eso es lo que tarda su pelo en agradecértelo.",
45: "El champú nunca iba a arreglarlo. La comida, sí.",
46: "Un pelo fuerte no se cepilla. Se alimenta.",
47: "La comida que le cocinarías si tuvieras tiempo. Sin tener que encontrarlo.",
48: "Casero, sin encender el fuego.",
49: "Cuando la comida es de verdad, no hay que insistir. Se come sola.",
50: "Su nariz decide antes que su hambre. Dale algo que quiera oler.",
51: "Su instinto no miente. Dale algo que reconozca como comida.",
52: "Si huele a comida de verdad, se lo come. Así de simple.",
53: "Un plato vacío empieza por lo que huele a comida real.",
54: "Deja de calcular a ojo. Nosotros lo hacemos por ti.",
55: "El peso no se controla adivinando. Se controla sabiendo.",
56: "Cada gramo, pensado para él. Ni uno de más.",
57: "Natural, sí. Pero calculado por quien sabe.",
58: "Completo no es casualidad. Es que alguien lo ha calculado bien.",
59: "Lo que su cuerpo necesita, sin dejarlo al azar.",
60: "Nada improvisado. Todo pensado para él.",
61: "Sin sustos, sin rechazo. Solo el cambio hecho bien.",
62: "Ir despacio también es acertar a la primera.",
63: "Pensado para gatos, por quienes de verdad los entienden.",
64: "Dale algo pensado para su salud, no para ahorrar costes de fábrica.",
65: "Ahora que lo sabes, ya no puedes mirar para otro lado.",
66: "Sus heces hablan. Escúchalas antes de que griten.",
67: "Una buena digestión empieza siempre por lo que hay en el bol.",
68: "Menos olor no es casualidad. Es mejor digestión.",
69: "Que beba poco no significa que no necesite hidratarse. Dale agua en cada bocado.",
70: "Si no bebe agua, que se hidrate comiendo.",
71: "Un euro más al día. Muchos años más a su lado.",
72: "El cambio se nota, aunque el precio tarde en justificarse.",
73: "No pagas más por lo mismo. Pagas por algo que de verdad le hace bien.",
74: "Lo mejor para tu gato no tiene por qué costar más de lo que necesita.",
}

rows = sorted(cierres.keys())
assert rows == list(range(42, 75)), "Faltan filas"

values = [[cierres[r]] for r in rows]

body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "'VIDEO'!M42:M74", "values": values},
    ],
}

result = s.service.spreadsheets().values().batchUpdate(spreadsheetId=s.SHEET_ID, body=body).execute()

with io.open("scratch_rewrite_ffj_gato_cierres_v2_result.txt", "w", encoding="utf-8") as f:
    f.write(str(result))

print("OK - filas actualizadas:", len(values))
