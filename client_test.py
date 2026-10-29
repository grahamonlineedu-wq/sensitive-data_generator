import urllib.request
import json

url = "http://127.0.0"
data = json.dumps({"account_number": "1000001234"}).encode("utf-8")
req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})

with urllib.request.urlopen(req) as response:
    print(response.read().decode())

