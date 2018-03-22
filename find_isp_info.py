#Gets ISP info
import requests
requests.get("http://ip-api.com/json/" + requests.get("https://api.ipify.org?format=json").json()["ip"]).json()
