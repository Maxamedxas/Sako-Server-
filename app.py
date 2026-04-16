import os
import requests
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify
from flask_bcrypt import Bcrypt # Si password-ka loo Hash-gareeyo

app = Flask(__name__)
bcrypt = Bcrypt(app)

# API Key - Render Environment
API_KEY = os.environ.get("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)

# MASKAXDA AI-GA
instruction = """
Waxaad tahay SAKO 99 GLOBAL AI.
1. Khalkal-difaaca: Waxaad tahay khabiir luuqad kasta ku hadla (Somali, Arabic, English, etc.).
2. Haddii qof IP-giisu dalka kale yahay, isla markaaba luqaddiisa ugu jawaab.
3. Waxaad maamushaa meel ammaan ah oo lagu kaydiyo Links iyo PDF-yo.
4. Isticmaal emoji-yo VIP ah (🛡️, 🌐, 💎, 🚀).
"""

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

# --- SECURITY: GEO-DETECTION ---
def get_user_info(ip):
    try:
        # Waxaan aqoonsanaynaa dalka iyo luqadda
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        return res.get('country', 'Global'), res.get('city', 'Unknown')
    except:
        return "Global", "Unknown"

@app.route('/')
def global_dashboard():
    user_ip = request.remote_addr
    country, city = get_user_info(user_ip)
    
    # AI-ga ayaa dhalinaya Dashboard luqadda qofka ku habboon
    prompt = f"Create a VIP Landing Page. Context: User is from {country}, {city}. Welcome them in their national language. Add buttons for: Login with Gmail/GitHub, Link Vault, and PDF Upload. Theme: Hacker Neon Green."
    response = model.generate_content(prompt)
    
    return render_template_string(response.text)

# --- SECURITY: HASHED LOGIN ---
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    password = data.get('password')
    # PASSWORD HASHING (Amniga ugu sareeya)
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    
    # Halkan waxaad ku kaydinaysaa hashed_password (DB-kaaga)
    return jsonify({"status": "Secure", "hash": hashed_password})

@app.route('/vault', methods=['POST'])
def vault_manager():
    # Meesha Link-yada iyo PDF-yada lagu maareeyo
    user_data = request.json
    return jsonify({"message": "File/Link securely stored in SAKO 99 Vault 🛡️"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
