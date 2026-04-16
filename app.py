import os
import requests
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify

app = Flask(__name__)

# API Key
API_KEY = os.environ.get("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# --- BOGGA UGU DHAKHSIYA BADAN (HTML FUDUD) ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="so">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAKO 99 AI - LIGHTSPEED</title>
    <style>
        body { background: #0d1117; color: #39ff14; font-family: 'Courier New', monospace; text-align: center; padding: 50px; }
        .box { border: 2px solid #39ff14; padding: 20px; border-radius: 10px; display: inline-block; background: #161b22; }
        input { background: #0d1117; border: 1px solid #39ff14; color: white; padding: 10px; width: 80%; }
        button { background: #39ff14; color: black; border: none; padding: 10px 20px; cursor: pointer; font-weight: bold; }
        .loading { color: #8b949e; font-size: 12px; }
    </style>
</head>
<body>
    <div class="box">
        <h1>🛡️ SAKO 99 GLOBAL AI</h1>
        <p>Internet-kaagu waa daciif, laakiin anigu waan shaqaynayaa!</p>
        <div id="chat"></div>
        <input type="text" id="msg" placeholder="Qor fariintaada ama koodhka sirta ah...">
        <button onclick="send()">DIR</button>
        <p class="loading">Server is optimized for Low-Bandwidth.</p>
    </div>

    <script>
        async function send() {
            let m = document.getElementById('msg').value;
            let response = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: m})
            });
            let data = await response.json();
            alert(data.response);
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json
    user_msg = data.get("message", "")
    
    # Koodhka Maamulaha
    if "waa sako 610848280" in user_msg.lower():
        return jsonify({"response": "🛡️ SAKO 99 VERIFIED. Server-kaagu waa xaalad wanaagsan, qadkuna hadda waa Lightweight Mode!"})

    ai_response = model.generate_content(user_msg)
    return jsonify({"response": ai_response.text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
