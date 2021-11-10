import subprocess
import itertools
import re
import os
import time
import json
import psutil
from termcolor import colored
try:
    import requests
    import urllib3
except ModuleNotFoundError:
    input()
    exit()

start_time = time.time()
os.system("cls" if os.name == "nt" else "clear")

def launchercheck():
    try:
        command = "WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline"

        output = subprocess.Popen(command, stdout=subprocess.PIPE,
                                        shell=True).stdout.read().decode('utf-8')

        port = re.findall(r'"--app-port=(.*?)"', output)[0]
        password = re.findall(r'"--remoting-auth-token=(.*?)"', output)[0]

        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

        session = requests.session()
        session.verify = False
        return port, password, session
    except:
        return 0, "", 0

def countdown(t):
    while t:
        time.sleep(1)
        t -= 1
        os.system("cls" if os.name == "nt" else "clear")
        if t <= 1:
            print(colored("League found.", "green"), "Please wait", colored(t, "yellow"), "second.")
        else:
            print(colored("League found.", "green"), "Please wait", colored(t, "yellow"), "seconds.")
    os.system("cls" if os.name == "nt" else "clear")
    print(colored("Auto Accept is currently active.", "green"))
    print("Press", colored('"Ctrl + C"', "red"), "to stop the script.\n")


def time_converter(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Program was running for {0}h:{1}m:{2}s".format(int(hours),int(mins),int(sec)))


leaguecheck = "LeagueClient.exe" in (p.name() for p in psutil.process_iter())

def firstleaguecheck():
    for c in itertools.cycle([".", "..", "..."]):
        leaguecheck = "LeagueClient.exe" in (p.name() for p in psutil.process_iter())
        os.system("cls" if os.name == "nt" else "clear")
        output = "Waiting for League" + c
        print(colored(output, "yellow"))
        if leaguecheck == True:
            countdown(15)
            break

def leaguecheckfunc():
    leaguecheck = "LeagueClient.exe" in (p.name() for p in psutil.process_iter())
    if leaguecheck == False:
        firstleaguecheck()

os.system("cls" if os.name == "nt" else "clear")
print(colored("Auto Accept is currently disabled.\n", "red"))
print("Type", colored('"start"', "green"), "to start the Auto Accept.")
print("Press", colored('"Ctrl + C"', "red"), "to stop the script.\n")


def DoAccept(ready):
    try:
        if ready == "start":
            os.system("cls" if os.name == "nt" else "clear")
            print(colored("Auto Accept is currently active.", "green"))
            print("Press", colored('"Ctrl + C"', "red"), "to stop the script.\n")

            while True:
                leaguecheckfunc()
                port, password, session = launchercheck()
                if port != 0:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S:", t)

                    checkResponse = session.get("https://127.0.0.1:%s/lol-matchmaking/v1/ready-check" %
                            port, data={}, auth=requests.auth.HTTPBasicAuth("riot", password))
                    if checkResponse.ok:
                        jsonResponse = json.loads(checkResponse.text)
                        if jsonResponse["state"] == "InProgress" and jsonResponse["playerResponse"] != "Accepted":
                            acceptResponse = session.post("https://127.0.0.1:%s/lol-matchmaking/v1/ready-check/accept" %
                                    port, data={}, auth=requests.auth.HTTPBasicAuth("riot", password))
                            if acceptResponse.ok:
                                print(current_time, colored("Match accepted", "green"))
                                
                    time.sleep(0.5)
        else:
            os.system("cls" if os.name == "nt" else "clear")
            print(colored("Unknown command:", "red"), ready, "\n")
            print("Type", colored('"start"', "green"), "to start the Auto Accept.")
            print("Press", colored('"Ctrl + C"', "red"), "to stop the script.\n")
            NewInput = input()
            DoAccept(NewInput)

    except KeyboardInterrupt:
        os.system("cls" if os.name == "nt" else "clear")
        print(colored("Auto Accept has been closed.\n", "red"))
        end_time = time.time()
        time_lapsed = end_time - start_time
        time_converter(time_lapsed)
        pass

DoAccept(input())