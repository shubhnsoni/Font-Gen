from flask import Flask, jsonify, request, send_file
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
import base64
import uuid

free_limit = 3
usage = {}
fonts = {}

def create_font_image(prompt: str) -> bytes:
    img = Image.new("RGB", (400, 200), color="white")
    d = ImageDraw.Draw(img)
    text = f"Font for: {prompt}"
    d.text((10, 90), text, fill="black")
    buf = BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

app = Flask(__name__)

@app.route("/")
def home():
    return jsonify(message="FontGen backend is alive! 🚀")


@app.route("/generate", methods=["POST"])
def generate_font():
    data = request.get_json() or {}
    prompt = data.get("prompt")
    api_key = data.get("api_key", "")
    user = api_key or request.remote_addr

    if not prompt:
        return jsonify(error="Prompt required"), 400

    count = usage.get(user, 0)
    if api_key != "premium" and count >= free_limit:
        return jsonify(error="Free limit reached. Upgrade to premium."), 403

    font_data = create_font_image(prompt)
    font_id = str(uuid.uuid4())
    fonts[font_id] = font_data
    usage[user] = count + 1

    preview_b64 = base64.b64encode(font_data).decode("utf-8")
    remaining = None if api_key == "premium" else max(0, free_limit - usage[user])
    return jsonify(font_id=font_id, preview=preview_b64, remaining=remaining)


@app.route("/download/<font_id>")
def download_font(font_id):
    font = fonts.get(font_id)
    if not font:
        return jsonify(error="Font not found"), 404
    return send_file(
        BytesIO(font),
        mimetype="image/png",
        as_attachment=True,
        download_name=f"{font_id}.png",
    )


@app.route("/preview/<font_id>")
def preview_font(font_id):
    font = fonts.get(font_id)
    if not font:
        return jsonify(error="Font not found"), 404
    return send_file(BytesIO(font), mimetype="image/png")


# New route to obtain a public share URL for a generated font
@app.route("/share/<font_id>")
def share_font(font_id):
    """Return a sharable URL that opens the preview in the browser."""
    if font_id not in fonts:
        return jsonify(error="Font not found"), 404
    # Compose full URL to the preview endpoint
    url = request.host_url.rstrip("/") + f"/preview/{font_id}"
    return jsonify(url=url)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050)
