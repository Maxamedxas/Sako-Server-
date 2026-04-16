import os
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sako_99_auto_vault")

# --- AI CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# SAKO 99 SYSTEM INSTRUCTION
instruction = (
    "Magacaaga waa SAKO 99 AI. Waxaad tahay nidaam otomaatig ah (Automation Engine). "
    "Hadafkaagu waa inaad si dhakhso ah u soo saarto koodhka Rust, C++, Java, iyo Python adigoon qofka sugin. "
    "Koodhkaagu ha noqdo mid GitHub-style ah oo nadiif ah."
)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

# LOGIN: Identifier: admin | Security Key: sako99
users_db = {"admin": generate_password_hash("sako99")}

# --- DASHBOARD UI (AUTO-GENERATOR) ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="so">
<head>
    <meta charset="UTF-8">
    <title>SAKO 99 | AUTO-DASHBOARD</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #010409; color: #c9d1d9; font-family: -apple-system, sans-serif; margin: 0; }
        .header { background: #161b22; border-bottom: 1px solid #30363d; padding: 20px; text-align: center; }
        .main { max-width: 1000px; margin: 30px auto; padding: 20px; border: 1px solid #30363d; border-radius: 8px; }
        .grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 30px; }
        .card { background: #0d1117; border: 1px solid #30363d; padding: 20px; border-radius: 6px; text-align: center; cursor: pointer; transition: 0.3s; }
        .card:hover { border-color: #58a6ff; background: #161b22; }
        .terminal { background: #000; border: 1px solid #238636; padding: 15px; font-family: monospace; height: 300px; overflow-y: auto; color: #39ff14; }
        input { width: 75%; padding: 12px; background: #0d1117; border: 1px solid #30363d; color: #fff; margin-top: 10px; }
        button { width: 20%; padding: 12px; background: #238636; color: #fff; border: none; cursor: pointer; }
    </style>
</head>
<body>
    <div class="header">
        <h1 style="letter-spacing: 5px;">SAKO 99 AI v6.0</h1>
        <p>Elite Automation & Scripting Engine</p>
    </div>
    <div class="main">
        <div class="grid">
            <div class="card" onclick="autoBuild('Rust')">🚀 BUILD RUST</div>
            <div class="card" onclick="autoBuild('C++')">⚙️ BUILD C++</div>
            <div class="card" onclick="autoBuild('Python')">🐍 BUILD PYTHON</div>
            <div class="card" onclick="autoBuild('Java')">☕ BUILD JAVA</div>
        </div>
        <div class="terminal" id="term">SAKO 99 SYSTEM READY... Waiting for command.</div>
        <input type="text" id="cmd" placeholder="Tusaale: Ii dhis script-ka FF Sensitivity...">
        <button onclick="ask()">EXECUTE</button>
    </div>
    <script>
        async function autoBuild(lang) {
            document.getElementById('term').innerText = "[AUTOMATION]: Generating " + lang + " Elite Script...";
            ask("Ii qor koodh professional ah oo " + lang + " ah.");
        }
        async function ask(customMsg = null) {
            let msg = customMsg || document.getElementById('cmd').value;
            if(!msg) return;
            let res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: msg})
            });
            let data = await res.json();
            document.getElementById('term').innerText = data.response;
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
    msg = request.json.get("message", "")
    try:
        response = model.generate_content(msg)
        return jsonify({"response": response.text})
    except:
        return jsonify({"response": "Error: Link to AI lost."})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if user in users_db and check_password_hash(users_db[user], pwd):
            session['username'] = user
            return redirect(url_for('index'))
        return "Key Incorrect."
    return render_template_string('<div style="background:#000; height:100vh; color:#fff; display:flex; flex-direction:column; align-items:center; justify-content:center;"><h2>VAULT ACCESS</h2><form method="post"><input name="username" placeholder="admin"><br><input type="password" name="password" placeholder="sako99"><br><button>ENTER</button></form></div>')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
