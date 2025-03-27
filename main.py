from flask import Flask, request, send_file
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import os

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_image():
    # Lấy tiêu đề từ form
    title = request.form.get('title', 'Không có tiêu đề')

    # Tạo ảnh trắng kích thước 1080x1080
    img = Image.new('RGB', (1080, 1080), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)

    # Đường dẫn font (mặc định hệ thống Ubuntu trên Render)
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"

    # Load font với fallback nếu font không tồn tại
    try:
        font = ImageFont.truetype(font_path, 60)
    except IOError:
        font = ImageFont.load_default()

    # Tính toán vị trí để căn giữa
    text_bbox = draw.textbbox((0, 0), title, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    position = ((1080 - text_width) // 2, (1080 - text_height) // 2)

    # Vẽ text lên ảnh
    draw.text(position, title, fill=(0, 0, 0), font=font)

    # Lưu ảnh vào bộ nhớ
    img_io = BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

# Cần cho Render chạy đúng
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(debug=False, host='0.0.0.0', port=port)
