import os
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "sako_99_vault_key_2026")

# --- AI CONFIG ---
API_KEY = os.environ.get("GEMINI_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

model = genai.GenerativeModel('gemini-1.5-flash')

# LOGIN DATA (Direct settings si uusan khalad u dhicin)
USER_ID = "admin"
USER_KEY = "sako99"

# --- GITHUB DARK VIP UI ---
HTML_LAYOUT = """
<!DOCTYPE html>
<html>
<head>
    <title>SAKO 99 | SERVER CORE</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        body { background: #0d1117; color: #c9d1d9; font-family: -apple-system, sans-serif; margin: 0; overflow-x: hidden; }
        .nav { background: #161b22; padding: 15px; border-bottom: 1px solid #30363d; display: flex; gap: 20px; justify-content: center; position: sticky; top: 0; z-index: 100; }
        .nav a { color: #8b949e; text-decoration: none; font-size: 13px; font-weight: 600; cursor: pointer; }
        .nav a:hover { color: #58a6ff; }
        .container { max-width: 900px; margin: 30px auto; padding: 20px; border: 1px solid #30363d; border-radius: 6px; background: #0d1117; }
        .terminal { background: #010409; border: 1px solid #238636; padding: 20px; height: 400px; overflow-y: auto; font-family: 'Consolas', monospace; color: #7ee787; border-radius: 6px; margin-bottom: 20px; box-shadow: inset 0 0 10px #000; }
        .user-line { color: #8b949e; margin-bottom: 5px; }
        .ai-line { color: #58a6ff; margin-bottom: 15px; border-left: 2px solid #58a6ff; padding-left: 10px; }
        .input-area { display: flex; gap: 10px; }
        input { flex: 1; padding: 12px; background: #0d1117; border: 1px solid #30363d; color: #fff; border-radius: 6px; outline: none; }
        input:focus { border-color: #58a6ff; }
        button { padding: 12px 25px; background: #238636; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: bold; }
        button:hover { background: #2ea043; }
        .login-screen { display: flex; flex-direction: column; align-items: center; justify-content: center; height: 80vh; }
        .login-card { background: #161b22; border: 1px solid #30363d; padding: 40px; border-radius: 6px; width: 300px; text-align: center; }
    </style>
</head>
<body>
    <div class="nav">
        <a>DASHBOARD</a>
        <a>SECURITY SCAN</a>
        <a>ELITE SCRIPTS</a>
        <a href="/logout" style="color: #f85149;">LOGOUT</a>
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
    dashboard_html = """
    <h2 style="text-align:center; font-weight: 300; letter-spacing: 3px;">SAKO 99 AI TERMINAL</h2>
    <div class="terminal" id="terminalBox">
        <div style="color: #8b949e;">[SYSTEM]: Booting SAKO 99 Core...</div>
        <div style="color: #8b949e;">[SYSTEM]: Security Protocols Active.</div>
        <div class="ai-line"><b>SAKO 99:</b> Welcome, Admin. Terminal is ready for Elite Scripting. What shall we build today?</div>
    </div>
    <div class="input-area">
        <input type="text" id="userInput" placeholder="Ask for Rust, C++, Java code or FF scripts..." onkeypress="if(event.keyCode==13) send()">
        <button onclick="send()">EXECUTE</button>
    </div>
    <script>
        async function send() {
            let input = document.getElementById('userInput');
            let box = document.getElementById('terminalBox');
            if(!input.value) return;
            
            box.innerHTML += `<div class="user-line"><b>[ADMIN]:</b> ${input.value}</div>`;
            let userVal = input.value;
            input.value = "";
            
            let response = await fetch('/ask', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({prompt: userVal})
            });
            let data = await response.json();
            box.innerHTML += `<div class="ai-line"><b>[SAKO 99]:</b><br>${data.text}</div>`;
            box.scrollTop = box.scrollHeight;
        }
    </script>
    """
    return render_template_string(HTML_LAYOUT, content=dashboard_html)

@app.route('/ask', methods=['POST'])
def ask():
    if 'user' not in session: return jsonify({"text": "Unauthorized Access."})
    prompt = request.json.get("prompt")
    try:
        # Halkan AI-gu wuxuu si otomaatig ah u bixinayaa koodhka
        res = model.generate_content(f"You are SAKO 99 AI. Provide elite code/scripts for: {prompt}")
        return jsonify({"text": res.text})
    except Exception as e:
        return jsonify({"text": "Connection Error: Check API Key."})

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        if request.form['u'] == USER_ID and request.form['p'] == USER_KEY:
            session['user'] = USER_ID
            return redirect(url_for('index'))
        return render_template_string(HTML_LAYOUT, content='<div class="login-screen"><div class="login-card"><h2 style="color:#f85149;">DENIED</h2><p>Incorrect Credentials.</p><a href="/login" style="color:#58a6ff;">Try Again</a></div></div>')
    
    login_html = f"""
    <div class="login-screen">
        <div class="login-card">
            <h2 style="letter-spacing: 5px;">AUTHENTICATION</h2>
            <form method="post">
                <input name="u" placeholder="IDENTIFIER" required style="width:100%; margin-bottom:15px;"><br>
                <input type="password" name="p" placeholder="SECURITY KEY" required style="width:100%; margin-bottom:15px;"><br>
                <button style="width:100%;">GRANT ACCESS</button>
            </form>
        </div>
    </div>
    """
    return render_template_string(HTML_LAYOUT, content=login_html)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 10000)))
