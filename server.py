import os
import json
from flask import Flask, request, jsonify, render_template
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

PORT = int(os.getenv("PORT", 5000))
DATABASE_URL = os.getenv("DATABASE_URL")
MONGO_URI = os.getenv("MONGO_URI")
EMERGENCY_ACCESS_KEY = os.getenv("EMERGENCY_ACCESS_KEY", "SECURE-KEY-2026")

def load_database():
    if os.path.exists("database.json"):
        with open("database.json", "r") as f:
            return json.load(f)
    return {"records": []}

def security_validation_agent(req_headers, req_body):
    auth_token = req_headers.get("Authorization")
    official_code = req_body.get("official_clearance_code")

    if not official_code or official_code != EMERGENCY_ACCESS_KEY:
        return False, "Security Agent: Unauthorized access. Invalid clearance code."
    
    return True, "Security Agent: Clearance verified successfully."

def data_synthesis_agent(user_id, purpose):
    db = load_database()
    user_records = [r for r in db.get("records", []) if r.get("user_id") == user_id]

    if not user_records:
        return None, "Synthesis Agent: No matching sensitive records found."

    report = {
        "agent_status": "SUCCESS",
        "purpose_stated": purpose,
        "target_user": user_id,
        "payload": user_records,
        "classification": "CONFIDENTIAL - OFFICIAL USE ONLY"
    }
    return report, "Synthesis Agent: Data successfully retrieved and structured."

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/api/dual-agent-fetch', methods=['POST'])
def dual_agent_orchestrator():
    data = request.json or {}
    user_id = data.get("user_id")
    purpose = data.get("purpose", "Formal Emergency Request")

    is_secure, security_msg = security_validation_agent(request.headers, data)
    if not is_secure:
        return jsonify({"error": security_msg}), 403

    synthesized_data, synthesis_msg = data_synthesis_agent(user_id, purpose)
    if not synthesized_data:
        return jsonify({"error": synthesis_msg}), 404

    return jsonify({
        "audit_trail": {
            "security_check": security_msg,
            "synthesis_status": synthesis_msg,
            "timestamp": os.popen("date -u").read().strip()
        },
        "result": synthesized_data
    }), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True)
