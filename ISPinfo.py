# gets info about the ISP the command is running from
import requests
r = requests.get(f"http://ip-api.com/json/{requests.get('https://api.ipify.org?format=json').json()['ip']}").json()
print(r)
