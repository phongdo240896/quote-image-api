from fastapi import FastAPI, Form
from fastapi.responses import FileResponse
from PIL import Image, ImageDraw, ImageFont
import textwrap
import uuid

app = FastAPI()

@app.post("/generate")
def generate_image(title: str = Form(...)):
    width, height = 1080, 1080
    background_color = (31, 31, 31)
    highlight_color = (255, 193, 7)
    text_color = (255, 255, 255)

    img = Image.new('RGB', (width, height), color=background_color)
    draw = ImageDraw.Draw(img)

    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 60)
    margin = 100
    max_chars = 26
    line_height = 90

    formatted = title.upper().replace("**", "|")
    words = formatted.split()
    lines = []
    line = ""
    for word in words:
        test = line + " " + word if line else word
        if len(test) > max_chars:
            lines.append(line)
            line = word
        else:
            line = test
    if line:
        lines.append(line)

    total_height = line_height * len(lines)
    y = (height - total_height) // 2

    for line in lines:
        x = margin
        for word in line.split():
            is_highlight = word.startswith("|") and word.endswith("|")
            w_clean = word.strip("|")
            color = highlight_color if is_highlight else text_color
            draw.text((x, y), w_clean + " ", font=font, fill=color)
            x += draw.textlength(w_clean + " ", font=font)
        y += line_height

    filename = f"/mnt/data/{uuid.uuid4().hex}.png"
    img.save(filename)
    return FileResponse(filename, media_type="image/png")