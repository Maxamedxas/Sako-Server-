import os
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for

# Magaca 'app' waa in loo isticmaalo sidii Vercel u aqoonsan lahaa
app = Flask(__name__)
app.secret_key = "sako99_vault_2026"

# --- API SETUP ---
# Hubi in GEMINI_API_KEY uu ku jiro Environment Variables-ka Vercel
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

# LOGIN INFO
USER_ID = "admin"
USER_KEY = "sako99"

# --- PREMIUM BLACK & WHITE UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="so">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SAKO 99 PRO</title>
    <style>
        :root { --bg: #000000; --text: #ffffff; --border: #ffffff; }
        body { background-color: var(--bg); color: var(--text); font-family: monospace; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        .header { background: var(--bg); padding: 18px; border-bottom: 2px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
        .logo { font-size: 14px; font-weight: 900; letter-spacing: 4px; }
        .menu-toggle { cursor: pointer; border: 1px solid var(--border); padding: 5px 10px; font-size: 12px; }
        .sidebar { position: fixed; right: -100%; top: 0; width: 100%; height: 100%; background: var(--bg); transition: 0.4s; z-index: 999; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .sidebar.active { right: 0; }
        .sidebar a { font-size: 24px; color: var(--text); text-decoration: none; margin: 15px; letter-spacing: 5px; text-transform: uppercase; }
        .main { flex: 1; padding: 15px; overflow: hidden; display: flex; flex-direction: column; }
        .terminal { flex: 1; border: 1px solid var(--border); padding: 15px; overflow-y: auto; font-size: 11px; white-space: pre-wrap; }
        .footer { padding: 15px; display: flex; gap: 10px; border-top: 1px solid #333; }
        input { flex: 1; background: transparent; border: 1px solid var(--border); color: var(--text); padding: 15px; outline: none; font-family: inherit; }
        .btn { background: var(--text); color: var(--bg); border: none; padding: 0 25px; font-weight: 900; cursor: pointer; text-transform: uppercase; }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">SAKO 99 // CORE</div>
        <div class="menu-toggle" onclick="toggleMenu()">[ MENU ]</div>
    </div>
    <div class="sidebar" id="sidebar">
        <div style="position:absolute; top:20px; right:20px; font-size:30px; cursor:pointer;" onclick="toggleMenu()">×</div>
        <a onclick="setLang('JAVA')">JAVA</a>
        <a onclick="setLang('RUST')">RUST</a>
        <a onclick="setLang('C++')">C++</a>
        <a href="/logout" style="font-size:16px; color:#666;">DISCONNECT</a>
    </div>
    <div class="main">
        <div class="terminal" id="term">READY: SYSTEM ENCRYPTED B&W EDITION.</div>
    </div>
    <div class="footer">
        <input type="text" id="inp" placeholder="ENTER COMMAND..." autocomplete="off">
        <button class="btn" onclick="run()">RUN</button>
    </div>
    <script>
        let lang = "GENERAL";
        function toggleMenu() { document.getElementById('sidebar').classList.toggle('active'); }
        function setLang(l) { lang = l; toggleMenu(); }
        async function run() {
            let i = document.getElementById('inp');
            let t = document.getElementById('term');
            if(!i.value) return;
            t.innerHTML += `<div style="margin-top:10px; color:#888;">> [${lang}]: ${i.value}</div>`;
            let val = i.value; i.value = "";
            let res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({msg: val, lang: lang})
            });
            let data = await res.json();
            t.innerHTML += `<div style="margin-bottom:10px;">${data.response}</div>`;
            t.scrollTop = t.scrollHeight;
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
        response = model.generate_content(f"Mode: {data['lang']}. Task: {data['msg']}")
        return jsonify({"response": response.text})
    except Exception as e:
        return jsonify({"response": "[CONNECTION ERROR]"})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['u'] == USER_ID and request.form['p'] == USER_KEY:
            session['user'] = USER_ID
            return redirect(url_for('home'))
        return "DENIED"
    return render_template_string("""
    <body style="background:#000; color:#fff; display:flex; justify-content:center; align-items:center; height:100vh; margin:0; font-family:monospace;">
        <form method="post" style="border:1px solid #fff; padding:40px; width:280px;">
            <div style="text-align:center; margin-bottom:20px; letter-spacing:3px;">ACCESS KEY</div>
            <input name="u" placeholder="IDENTIFIER" required style="display:block; width:100%; margin-bottom:10px; background:0; border:1px solid #333; color:#fff; padding:12px; box-sizing:border-box;">
            <input type="password" name="p" placeholder="SECURITY KEY" required style="display:block; width:100%; margin-bottom:20px; background:0; border:1px solid #333; color:#fff; padding:12px; box-sizing:border-box;">
            <button style="width:100%; background:#fff; color:#000; border:0; padding:12px; font-weight:bold; cursor:pointer;">GRANT ACCESS</button>
        </form>
    </body>
    """)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=False)
