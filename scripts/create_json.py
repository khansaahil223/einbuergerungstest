from db import conn
import pytesseract
from PIL import Image
import io
import json

rows = []

for x in conn.execute("select * from questions"):
    y = dict(x)
    
    if y["bundesland"] is None:
        y["bundesland"] = "Allgemein"

    rows.append(y)

for row in rows:
    row["question"] = pytesseract.image_to_string(Image.open(io.BytesIO(row["question_png_bytes"])),lang="deu").replace("\n","")
    del row["question_png_bytes"]

with open("data.json","w", encoding='utf-8') as file:
    json.dump(rows,file,indent=4, ensure_ascii=False)
