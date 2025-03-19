# advance bg remove more bg remove
from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image, ImageEnhance
import io

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/remove-bg', methods=['POST'])
def remove_bg():
    if 'file' not in request.files:
        return "No file provided", 400
    file = request.files['file']
    image_data = file.read()

    # Open the image and remove the background
    img = Image.open(io.BytesIO(image_data))
    img = remove(img)

    # Optionally, enhance contrast or brightness to reduce shadow effects
    enhancer = ImageEnhance.Contrast(img)
    img = enhancer.enhance(2)  # Increase contrast; adjust value as needed

    img = img.convert("RGBA")
    datas = img.getdata()

    new_data = []
    for item in datas:
        # Replace shadows (which may be semi-transparent black) with transparency
        if item[3] > 0 and item[:3] == (0, 0, 0):
            new_data.append((255, 255, 255, 0))  # Replace shadow with transparent
        else:
            new_data.append(item)

    img.putdata(new_data)

    # Save the result in a BytesIO object
    img_io = io.BytesIO()
    img.save(img_io, 'PNG')
    img_io.seek(0)

    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    app.run(debug=True)
