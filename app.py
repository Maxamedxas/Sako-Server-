import os
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sako_99_elite_auto_2026")

# --- AI CONFIGURATION ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

# SAKO 99 CORE SYSTEM
instruction = (
    "Magacaaga waa SAKO 99 AI. Waxaad tahay khabiir caalami ah oo Cybersecurity iyo Coding ah. "
    "Magaaladaada waa Mogadishu. Waxaad bixisaa koodh Elite ah (Rust, C++, Java, Python). "
    "Marka koodh lagu weydiiyo, u qor si professional ah oo si toos ah loogu isticmaali karo Termux ama AIDE."
)
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

# LOGIN: User: admin | Key: sako99
users_db = {"admin": generate_password_hash("sako99")}

# --- DASHBOARD UI (THE AUTO-GENERATOR) ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html lang="so">
<head>
    <meta charset="UTF-8">
    <title>SAKO 99 | AUTO-VAULT</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #010409; color: #c9d1d9; font-family: 'Segoe UI', sans-serif; margin: 0; }
        .nav { background: #161b22; border-bottom: 1px solid #30363d; padding: 15px; text-align: center; }
        .container { max-width: 900px; margin: 40px auto; padding: 25px; border: 1px solid #30363d; border-radius: 8px; background: #0d1117; }
        .terminal { background: #000; border: 1px solid #238636; padding: 20px; font-family: 'Consolas', monospace; min-height: 350px; overflow-y: auto; color: #39ff14; border-radius: 6px; margin-bottom: 20px; box-shadow: 0 0 15px rgba(35,134,54,0.2); }
        .cmd-box { display: flex; gap: 10px; }
        input { flex: 1; padding: 12px; background: #010409; border: 1px solid #30363d; color: #fff; border-radius: 4px; outline: none; }
        button { padding: 12px 25px; background: #238636; color: white; border: none; border-radius: 4px; cursor: pointer; font-weight: bold; }
        button:hover { background: #2ea043; }
        .btn-auto { background: #1f6feb; margin-bottom: 15px; width: 100%; display: block; }
    </style>
</head>
<body>
    <div class="nav">
        <h2 style="letter-spacing: 3px; color: #fff;">SAKO 99 ELITE AUTO-ENGINE</h2>
    </div>
    <div class="container">
        <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 20px;">
            <button onclick="auto('Rust Code')" style="background:#d97706;">BUILD RUST</button>
            <button onclick="auto('C++ Code')" style="background:#2563eb;">BUILD C++</button>
            <button onclick="auto('Python Code')" style="background:#059669;">BUILD PYTHON</button>
            <button onclick="auto('Java Code')" style="background:#7c3aed;">BUILD JAVA</button>
        </div>
        <div class="terminal" id="term">[SYSTEM]: Standing by for command...</div>
        <div class="cmd-box">
            <input type="text" id="userInput" placeholder="Geli amarkaaga (tusaale: Ii qor virus scanner Python ah)...">
            <button onclick="execute()">EXECUTE</button>
        </div>
    </div>
    <script>
        async function auto(type) {
            document.getElementById('term').innerText = "[GENERATING]: Fadlan sug, AI-ga ayaa dhisaya " + type + "...";
            execute("Ii qor " + type + " oo professional ah.");
        }
        async function execute(custom = null) {
            let msg = custom || document.getElementById('userInput').value;
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
    if 'username' not in session: return jsonify({"response": "Denied."})
    msg = request.json.get("message", "")
    try:
        response = model.generate_content(msg)
        return jsonify({"response": response.text})
    except:
        return jsonify({"response": "Error connecting to AI server."})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form.get('username')
        pwd = request.form.get('password')
        if user in users_db and check_password_hash(users_db[user], pwd):
            session['username'] = user
            return redirect(url_for('index'))
        return "Access Denied: Key is incorrect."
    
    return render_template_string('''
        <body style="background:#000; color:#fff; display:flex; align-items:center; justify-content:center; height:100vh; font-family:sans-serif;">
            <div style="border:1px solid #30363d; padding:40px; border-radius:8px; text-align:center;">
                <h1 style="letter-spacing:5px;">SAKO 99 VAULT</h1>
                <form method="post">
                    <input name="username" placeholder="IDENTIFIER" required style="display:block; width:100%; margin-bottom:10px; padding:10px; background:#0d1117; border:1px solid #333; color:#fff;"><br>
                    <input type="password" name="password" placeholder="SECURITY KEY" required style="display:block; width:100%; margin-bottom:10px; padding:10px; background:#0d1117; border:1px solid #333; color:#fff;"><br>
                    <button style="width:100%; padding:10px; background:#238636; border:none; color:#fff; cursor:pointer;">GRANT ACCESS</button>
                </form>
            </div>
        </body>
    ''')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run()
