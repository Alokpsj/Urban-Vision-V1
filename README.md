## Urban Vision AI

**AI-assisted Urban Infrastructure Audit & Restoration Tool**

Urban Vision is a desktop-based web application that uses Google Gemini’s multimodal AI to analyze urban street images and generate structured infrastructure audit reports.  
The project demonstrates how AI can assist urban planners, civic bodies, and architects in identifying safety issues, infrastructural gaps, and improvement opportunities, especially in Indian cities.

---

## Key Features

- Image-based urban street analysis
- AI-generated audit report covering:
  - Architecture condition
  - Pedestrian safety
  - Road quality & traffic flow
  - Visual clutter (wires, signage, encroachments)
  - Livability & urban usability
- Clean web-based UI
- Desktop `.exe` application for easy demo
- Google Gemini API integration (multimodal)

---

## 🛠 Tech Stack

- **Backend:** Python, Flask  
- **AI:** Google Gemini API (Multimodal)  
- **Frontend:** HTML, CSS  
- **Packaging:** PyInstaller  
- **Environment Management:** python-dotenv  

---

## 🚀 How It Works

1. User uploads a street image
2. Image is sent to Google Gemini via API
3. AI analyzes the scene as an Indian urban environment
4. A structured Urban Audit Report is generated and displayed

---

## ▶ Running the App

### Option 1: Desktop App (Recommended)
- Run `app.exe` from the `dist/` folder
- Ensure `.env` is present beside the executable

### Option 2: Development Mode
```bash
>> pip install -r requirements.txt involving flask, google-genai, python-dotenv, pillow
>> python app.py
