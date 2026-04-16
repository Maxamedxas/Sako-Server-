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

# --- PREMIUM BLACK & WHITE UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="so">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>SAKO 99 PRO</title>
    <style>
        :root { --bg: #000000; --text: #ffffff; --border: #ffffff; --hover: #1a1a1a; }
        body { background-color: var(--bg); color: var(--text); font-family: 'SF Mono', 'Courier New', monospace; margin: 0; display: flex; flex-direction: column; height: 100vh; overflow: hidden; }
        
        /* Header Section */
        .header { background: var(--bg); padding: 18px 20px; border-bottom: 2px solid var(--border); display: flex; justify-content: space-between; align-items: center; z-index: 1000; }
        .logo { font-size: 14px; font-weight: 900; letter-spacing: 4px; text-transform: uppercase; }
        .menu-toggle { font-size: 12px; cursor: pointer; border: 1px solid var(--border); padding: 5px 10px; font-weight: bold; }
        
        /* Sidebar Navigation */
        .sidebar { position: fixed; right: -100%; top: 0; width: 100%; height: 100%; background: var(--bg); transition: 0.4s cubic-bezier(0.7, 0, 0.3, 1); z-index: 999; display: flex; flex-direction: column; justify-content: center; align-items: center; }
        .sidebar.active { right: 0; }
        .sidebar a { font-size: 24px; color: var(--text); text-decoration: none; margin: 15px 0; text-transform: uppercase; letter-spacing: 5px; transition: 0.3s; width: 100%; text-align: center; }
        .sidebar a:hover { background: var(--text); color: var(--bg); }
        .close-menu { position: absolute; top: 20px; right: 20px; font-size: 30px; cursor: pointer; }

        /* Terminal Area */
        .main { flex: 1; display: flex; flex-direction: column; padding: 15px; position: relative; }
        .terminal { flex: 1; border: 1px solid var(--border); background: var(--bg); padding: 15px; overflow-y: auto; font-size: 11px; line-height: 1.6; }
        .msg-line { margin-bottom: 12px; border-left: 1px solid #333; padding-left: 10px; }
        .ai-label { color: #888; text-transform: uppercase; font-size: 9px; margin-bottom: 4px; display: block; }
        
        /* Input System */
        .footer { padding: 15px; border-top: 1px solid #333; display: flex; gap: 10px; }
        input { flex: 1; background: transparent; border: 1px solid var(--border); color: var(--text); padding: 15px; font-family: inherit; font-size: 14px; outline: none; }
        .btn-run { background: var(--text); color: var(--bg); border: none; padding: 0 25px; font-weight: 900; text-transform: uppercase; cursor: pointer; }

        /* Scrollbar */
        ::-webkit-scrollbar { width: 3px; }
        ::-webkit-scrollbar-thumb { background: var(--border); }
    </style>
</head>
<body>
    <div class="header">
        <div class="logo">SAKO 99 // CORE</div>
        <div class="menu-toggle" onclick="toggleSidebar()">[ MENU ]</div>
    </div>

    <div class="sidebar" id="sidebar">
        <div class="close-menu" onclick="toggleSidebar()">×</div>
        <a onclick="setLang('JAVA')">JAVA</a>
        <a onclick="setLang('RUST')">RUST</a>
        <a onclick="setLang('C++')">C++</a>
        <a onclick="setLang('PYTHON')">PYTHON</a>
        <a href="/logout" style="color: #666; font-size: 16px;">DISCONNECT</a>
    </div>

    <div class="main">
        <div class="terminal" id="terminal">
            <div class="msg-line">
                <span class="ai-label">System Initialized</span>
                STATUS: ENCRYPTED B&W INTERFACE READY.
            </div>
        </div>
    </div>

    <div class="footer">
        <input type="text" id="userInput" placeholder="ENTER COMMAND..." onkeypress="handleKey(event)">
        <button class="btn-run" onclick="execute()">RUN</button>
    </div>

    <script>
        let currentLang = "GENERAL";

        function toggleSidebar() {
            document.getElementById('sidebar').classList.toggle('active');
        }

        function setLang(lang) {
            currentLang = lang;
            document.getElementById('terminal').innerHTML += `<div class="msg-line"><span class="ai-label">Protocol Update</span>ENVIRONMENT SET TO: ${lang}</div>`;
            toggleSidebar();
        }

        function handleKey(e) { if(e.key === 'Enter') execute(); }

        async function execute() {
            let inp = document.getElementById('userInput');
            let term = document.getElementById('terminal');
            if(!inp.value) return;

            term.innerHTML += `<div class="msg-line" style="border-left-color: #fff;"><b>> ${inp.value}</b></div>`;
            let val = inp.value; inp.value = "";
            term.scrollTop = term.scrollHeight;

            let res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({msg: val, lang: currentLang})
            });
            let data = await res.json();
            term.innerHTML += `<div class="msg-line"><span class="ai-label">SAKO 99 Response</span>${data.response}</div>`;
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
        # Halkan AI-ga ayaa loogu sheegayaa luuqadda uu isticmaalayo
        prompt = f"Mode: {data['lang']}. Task: {data['msg']}"
        response = model.generate_content(prompt)
        return jsonify({"response": response.text})
    except:
        return jsonify({"response": "CONNECTION ERROR: CHECK SYSTEM STATUS."})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['u'] == USER_ID and request.form['p'] == USER_KEY:
            session['user'] = USER_ID
            return redirect(url_for('home'))
        return "DENIED."
    return render_template_string("""
    <body style="background:#000; color:#fff; font-family:monospace; display:flex; justify-content:center; align-items:center; height:100vh; margin:0;">
        <div style="border:1px solid #fff; padding:40px; width:300px;">
            <div style="text-align:center; margin-bottom:30px; letter-spacing:5px; font-weight:bold;">SAKO 99 ACCESS</div>
            <form method="post">
                <input name="u" placeholder="IDENTIFIER" required style="width:100%; background:transparent; border:1px solid #333; color:#fff; padding:12px; margin-bottom:15px; outline:none; box-sizing:border-box;">
                <input type="password" name="p" placeholder="SECURITY KEY" required style="width:100%; background:transparent; border:1px solid #333; color:#fff; padding:12px; margin-bottom:20px; outline:none; box-sizing:border-box;">
                <button style="width:100%; background:#fff; color:#000; border:none; padding:15px; font-weight:bold; cursor:pointer; letter-spacing:2px;">GRANT ACCESS</button>
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
