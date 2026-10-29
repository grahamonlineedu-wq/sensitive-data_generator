import os

def analyze_security_logs(log_file_path='security.log'):
    if not os.path.exists(log_file_path):
        print("[SYSTEM ERROR] No security.log file found yet. Generate some traffic first!")
        return

    success_count = 0
    failed_count = 0
    alert_count = 0
    total_lines = 0

    print("\n" + "="*50)
    print("        CIG SYSTEM SECURITY STATUS AUDIT        ")
    print("="*50)

    with open(log_file_path, 'r') as file:
        for line in file:
            total_lines += 1
            if "SUCCESS" in line:
                success_count += 1
            elif "FAILED" in line:
                failed_count += 1
            elif "Rate limit exceeded" in line or "Security Alert" in line:
                alert_count += 1

    print(f"📄 Total System Log Entries Processed: {total_lines}")
    print(f"🟢 Successful Verifications:         {success_count}")
    print(f"🔴 Failed Lookup Attempts:           {failed_count}")
    print(f"⚠️ Security Rate-Limit Blocks:       {alert_count}")
    print("="*50)

    # Basic risk assessment heuristic
    if alert_count > 5:
        print("🚨 [STATUS ALERT] High frequency of rate-limit triggers detected. Possible automated scan.")
    elif failed_count > success_count * 2 and failed_count > 0:
        print("🟡 [STATUS WARNING] Elevated failure rate. Monitor endpoint usage pattern closely.")
    else:
        print("🍏 [STATUS NOMINAL] System operational parameters within secure boundaries.")
    print("="*50 + "\n")

if __name__ == '__main__':
    analyze_security_logs()

