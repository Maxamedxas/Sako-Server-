import os
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "sako99_secret_key"

# --- CONFIG AI ---
# Hubi in magaca 'GEMINI_API_KEY' uu sax ku yahay Vercel
api_key = os.environ.get("GEMINI_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-1.5-flash')

# LOGIN (admin / sako99)
USER_ID = "admin"
USER_KEY = "sako99"

# --- GITHUB MOBILE DARK UI ---
GITHUB_UI = """
<!DOCTYPE html>
<html lang="so">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SAKO 99 | GITHUB CORE</title>
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; margin: 0; }
        .header { background: #161b22; padding: 16px; border-bottom: 1px solid #30363d; display: flex; align-items: center; justify-content: space-between; }
        .header h1 { font-size: 16px; margin: 0; font-weight: 600; }
        .container { padding: 16px; max-width: 500px; margin: auto; }
        .repo-card { background: #0d1117; border: 1px solid #30363d; border-radius: 6px; padding: 16px; margin-bottom: 16px; }
        .terminal { background: #010409; border: 1px solid #30363d; border-radius: 6px; padding: 12px; height: 300px; overflow-y: auto; font-family: ui-monospace, SFMono-Regular, SF Mono, Menlo, monospace; font-size: 12px; color: #7ee787; margin-bottom: 12px; }
        .input-group { display: flex; gap: 8px; }
        input { flex: 1; background: #0d1117; border: 1px solid #30363d; border-radius: 6px; color: #f0f6fc; padding: 8px 12px; font-size: 14px; outline: none; }
        input:focus { border-color: #58a6ff; box-shadow: 0 0 0 3px rgba(31, 111, 235, 0.3); }
        button { background: #238636; color: #ffffff; border: 1px solid rgba(240, 246, 252, 0.1); border-radius: 6px; padding: 8px 16px; font-size: 14px; font-weight: 500; cursor: pointer; }
        button:hover { background: #2ea043; }
        .status-dot { height: 8px; width: 8px; background: #238636; border-radius: 50%; display: inline-block; margin-right: 4px; }
        .login-box { text-align: center; padding-top: 100px; }
    </style>
</head>
<body>
    <div class="header">
        <h1>SAKO 99 / <span>Eternal-Phantom</span></h1>
        <a href="/logout" style="color:#58a6ff; text-decoration:none; font-size:12px;">Logout</a>
    </div>
    <div class="container">
        {{ content | safe }}
    </div>
</body>
</html>
"""

@app.route('/')
def index():
    if 'user' not in session: return redirect(url_for('login'))
    main_content = """
    <div class="repo-card">
        <div style="font-size:12px; margin-bottom:8px;"><span class="status-dot"></span> SAKO 99 AI is Online</div>
        <div class="terminal" id="term">
            [system]: Booting SAKO 99 Core v2000.0...<br>
            [system]: Ready for instructions.
        </div>
        <div class="input-group">
            <input type="text" id="cmd" placeholder="Tusaale: Ii qor koodh Rust ah...">
            <button onclick="askAI()">Run</button>
        </div>
    </div>
    <script>
        async function askAI() {
            let i = document.getElementById('cmd');
            let t = document.getElementById('term');
            if(!i.value) return;
            t.innerHTML += `<div style="color:#8b949e; margin-top:10px;">> ${i.value}</div>`;
            let res = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: i.value})
            });
            let data = await res.json();
            t.innerHTML += `<div style="color:#58a6ff; margin-top:5px;">${data.reply}</div>`;
            i.value = "";
            t.scrollTop = t.scrollHeight;
        }
    </script>
    """
    return render_template_string(GITHUB_UI, content=main_content)

@app.route('/ask', methods=['POST'])
def ask():
    p = request.json.get("prompt")
    try:
        response = model.generate_content(p)
        return jsonify({"reply": response.text})
    except:
        return jsonify({"reply": "Error: API Key is missing or invalid in Vercel settings."})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['u'] == USER_ID and request.form['p'] == USER_KEY:
            session['user'] = USER_ID
            return redirect(url_for('index'))
        return "Access Denied."
    return render_template_string(GITHUB_UI, content='''
        <div class="login-box">
            <h3>Sign in to SAKO 99</h3>
            <form method="post" style="display:flex; flex-direction:column; gap:12px;">
                <input name="u" placeholder="Username" required>
                <input type="password" name="p" placeholder="Password" required>
                <button>Sign in</button>
            </form>
        </div>
    ''')

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
