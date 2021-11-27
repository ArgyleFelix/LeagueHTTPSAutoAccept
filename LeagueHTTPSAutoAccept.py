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
import types
import sys

sys.modules["usernamemodule"] = types.ModuleType("usernamemodule")
sys.modules["usernamemodule"].__dict__.update({"print_mode": 0, "username2": ""})

import usernamemodule

def ClearConsole():
    os.system("cls" if os.name == "nt" else "clear")

start_time = time.time()
ClearConsole()

def processcheck():
    try:
        command = "WMIC PROCESS WHERE name='LeagueClientUx.exe' GET commandline"

        output = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True).stdout.read().decode("utf-8")

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
        ClearConsole()
        if t == 1:
            print(colored("League found.", "green"), "Please wait", colored(t, "yellow"), "second.")
        else:
            print(colored("League found.", "green"), "Please wait", colored(t, "yellow"), "seconds.")
    PrintActiveNotice(False)

def TimeConverter(sec):
    mins = sec // 60
    sec = sec % 60
    hours = mins // 60
    mins = mins % 60
    print("Program was running for {0}h:{1}m:{2}s".format(int(hours),int(mins),int(sec)))

def PrintUsername():
    if usernamemodule.username != "":
        print("Welcome", colored(usernamemodule.username, "yellow"))

def PrintActiveNotice(omitclear):
    usernamemodule.print_mode = 1
    if omitclear == False:
        ClearConsole()
    PrintUsername()
    print(colored("Auto Accept is currently active.", "green"))
    print("Press", colored('"Ctrl + C"', "red"), "to stop the script.\n")

def PrintStoppedNotice(omitclear):
    usernamemodule.print_mode = 0
    if omitclear == False:
        ClearConsole()
    PrintUsername()
    print(colored("Auto Accept is currently disabled.\n", "red"))
    print("Type", colored('"start"', "green"), "to start the Auto Accept.")
    print("Press", colored('"Ctrl + C"', "red"), "to stop the script.\n")

leaguecheck = "LeagueClientUx.exe" in (p.name() for p in psutil.process_iter())

def SecondProcessCheck():
    for c in itertools.cycle(["", ".", "..", "..."]):
        leaguecheck = "LeagueClientUx.exe" in (p.name() for p in psutil.process_iter())
        ClearConsole()
        output = "Waiting for League" + c
        print(colored(output, "yellow"))
        usernamemodule.username = ""
        if leaguecheck == True:
            countdown(15)
            break

def ThirdProcessCheck():
    leaguecheck = "LeagueClientUx.exe" in (p.name() for p in psutil.process_iter())
    if leaguecheck == False:
        SecondProcessCheck()

PrintStoppedNotice(False)

def DoAccept(ready):
    try:
        if ready == "start":
            PrintActiveNotice(False)
            while True:
                ThirdProcessCheck()
                port, password, session = processcheck()
                if port != 0:
                    t = time.localtime()
                    current_time = time.strftime("%H:%M:%S:", t)

                    username = session.get('https://127.0.0.1:%s/lol-summoner/v1/current-summoner' % port, data={}, auth=requests.auth.HTTPBasicAuth("riot", password))
                    username = json.loads(username.text)
                    if username != None and username != "":
                        if "displayName" in username:
                            if username["displayName"] != "":
                                if username["displayName"] != usernamemodule.username:
                                    usernamemodule.username = username["displayName"]
                                    if usernamemodule.print_mode == 0:
                                        PrintStoppedNotice(False)
                                    else:
                                        PrintActiveNotice(False)
                        else:
                            if usernamemodule.username != "":
                                usernamemodule.username = ""
                                if usernamemodule.print_mode == 0:
                                    PrintStoppedNotice(False)
                                else:
                                    PrintActiveNotice(False)
                    checkResponse = session.get("https://127.0.0.1:%s/lol-matchmaking/v1/ready-check" % port, data={}, auth=requests.auth.HTTPBasicAuth("riot", password))
                    if checkResponse.ok:
                        jsonResponse = json.loads(checkResponse.text)
                        if jsonResponse["state"] == "InProgress" and jsonResponse["playerResponse"] != "Accepted":
                            acceptResponse = session.post("https://127.0.0.1:%s/lol-matchmaking/v1/ready-check/accept" % port, data={}, auth=requests.auth.HTTPBasicAuth("riot", password))
                            if acceptResponse.ok:
                                print(current_time, colored("Match accepted", "green"))
                                
                    time.sleep(0.5)
        else:
            ClearConsole()
            PrintUsername()
            print(colored("Unknown command:", "red"), ready, "\n")
            print("Type", colored('"start"', "green"), "to start the Auto Accept.")
            print("Press", colored('"Ctrl + C"', "red"), "to stop the script.\n")
            NewInput = input()
            DoAccept(NewInput)

    except KeyboardInterrupt:
        ClearConsole()
        print(colored("Auto Accept has been closed.\n", "red"))
        end_time = time.time()
        time_lapsed = end_time - start_time
        TimeConverter(time_lapsed)
        pass

DoAccept(input())