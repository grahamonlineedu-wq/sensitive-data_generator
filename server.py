from flask import Flask, request, jsonify, render_template, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import hashlib
import logging
import os

app = Flask(__name__)

logging.basicConfig(
    filename='security.log',
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["100 per day"],
    storage_uri="memory://"
)

def load_database():
    with open('database.json', 'r') as file:
        return json.load(file)

@app.errorhandler(429)
def ratelimit_handler(e):
    logging.warning(f"Security Alert: Rate limit exceeded by client IP: {request.remote_addr}")
    return jsonify({
        "status": "error",
        "message": "Too many requests. Cyber-security rate limit triggered. Please slow down."
    }), 429


@app.route('/', methods=['GET'])
def home():
    logging.info(f"CIG Reference Portal accessed by remote IP: {request.remote_addr}")
    # CACHE BUSTING FIX: Tells browser to fetch structural updates immediately instead of loading from old memory cache
    response = make_response(render_template('index.html'))
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response, 200


@app.route('/api/verify', methods=['POST'])
@limiter.limit("5 per minute")
def verify_identity():
    data = request.get_json()

    if not data or 'account_number' not in data or 'scope' not in data:
        logging.warning(f"Malformed payload block triggered from IP: {request.remote_addr}")
        return jsonify({"status": "error", "message": "Bad Request. Missing target metrics."}), 400

    input_account = data['account_number'].strip()
    target_scope = data['scope'].strip()

    hasher = hashlib.sha256()
    hasher.update(input_account.encode('utf-8'))
    input_hash = hasher.hexdigest()
    input_suffix = input_account[-4:]

    db = load_database()

    for user in db['users']:
        if (user['account_hash'] == input_hash and
            user['account_suffix'] == input_suffix and
            user['scope'] == target_scope):

            logging.info(f"Identity Verification: SUCCESS for scope [{target_scope}] Suffix: {input_suffix} from IP: {request.remote_addr}")
            return jsonify({
                "status": "success",
                "match": True,
                "masked_name": user['masked_name'],
                "suffix": user['account_suffix']
            }), 200

    logging.warning(f"Identity Verification: FAILED lookup for scope [{target_scope}] Suffix: {input_suffix} from IP: {request.remote_addr}")
    return jsonify({"status": "denied", "message": "Signature verification failed for the selected scope."}), 401


@app.route('/api/metrics', methods=['GET'])
def get_system_metrics():
    log_file = 'security.log'
    if not os.path.exists(log_file):
        return jsonify({"total_entries": 0, "successful": 0, "failed": 0, "status": "NOMINAL"})

    success_count = 0
    failed_count = 0
    total_lines = 0

    with open(log_file, 'r') as file:
        for line in file:
            total_lines += 1
            if "SUCCESS" in line:
                success_count += 1
            elif "FAILED" in line:
                failed_count += 1

    status = "NOMINAL"
    if failed_count > success_count * 2 and failed_count > 0:
        status = "ALERT_ELEVATED_FAILURES"

    return jsonify({
        "total_entries": total_lines,
        "successful": success_count,
        "failed": failed_count,
        "status": status
    }), 200

if __name__ == '__main__':
    print("--- Starting Enhanced CIG Web API and Dashboard Server ---")
    app.run(host='127.0.0.1', port=5000, debug=True)

