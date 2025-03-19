import os
from flask import Flask, render_template, request, send_file
from rembg import remove
from PIL import Image
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
    output = remove(img)
    
    # Save the result in a BytesIO object
    img_io = io.BytesIO()
    output.save(img_io, 'PNG')
    img_io.seek(0)
    
    return send_file(img_io, mimetype='image/png')

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Use Render's assigned port or default to 10000
    app.run(host="0.0.0.0", port=port)  # Bind to 0.0.0.0 for external access
