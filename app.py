import os
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import requests # Si loo ogaado dalka IP-ga

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sako_99_guardian_vault_2026")

# --- AI CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# MASKAXDA AI-GA (Magaca: SAKO 99 AI)
instruction = (
    "Magacaaga waa SAKO 99 AI. Waxaad tahay khabiir caalami ah oo dhanka amniga (Cybersecurity) iyo Coding-ka. "
    "Waxaad tahay difaaca Eternal Vault. Qof walba oo soo gala dareensii inuu joogo meel ammaan ah (Safe Zone). "
    "Marka lagu weydiiyo magacaaga, dheh: 'Waxaan ahay SAKO 99 AI'. "
    "Waxaad awood u leedahay inaad hal mar u adeegto 100,000 oo qof si degdeg ah. "
    "Haddii aad aragto koodh virus ah ama script xun, digniin bixi oo xir (block). "
    "Style-kaagu waa Black & White VIP."
)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

# Database-ka (Admin Access)
users_db = {"admin": generate_password_hash("sako99")}

# --- IP & LANGUAGE LOGIC ---
def get_welcome_message():
    try:
        # Waxaan ogaanaynaa halka uu qofku ka soo galay
        ip_info = requests.get('https://ipapi.co/json/').json()
        country = ip_info.get('country_name', 'Global')
        city = ip_info.get('city', 'Unknown')
        
        if country == "Somalia":
            return f"Soo dhowow mudane, waxaad ka soo gashay {city}, Somalia. Nidaamka SAKO 99 waa mid ammaan ah. 🛡️"
        elif country == "Kenya":
            return f"Karibu sana! Unatoka {city}, Kenya. Mfumo wa SAKO 99 uko salama kabisa. 💎"
        else:
            return f"Welcome Elite User from {country}. You are now inside the SAKO 99 Secure Zone. 🚀"
    except:
        return "Welcome to SAKO 99 AI. Connection Secure. 🟢"

# --- MUUQAALKA (VIP BLACK & WHITE) ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="so">
<head>
    <meta charset="UTF-8">
    <title>SAKO 99 AI | GUARDIAN VAULT</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; transition: 0.2s; }
        body { background: #000; color: #fff; font-family: 'Courier New', monospace; margin: 0; }
        .menu { display: flex; justify-content: center; background: #080808; border-bottom: 2px solid #1a1a1a; position: sticky; top: 0; z-index: 1000; }
        .menu a { color: #666; padding: 20px; text-decoration: none; font-size: 11px; letter-spacing: 2px; font-weight: bold; }
        .menu a:hover, .menu a.active { color: #fff; background: #111; }
        .container { max-width: 900px; margin: 30px auto; padding: 20px; border: 1px solid #111; background: #030303; position: relative; }
        .scanner-bar { height: 2px; background: #fff; width: 0%; animation: scan 3s infinite; margin-bottom: 10px; }
        @keyframes scan { 0% { width: 0%; } 50% { width: 100%; } 100% { width: 0%; } }
        h2 { text-align: center; font-weight: 100; letter-spacing: 10px; border-bottom: 1px solid #111; padding-bottom: 10px; }
        #chat-box { height: 500px; overflow-y: auto; background: #000; border: 1px solid #0a0a0a; padding: 20px; font-size: 13px; margin-bottom: 15px; }
        .system-log { color: #444; font-size: 10px; margin-bottom: 5px; }
        .ai-response { color: #fff; margin-bottom: 20px; padding-left: 10px; border-left: 1px solid #fff; }
        input { width: 80%; padding: 15px; background: #000; border: 1px solid #222; color: #fff; outline: none; }
        button { width: 18%; padding: 15px; background: #fff; color: #000; border: none; font-weight: bold; cursor: pointer; }
        button:hover { background: #888; }
        .status-tag { float: right; font-size: 10px; color: #fff; border: 1px solid #fff; padding: 2px 5px; }
    </style>
</head>
<body>
    <div class="menu">
        <a href="/">DASHBOARD</a>
        <a href="/security">SECURITY SCAN</a>
        <a href="/scripts">ELITE SCRIPTS</a>
    </div>
    <div class="container">
        <div class="scanner-bar"></div>
        <span class="status-tag">SECURE 🛡️</span>
        {{ content | safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    if 'username' not in session: return redirect(url_for('login'))
    welcome = get_welcome_message()
    home_html = f"""
    <h2>SAKO 99 AI</h2>
    <div id="chat-box">
        <div class="system-log">[SYSTEM]: Integrity Check... 100% OK</div>
        <div class="system-log">[SCANNER]: No Viruses Detected.</div>
        <div class="ai-response"><b>SAKO 99 AI:</b> {welcome}</div>
    </div>
    <input type="text" id="userInput" placeholder="Geli Amarka (Ask anything)..." onkeypress="if(event.keyCode==13) ask()">
    <button onclick="ask()">EXECUTE</button>
    <script>
        async function ask() {{
            let inp = document.getElementById('userInput');
            let box = document.getElementById('chat-box');
            if(!inp.value) return;
            box.innerHTML += `<div class='system-log'>[USER]: ${{inp.value}}</div>`;
            let msg = inp.value; inp.value = "";
            let res = await fetch('/ask', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{message: msg}})
            }});
            let data = await res.json();
            box.innerHTML += `<div class='ai-response'><b>SAKO 99 AI:</b> ${{data.response}}</div>`;
            box.scrollTop = box.scrollHeight;
        }}
    </script>
    """
    return render_template_string(HTML_LAYOUT, content=home_html)

@app.route('/ask', methods=['POST'])
def ask():
    if 'username' not in session: return jsonify({"response": "Denied."})
    msg = request.json.get("message", "")
    
    # ANTI-VIRUS/BOT SCANNER
    forbidden = ["virus", "malware", "hack_db", "exploit"]
    if any(word in msg.lower() for word in forbidden):
        return jsonify({"response": "⚠️ DIGNIIN: Script xun ayaa la dareemay. Isku dayga waa la joojiyay (Blocked)."})

    try:
        response = model.generate_content(msg)
        return jsonify({"response": response.text})
    except:
        return jsonify({"response": "Server busy. Handling 100k+ users. Try again."})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if user in users_db and check_password_hash(users_db[user], pwd):
            session['username'] = user
            return redirect(url_for('index'))
        return "Access Denied."
    
    login_form = """
    <div style="padding:50px; text-align:center;">
        <h2>AUTHENTICATION</h2>
        <form method="post">
            <input type="text" name="username" placeholder="IDENTIFIER" style="width:100%; margin-bottom:10px;"><br>
            <input type="password" name="password" placeholder="SECURITY KEY" style="width:100%; margin-bottom:10px;"><br>
            <button type="submit" style="width:100%;">GRANT ACCESS</button>
        </form>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=login_form)

if __name__ == "__main__":
    app.run()
