import json
import hashlib

def load_database():
    with open('database.json', 'r') as file:
        return json.load(file)

def verify_account(input_account):
    cleaned_input = input_account.strip()

    hasher = hashlib.sha256()
    hasher.update(cleaned_input.encode('utf-8'))
    input_hash = hasher.hexdigest()

    # DEBUG LINE: This shows you exactly what hash your input created
    print(f"[DEBUG] Generated Hash: {input_hash}")

    input_suffix = cleaned_input[-4:]
    db = load_database()

    for user in db['users']:
        if user['account_hash'] == input_hash and user['account_suffix'] == input_suffix:
            return f"[SUCCESS] Match Found. Account Suffix: {user['account_suffix']} belongs to: {user['masked_name']}"

    return "[ERROR] Access Denied. No matching records or invalid credentials."

print("--- Secure Identity Verification System ---")
user_input = input("Enter your full account number to verify identity: ")

result = verify_account(user_input)
print(result)

