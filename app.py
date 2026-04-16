import os
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "sako99_vault_2026"

# --- API SETUP ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# LOGIN INFO
USER_ID = "admin"
USER_KEY = "sako99"

# --- GITHUB PRO UI WITH SIDEBAR ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="so">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAKO 99 PRO</title>
    <style>
        body { background-color: #0d1117; color: #c9d1d9; font-family: -apple-system, sans-serif; margin: 0; display: flex; flex-direction: column; height: 100vh; }
        .header { background: #161b22; padding: 12px; border-bottom: 1px solid #30363d; display: flex; justify-content: space-between; align-items: center; z-index: 1000; }
        .menu-btn { font-size: 24px; cursor: pointer; color: #58a6ff; }
        
        /* Sidebar Menu Right */
        .sidebar { position: fixed; right: -250px; top: 0; width: 250px; height: 100%; background: #161b22; border-left: 1px solid #30363d; transition: 0.3s; z-index: 999; padding-top: 60px; }
        .sidebar.active { right: 0; }
        .sidebar a { display: block; padding: 15px 25px; color: #c9d1d9; text-decoration: none; border-bottom: 1px solid #21262d; font-size: 14px; }
        .sidebar a:hover { background: #21262d; color: #58a6ff; }
        .sidebar .category { padding: 10px 25px; font-size: 11px; color: #8b949e; text-transform: uppercase; letter-spacing: 1px; }

        .main { flex: 1; padding: 15px; display: flex; flex-direction: column; }
        .terminal { flex: 1; background: #010409; border: 1px solid #30363d; border-radius: 6px; padding: 15px; overflow-y: auto; font-family: monospace; font-size: 13px; margin-bottom: 10px; }
        .ai-msg { color: #58a6ff; margin-bottom: 15px; }
        .user-msg { color: #8b949e; border-left: 2px solid #238636; padding-left: 10px; margin-bottom: 10px; }
        
        .input-bar { display: flex; gap: 5px; }
        input { flex: 1; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #fff; padding: 12px; outline: none; }
        button { background: #238636; color: #fff; border: none; border-radius: 6px; padding: 0 20px; font-weight: bold; cursor: pointer; }
        
        .overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); z-index: 998; }
        .overlay.active { display: block; }
    </style>
</head>
<body>
    <div class="header">
        <b style="color: #f0f6fc;">SAKO 99 / Core</b>
        <div class="menu-btn" onclick="toggleMenu()">☰</div>
    </div>

    <div class="overlay" id="overlay" onclick="toggleMenu()"></div>
    
    <div class="sidebar" id="sidebar">
        <div class="category">Elite Languages</div>
        <a onclick="setLang('Java')">☕ Java Scripts</a>
        <a onclick="setLang('Rust')">🦀 Rust Scripts</a>
        <a onclick="setLang('C++')">⚙️ C++ Scripts</a>
        <a onclick="setLang('Python')">🐍 Python Scripts</a>
        <div class="category">System</div>
        <a href="/login">👤 Sign Up / Switch</a>
        <a href="/logout" style="color: #f85149;">🚪 Logout</a>
    </div>

    <div class="main">
        <div class="terminal" id="term">
            <div class="ai-msg">[SYSTEM]: SAKO 99 PRO Loaded. Menu is on the right. Select a language or type below.</div>
        </div>
        <div class="input-bar">
            <input type="text" id="userInput" placeholder="Geli amarkaaga...">
            <button onclick="sendMsg()">RUN</button>
        </div>
    </div>

    <script>
        let currentLang = "General";

        function toggleMenu() {
            document.getElementById('sidebar').classList.toggle('active');
            document.getElementById('overlay').classList.toggle('active');
        }

        function setLang(lang) {
            currentLang = lang;
            document.getElementById('term').innerHTML += `<div class="ai-msg">[SYSTEM]: Mode switched to <b>${lang}</b></div>`;
            toggleMenu();
        }

        async function sendMsg() {
            let inp = document.getElementById('userInput');
            let box = document.getElementById('term');
            if(!inp.value) return;

            box.innerHTML += `<div class="user-msg"><b>[${currentLang}]:</b> ${inp.value}</div>`;
            let prompt = `[Language: ${currentLang}] User request: ${inp.value}`;
            inp.value = "";

            let res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({msg: prompt})
            });
            let data = await res.json();
            box.innerHTML += `<div class="ai-msg"><b>SAKO 99:</b><br>${data.response}</div>`;
            box.scrollTop = box.scrollHeight;
        }
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    if 'user' not in session: return redirect(url_for('login'))
    return render_template_string(HTML_TEMPLATE)

@app.route('/ask', methods=['POST'])
def ask():
    user_msg = request.json.get("msg")
    try:
        response = model.generate_content(f"You are SAKO 99 AI. Focus on {user_msg}")
        return jsonify({"response": response.text})
    except:
        return jsonify({"response": "Error: API Key is missing or expired."})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['u'] == USER_ID and request.form['p'] == USER_KEY:
            session['user'] = USER_ID
            return redirect(url_for('home'))
        return "Key Incorrect."
    return render_template_string('''
        <body style="background:#0d1117; color:#fff; text-align:center; padding-top:100px; font-family:sans-serif;">
            <h2>SAKO 99 AUTH</h2>
            <form method="post">
                <input name="u" placeholder="ID" required style="padding:12px; margin-bottom:10px; width:250px;"><br>
                <input type="password" name="p" placeholder="KEY" required style="padding:12px; margin-bottom:10px; width:250px;"><br>
                <button style="padding:12px 40px; background:#238636; color:#fff; border:none; border-radius:6px; cursor:pointer;">SIGN IN</button>
            </form>
        </body>
    ''')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
