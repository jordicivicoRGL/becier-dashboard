# -*- coding: utf-8 -*-
import io
import scratch_read_ffj_sheet as s

result = s.service.spreadsheets().values().get(spreadsheetId=s.SHEET_ID, range="'VIDEO'!L42:L74").execute()
rows = result.get("values", [])
assert len(rows) == 33

texts = [r[0] if r else "" for r in rows]

# reemplazo global: ingredientes reales -> ingredientes naturales
texts = [t.replace("ingredientes reales", "ingredientes naturales") for t in texts]

# fix especifico fila 45 (indice 3, ya que empieza en fila 42)
idx_45 = 45 - 42
texts[idx_45] = (
    "Gasté meses en champús especiales, cepillos de todo tipo y suplementos, convencida de que el "
    "problema estaba en el pelo de mi gato. Hasta que un día leí de verdad la etiqueta de su pienso: "
    "harinas de subproductos, cereales de relleno, aditivos que ni sabía pronunciar. El pelo no se "
    "arregla por fuera si por dentro no le llega lo que necesita. Desde que cambié a comida cocinada "
    "con ingredientes naturales, no he vuelto a tocar un champú especial."
)

values = [[t] for t in texts]

body = {
    "valueInputOption": "USER_ENTERED",
    "data": [
        {"range": "'VIDEO'!L42:L74", "values": values},
    ],
}

result2 = s.service.spreadsheets().values().batchUpdate(spreadsheetId=s.SHEET_ID, body=body).execute()

with io.open("scratch_fix_reales_naturales_result.txt", "w", encoding="utf-8") as f:
    f.write(str(result2))

print("OK - filas actualizadas:", len(values))
