# ================================
# app.py (Flask Backend for Replit)
# ================================
from flask import Flask, request, render_template, send_file, jsonify
import requests
from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import os

app = Flask(__name__)

# ===============
# CONFIGURATION
# ===============
AI_API_KEY = os.getenv("AI_API_KEY")  # set this in Replit Secrets
AI_API_URL = "https://api.openrouter.ai/v1/chat/completions"  # using OpenRouter as example
MODEL = "meta-llama/llama-3.1-70b-instruct"  # Good quality model

# ===============
# HTML TEMPLATES
# ===============
# We'll keep templates simple. Create a 'templates' folder in Replit and add these files.

# templates/index.html:
'''
<!DOCTYPE html>
<html>
<head>
  <title>AI CV Polisher</title>
  <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 flex items-center justify-center min-h-screen">
  <div class="bg-white shadow-xl rounded-2xl p-8 max-w-xl w-full">
    <h1 class="text-2xl font-bold mb-4 text-center">AI CV Polisher</h1>
    <form id="cvForm" class="space-y-4">
      <input class="w-full p-2 border rounded" name="name" placeholder="Your Name" required>
      <textarea class="w-full p-2 border rounded" name="education" placeholder="Education" required></textarea>
      <textarea class="w-full p-2 border rounded" name="experience" placeholder="Work Experience" required></textarea>
      <textarea class="w-full p-2 border rounded" name="skills" placeholder="Skills" required></textarea>
      <input class="w-full p-2 border rounded" name="email" placeholder="Email (optional)">
      <button class="w-full bg-blue-600 text-white p-2 rounded" type="submit">Polish My CV</button>
    </form>
    <div id="result" class="mt-6 hidden">
      <h2 class="text-xl font-bold">Your Polished CV</h2>
      <pre id="cvOutput" class="bg-gray-50 p-4 rounded mt-2 text-sm"></pre>
      <button onclick="unlockAndDownload()" class="w-full bg-green-600 text-white p-2 rounded mt-4">Download as PDF</button>
      <p class="text-center text-gray-500 text-sm mt-2">+ Get a Free Interview Prep Guide</p>
    </div>
  </div>
<script>
const form = document.getElementById('cvForm');
form.addEventListener('submit', async (e) => {
  e.preventDefault();
  const formData = new FormData(form);
  const data = Object.fromEntries(formData.entries());

  const res = await fetch('/process', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data)
  });
  const result = await res.json();
  document.getElementById('cvOutput').textContent = result.polished_cv;
  document.getElementById('result').classList.remove('hidden');
});

function unlockAndDownload(){
  // ===== CONTENT LOCKER PLACEHOLDER =====
  // Replace with CPAGrip content locker script:
  // Example: window.location.href = 'YOUR_LOCKER_URL';
  window.location.href = '/download';
}
</script>
</body>
</html>
'''

# ===============
# BACKEND ROUTES
# ===============
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    prompt = f"Here is the CV info: {data}. Please polish it into a professional CV format. At the end, add one helpful tip to improve job applications."

    headers = {
        "Authorization": f"Bearer {AI_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": MODEL,
        "messages": [{"role": "user", "content": prompt}]
    }

    response = requests.post(AI_API_URL, headers=headers, json=payload)
    polished_cv = response.json()['choices'][0]['message']['content']

    # Save polished CV in session or temp storage
    request.environ['polished_cv'] = polished_cv
    return jsonify({"polished_cv": polished_cv})

@app.route('/download')
def download():
    polished_cv = request.environ.get('polished_cv', 'No CV available')
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    textobject = c.beginText(40, 800)
    for line in polished_cv.split('\n'):
        textobject.textLine(line)
    c.drawText(textobject)
    c.showPage()
    c.save()
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="polished_cv.pdf", mimetype='application/pdf')

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
Fix app.py for Render deployment

  
