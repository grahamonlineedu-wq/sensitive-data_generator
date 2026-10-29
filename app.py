import secrets

def generate_masked_token():
    # Generates a secure, random 16-byte token for a user
    secure_token = secrets.token_hex(16)
    # Mask it to protect user identity in logs
    masked = secure_token[:4] + "********" + secure_token[-4:]
    return masked

print(f"Secure Masked Token Generated: {generate_masked_token()}")

