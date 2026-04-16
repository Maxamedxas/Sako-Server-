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

USER_ID = "admin"
USER_KEY = "sako99"

# --- BLACK & WHITE UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="so">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SAKO 99 PRO</title>
    <style>
        :root { --bg: #000000; --header: #000000; --border: #ffffff; --text: #ffffff; }
        body { background-color: var(--bg); color: var(--text); font-family: 'Courier New', monospace; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        
        .header { background: var(--header); padding: 15px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; z-index: 1000; }
        .logo { font-size: 14px; font-weight: bold; letter-spacing: 2px; }
        .menu-btn { font-size: 20px; cursor: pointer; color: #fff; border: 1px solid #fff; padding: 2px 8px; border-radius: 4px; }
        
        /* Sidebar Right */
        .sidebar { position: fixed; right: -280px; top: 0; width: 260px; height: 100%; background: #000; border-left: 1px solid #fff; transition: 0.3s; z-index: 999; padding-top: 70px; }
        .sidebar.active { right: 0; }
        .sidebar a { display: block; padding: 15px 25px; color: #fff; text-decoration: none; border-bottom: 1px solid #333; font-size: 13px; text-transform: uppercase; }
        .sidebar a:hover { background: #fff; color: #000; }

        .main-content { flex: 1; display: flex; flex-direction: column; padding: 10px; overflow: hidden; }
        .terminal { flex: 1; background: #000; border: 1px solid #fff; padding: 10px; overflow-y: auto; font-size: 12px; margin-bottom: 10px; }
        .msg { margin-bottom: 10px; border-bottom: 1px dashed #333; padding-bottom: 5px; }
        
        .input-container { display: flex; gap: 5px; background: #000; }
        input { flex: 1; background: #000; border: 1px solid #fff; color: #fff; padding: 12px; font-size: 14px; outline: none; border-radius: 0; }
        .run-btn { background: #fff; color: #000; border: none; padding: 0 20px; font-weight: bold; cursor: pointer; }
        
        .overlay { display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(255,255,255,0.1); z-index: 998; }
        .overlay.active { display: block; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">SAKO 99 // CORE</div>
        <div class="menu-btn" onclick="toggleMenu()">MENU</div>
    </div>

    <div class="overlay" id="overlay" onclick="toggleMenu()"></div>
    
    <div class="sidebar" id="sidebar">
        <a onclick="setMode('Java')">Java</a>
        <a onclick="setMode('Rust')">Rust</a>
        <a onclick="setMode('C++')">C++</a>
        <a onclick="setMode('Python')">Python</a>
        <a href="/logout" style="background: #ff0000; color: #fff; margin-top: 20px;">Logout</a>
    </div>

    <div class="main-content">
        <div class="terminal" id="term">
            <div class="msg">[SYSTEM]: SAKO 99 PRO BLACK & WHITE EDITION ACTIVE.</div>
        </div>
        <div class="input-container">
            <input type="text" id="userInput" placeholder="TYPE COMMAND..." autocomplete="off">
            <button class="run-btn" onclick="send()">RUN</button>
        </div>
    </div>

    <script>
        let mode = "General";
        function toggleMenu() {
            document.getElementById('sidebar').classList.toggle('active');
            document.getElementById('overlay').classList.toggle('active');
        }
        function setMode(m) {
            mode = m;
            document.getElementById('term').innerHTML += `<div class="msg">[MODE]: Switched to ${m}</div>`;
            toggleMenu();
        }
        async function send() {
            let inp = document.getElementById('userInput');
            let term = document.getElementById('term');
            if(!inp.value) return;
            term.innerHTML += `<div class="msg"><b>USER:</b> ${inp.value}</div>`;
            let text = inp.value; inp.value = "";
            let res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({msg: text, mode: mode})
            });
            let data = await res.json();
            term.innerHTML += `<div class="msg"><b>AI:</b><br>${data.reply}</div>`;
            term.scrollTop = term.scrollHeight;
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
    data = request.json
    try:
        response = model.generate_content(f"Mode: {data['mode']}. Request: {data['msg']}")
        return jsonify({"reply": response.text})
    except:
        return jsonify({"reply": "[ERROR]: API CONNECTION FAILED."})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['u'] == USER_ID and request.form['p'] == USER_KEY:
            session['user'] = USER_ID
            return redirect(url_for('home'))
        return "DENIED."
    return render_template_string("""
    <body style="background:#000; color:#fff; font-family:monospace; margin:0; display:flex; justify-content:center; align-items:center; height:100vh;">
        <div style="border:1px solid #fff; padding:40px; width:280px; text-align:center;">
            <h2 style="letter-spacing:4px;">LOGIN</h2>
            <form method="post">
                <input name="u" placeholder="ID" required style="width:100%; padding:10px; margin-bottom:15px; background:#000; border:1px solid #fff; color:#fff;"><br>
                <input type="password" name="p" placeholder="KEY" required style="width:100%; padding:10px; margin-bottom:15px; background:#000; border:1px solid #fff; color:#fff;"><br>
                <button style="width:100%; padding:12px; background:#fff; color:#000; border:none; font-weight:bold; cursor:pointer;">ACCESS</button>
            </form>
        </div>
    </body>
    """)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
