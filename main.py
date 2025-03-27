
from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
import io
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_image():
    title = request.form.get('title', '').upper()
    if not title:
        return 'Missing title', 400

    # Tạo ảnh
    width, height = 1080, 1080
    image = Image.new("RGB", (width, height), color="#1F1F1F")
    draw = ImageDraw.Draw(image)

    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    font = ImageFont.truetype(font_path, 60)

    # Phân tích nội dung tô vàng bằng **
    words = title.split(" ")
    x, y = 100, 300
    space = draw.textlength(' ', font=font)
    max_width = width - 200

    for word in words:
        color = "#FFFFFF"
        if word.startswith("**") and word.endswith("**"):
            word = word[2:-2]
            color = "#FFC107"

        word_width = draw.textlength(word + " ", font=font)
        if x + word_width > max_width:
            x = 100
            y += 100

        draw.text((x, y), word + " ", font=font, fill=color)
        x += word_width

    # Xuất ra file ảnh
    img_io = io.BytesIO()
    image.save(img_io, 'JPEG', quality=100)
    img_io.seek(0)
    return send_file(img_io, mimetype='image/jpeg')

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
