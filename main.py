from flask import Flask, request, jsonify
from PIL import Image
import requests
from io import BytesIO

app = Flask(__name__)

@app.route('/process', methods=['GET'])
def process():
    image_url = request.args.get('url')
    if not image_url:
        return jsonify({"error": "Image URL not provided"}), 400

    try:
        response = requests.get(image_url)
        response.raise_for_status()
        image = Image.open(BytesIO(response.content))
        width, height = image.size
        colors = []

        for x in range(width):
            for y in range(height):
                r, g, b = image.getpixel((x, y))
                colors.append({"x": x, "y": y, "color": {"r": r, "g": g, "b": b}})

        return jsonify({"width": width, "height": height, "colors": colors})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
