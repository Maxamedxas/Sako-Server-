import os
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import requests

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sako_99_guardian_vault_2026")

# --- AI CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# MASKAXDA AI-GA: SAKO 99 AI
instruction = (
    "Magacaaga waa SAKO 99 AI. Waxaad tahay khabiir caalami ah oo ku takhasusay Software Architecture. "
    "Waxaad tahay master-ka luuqadaha Rust, C++, Java, iyo Python. "
    "Marka qofku ku soo galo, si diiran ugu soo dhowee qoraal qurux badan iyo Emojis. "
    "Koodhka aad bixinayso ha noqdo mid professional ah oo leh sharaxaad kooban."
)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

# Database-ka (Identifier: admin | Security Key: sako99)
users_db = {"admin": generate_password_hash("sako99")}

# --- MUUQAALKA (GitHub Dark VIP) ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="so">
<head>
    <meta charset="UTF-8">
    <title>SAKO 99 AI | ELITE VAULT</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: -apple-system, sans-serif; margin: 0; }
        .nav { background: #161b22; border-bottom: 1px solid #30363d; padding: 15px; display: flex; justify-content: center; gap: 30px; }
        .nav a { color: #8b949e; text-decoration: none; font-size: 14px; font-weight: 600; text-transform: uppercase; }
        .nav a:hover { color: #58a6ff; }
        .container { max-width: 900px; margin: 40px auto; padding: 30px; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; box-shadow: 0 8px 24px rgba(0,0,0,0.5); }
        .scan-line { height: 2px; background: #238636; width: 0%; animation: scan 3s infinite; margin-bottom: 15px; }
        @keyframes scan { 0% { width: 0%; } 50% { width: 100%; } 100% { width: 0%; } }
        h2 { border-bottom: 1px solid #21262d; padding-bottom: 10px; font-weight: 200; text-align: center; letter-spacing: 5px; color: #fff; }
        #chat-box, #code-res { height: 400px; overflow-y: auto; background: #010409; border: 1px solid #30363d; border-radius: 6px; padding: 20px; font-family: 'Consolas', monospace; font-size: 13px; color: #d1d5da; margin-bottom: 20px; }
        .ai-msg { color: #58a6ff; margin-bottom: 15px; }
        .sys-log { color: #8b949e; font-size: 11px; margin-bottom: 5px; }
        input, select { width: 78%; padding: 12px; background: #0d1117; border: 1px solid #30363d; color: #fff; border-radius: 6px; outline: none; }
        button { width: 20%; padding: 12px; background: #238636; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
        button:hover { background: #2ea043; }
        .code-section { display: none; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="javascript:void(0)" onclick="show('chat')">AI DASHBOARD</a>
        <a href="javascript:void(0)" onclick="show('code')">CORE TERMINAL</a>
        <a href="/logout" style="color:#f85149;">DESTROY SESSION</a>
    </div>
    <div class="container">
        <div class="scan-line"></div>
        
        <div id="chat-section">
            <h2>SAKO 99 AI DASHBOARD</h2>
            <div id="chat-box">
                <div class="sys-log">[SYSTEM]: Global Uplink Active.</div>
                <div class="ai-msg"><b>SAKO 99 AI:</b> Online. Sideen kuu caawiyaa maanta? 💎</div>
            </div>
            <input type="text" id="userInput" placeholder="Geli fariintaada..." onkeypress="if(event.keyCode==13) ask()">
            <button onclick="ask()">SEND</button>
        </div>

        <div id="code-section" class="code-section">
            <h2>CORE TERMINAL</h2>
            <div id="code-res">Dooro luuqada iyo waxaad rabto inaad dhisid...</div>
            <div style="display:flex; gap:10px;">
                <select id="lang">
                    <option value="Rust">RUST (HIGH SPEED)</option>
                    <option value="C++">C++ (SYSTEM)</option>
                    <option value="Java">JAVA (ENTERPRISE)</option>
                    <option value="Python">PYTHON (AI/AUTO)</option>
                </select>
                <input type="text" id="codeDesc" placeholder="Maxaan kuu qoraa? (tusaale: Virus Scanner)" style="width:55%;">
                <button onclick="buildCode()" style="width:20%;">BUILD</button>
            </div>
        </div>
    </div>

    <script>
        function show(type) {
            document.getElementById('chat-section').style.display = type === 'chat' ? 'block' : 'none';
            document.getElementById('code-section').style.display = type === 'code' ? 'block' : 'none';
        }

        async function ask() {
            let inp = document.getElementById('userInput');
            let box = document.getElementById('chat-box');
            if(!inp.value) return;
            box.innerHTML += `<div class='sys-log'>[USER]: ${{inp.value}}</div>`;
            let res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: inp.value})
            });
            let data = await res.json();
            box.innerHTML += `<div class='ai-msg'><b>SAKO 99 AI:</b> ${{data.response}}</div>`;
            inp.value = ""; box.scrollTop = box.scrollHeight;
        }

        async function buildCode() {
            let lang = document.getElementById('lang').value;
            let desc = document.getElementById('codeDesc').value;
            let resBox = document.getElementById('code-res');
            if(!desc) return;
            resBox.innerHTML = "[COMPILING]: Fadlan sug, koodhkaaga waa la diyaarinayaa...";
            let res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: "Ii qor koodh professional ah oo " + lang + " ah. Waxaa loogu talagalay: " + desc})
            });
            let data = await res.json();
            resBox.innerText = data.response;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def index():
    if 'username' not in session: return redirect(url_for('login'))
    return render_template_string(HTML_LAYOUT)

@app.route('/ask', methods=['POST'])
def ask():
    if 'username' not in session: return jsonify({"response": "Denied."})
    msg = request.json.get("message", "")
    try:
        response = model.generate_content(msg)
        return jsonify({"response": response.text})
    except:
        return jsonify({"response": "Error: Link Lost."})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if user in users_db and check_password_hash(users_db[user], pwd):
            session['username'] = user
            return redirect(url_for('index'))
        return "Key Incorrect."
    
    login_html = """
    <div style="background:#0d1117; height:100vh; display:flex; align-items:center; justify-content:center; flex-direction:column;">
        <h2 style="color:#fff; letter-spacing:10px;">VAULT ACCESS</h2>
        <form method="post" style="width:300px;">
            <input type="text" name="username" placeholder="IDENTIFIER" required style="width:100%; margin-bottom:15px; border:1px solid #30363d;"><br>
            <input type="password" name="password" placeholder="SECURITY KEY" required style="width:100%; margin-bottom:15px; border:1px solid #30363d;"><br>
            <button type="submit" style="width:100%; background:#238636;">ENTER</button>
        </form>
    </div>
    """
    return render_template_string(login_html)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
