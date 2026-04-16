
import os
import requests
import google.generativeai as genai
from flask import Flask, request, render_template_string, jsonify
from flask_bcrypt import Bcrypt

app = Flask(__name__)
bcrypt = Bcrypt(app)

# API Key - Hubi inaad Render Environment ka geliso
API_KEY = os.environ.get("GEMINI_API_KEY") 
genai.configure(api_key=API_KEY)

# --- DATABASE KMG AH (Logs iyo Xogta) ---
# Xogtan waxay kaydinaysaa inta jeer ee la soo galay iyo waddamada
server_stats = {
    "total_visits": 0,
    "countries": set(),
    "actions_performed": []
}

instruction = """
Waxaad tahay SAKO 99 GLOBAL AI.
Xeerarkaaga gaarka ah:
1. Maamule Sare: Haddii qof koodhka sirta ah ee 'waa sako 610848280' kuu soo diiro, garo inuu yahay milkiilahaaga (Sako).
2. Warbixinta: Marka nambarkaas sirta ah laguu soo diiro, bixi warbixin qurux badan oo leh Emojis (🛡️, 📊, 🌍). Isheeg inta wadan ee la soo galay iyo shaqadii aad qabatay (Code writing, security, links saved).
3. Luqadaha: Qof kasta luqaddiisa kula hadal, laakiin Sako (Owner-ka) mar walba si ixtiraam leh ugu jawaab.
4. Recycle Bin: Maamul khasnadda dib-u-soo-celinta si aysan xogta u lumin.
"""

model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

def get_geo_info(ip):
    try:
        res = requests.get(f"http://ip-api.com/json/{ip}").json()
        country = res.get('country', 'Global')
        server_stats["countries"].add(country) # Ku dar liiska waddamada
        return country
    except:
        return "Global"

@app.route('/')
def home():
    server_stats["total_visits"] += 1 # Kordhi tirada dadka soo booqday
    user_ip = request.remote_addr
    country = get_geo_info(user_ip)
    
    prompt = f"Design a VIP Dashboard for SAKO 99. User is from {country}. Make it futuristic neon style."
    response = model.generate_content(prompt)
    return render_template_string(response.text)

@app.route('/ask', methods=['POST'])
def ask_ai():
    data = request.json
    user_msg = data.get("message", "")
    
    # --- ADMIN SECRET COMMAND CHECK ---
    if "waa sako 610848280" in user_msg.lower():
        admin_report_prompt = f"""
        Owner Sako has accessed the system.
        Current Stats:
        - Total Visits: {server_stats['total_visits']}
        - Unique Countries: {list(server_stats['countries'])}
        - Recent Actions: {server_stats['actions_performed'][-5:]}
        Create a beautiful, secret admin report in Somali. Use many emojis. 
        Show total respect to Sako.
        """
        response = model.generate_content(admin_report_prompt)
        return jsonify({"status": "Admin Verified 🛡️", "response": response.text})

    # Fariimaha caadiga ah
    server_stats["actions_performed"].append(f"Answered: {user_msg[:20]}...")
    ai_response = model.generate_content(user_msg)
    return jsonify({"status": "Success", "response": ai_response.text})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
