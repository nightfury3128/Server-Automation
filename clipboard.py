from flask import Flask, request
import pyperclip

app = Flask(__name__)

@app.route("/clipboard", methods=["POST"])
def clipboard():
    text = ""

    # Case 1: JSON from Shortcuts
    if request.is_json:
        data = request.get_json(force=True)
        text = data.get("text", "")

    # Case 2: Raw text (text/plain)
    elif request.data:
        text = request.data.decode("utf-8")

    # Case 3: File/form-data
    elif "file" in request.files:
        file = request.files["file"]
        text = file.read().decode("utf-8")

    if text.strip():
        pyperclip.copy(text)
        print(f"📋 Updated clipboard with: {text[:60]}...")
        return "OK", 200
    else:
        print("⚠️ No text received.")
        return "No text", 400

@app.route("/get_clipboard", methods=["GET"])
def get_clipboard():
    text = pyperclip.paste()
    return text, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
