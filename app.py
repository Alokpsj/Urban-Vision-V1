import os
import sys
import threading
import webbrowser

from flask import Flask, render_template, request
from PIL import Image
from dotenv import load_dotenv
from google import genai

# =========================================================
# PyInstaller-safe resource handling
# =========================================================

def resource_path(relative_path):
    """
    Get absolute path to resource, works for dev and PyInstaller exe
    """
    try:
        base_path = sys._MEIPASS  # PyInstaller temp directory
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

# =========================================================
# Flask Config
# =========================================================

app = Flask(
    __name__,
    template_folder=resource_path("templates"),
    static_folder=resource_path("static")
)

UPLOAD_FOLDER = resource_path("static/uploads")
AFTER_FOLDER = resource_path("static/after")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(AFTER_FOLDER, exist_ok=True)

# =========================================================
# Load .env and initialize Gemini
# =========================================================

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")
print("API KEY FOUND:", bool(API_KEY))

client = genai.Client(api_key=API_KEY)

# =========================================================
# Auto-open browser (for .exe)
# =========================================================

def open_browser():
    webbrowser.open("http://127.0.0.1:5000")

# =========================================================
# Routes
# =========================================================

@app.route("/", methods=["GET", "POST"])
def home():
    report = None
    before_image = None
    after_image = None

    if request.method == "POST":
        file = request.files.get("image")

        if file and file.filename:
            filename = file.filename
            name, ext = os.path.splitext(filename)

            filepath = os.path.join(UPLOAD_FOLDER, filename)
            file.save(filepath)

            # Browser-accessible path
            before_image = f"/static/uploads/{filename}"

            # -------------------------------
            # AFTER IMAGE LOGIC (DEMO MODE)
            # -------------------------------
            after_filename = f"{name}_after{ext}"
            after_path = os.path.join(AFTER_FOLDER, after_filename)

            if os.path.exists(after_path):
                after_image = f"/static/after/{after_filename}"
            else:
                after_image = None

            # -------------------------------
            # Gemini Analysis
            # -------------------------------
            try:
                image = Image.open(filepath)

                response = client.models.generate_content(
                    model="models/gemini-2.5-flash-image",
                    contents=[
                        image,
                        """
You are an Urban Infrastructure Auditor.

Analyze the uploaded image as a real Indian urban street.

Perform a structured Urban Audit covering:
1. Architectural condition
2. Vacant / underutilized spaces
3. Road quality & pedestrian safety
4. Visual clutter (wires, signage, encroachments)
5. Overall livability

Return:
- Key observations
- Identified problems
- Practical improvement suggestions

Format the response clearly with headings.
"""
                    ]
                )

                report = response.text

            except Exception as e:
                report = f"AI ERROR:\n{str(e)}"

    return render_template(
        "index.html",
        report=report,
        before_image=before_image,
        after_image=after_image
    )

# =========================================================
# Main Entry Point
# =========================================================

if __name__ == "__main__":
    try:
        threading.Timer(1.5, open_browser).start()
    except Exception:
        pass

    app.run(host="127.0.0.1", port=5000, debug=False)
