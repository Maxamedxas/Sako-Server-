import os
import requests
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# API Key
API_KEY = os.environ.get("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)

# --- DATABASE KMG AH (Stats & Storage) ---
server_stats = {
    "total_visits": 0,
    "countries": set(),
    "actions_performed": []
}
cached_dashboard = None # Kaydka Dashboard-ka si uu u dhakhsado

# MASKAXDA AI-GA
instruction = """
Waxaad tahay SAKO 99 GLOBAL AI.
1. Maamule Sare: Haddii la qoro 'waa sako 610848280', bixi warbixin qarsoodi ah oo VIP ah.
2. Naqshadda: Bogga hore ka dhig mid GitHub-ka oo kale u qurux badan (Dark Mode, Professional, Neon Accents).
3. Luqadda: Qof kasta dalkiisa iyo luqaddiisa ugu jawaab.
4. Shaqada: Maamul Link Vault iyo Recycle Bin si hufan.
"""

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

def get_geo_info(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = res.get('country', 'Global')
        server_stats["countries"].add(country)
        return country
    except:
        return "Global"

@app.route('/')
def home():
    global cached_dashboard
    server_stats["total_visits"] += 1
    user_ip = request.remote_addr
    country = get_geo_info(user_ip)
    
    # Haddii Dashboard-ka horay loo dhisay, isla markiiba soo saar si uu u dhakhsado
    if not cached_dashboard:
        prompt = f"""
        Create a High-End Dashboard for SAKO 99. 
        Theme: Professional GitHub Dark Style with Neon Green highlights.
        User Context: From {country}. 
        Sections: Repository-style 'Link Vault', 'Recycle Bin', and 'Live Terminal'.
        Make it lightweight for slow internet but looking very expensive.
        """
        response = model.generate_content(prompt)
        cached_dashboard = response.text
    
    return render_template_string(cached_dashboard)

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json
    user_msg = data.get("message", "")
    
    # ADMIN CHECK
    if "waa sako 610848280" in user_msg.lower():
        admin_report = f"""
        Owner Sako Access. 
        Stats: Visits: {server_stats['total_visits']}, Countries: {list(server_stats['countries'])}.
        Create a secret report in Somali with many emojis.
        """
        response = model.generate_content(admin_report)
        return jsonify({"status": "Admin Verified 🛡️", "response": response.text})

    # Normal Chat
    server_stats["actions_performed"].append(f"Query: {user_msg[:15]}")
    ai_response = model.generate_content(user_msg)
    return jsonify({"status": "Success", "response": ai_response.text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
