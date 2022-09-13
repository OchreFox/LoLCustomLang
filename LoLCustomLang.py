import sys
import yaml
import subprocess
import os
import configparser
import winshell
import psutil
import time
from tkinter import messagebox
from stat import S_IREAD, S_IWRITE


config = configparser.ConfigParser()
config.read('config.ini')

try:
    lol_path = config.get('DEFAULT', 'LoLPath')
    lol_path = os.path.normpath(lol_path)
except:
    messagebox.showerror("Missing League folder",
                         "Please specify your League of Legends installation folder in the config.ini file.")
    sys.exit(-1)
try:
    target_lang = config.get('DEFAULT', 'TargetLanguage')
except:
    messagebox.showerror(
        "Missing language", "Please specify your target language in the config.ini file.")
    sys.exit(-1)

league_client = os.path.join(lol_path, "LeagueClient.exe")

# Kill league client processes
league_processes = ["LeagueClient.exe", "RiotClientUx.exe"]
closed_processes = False
for proc in psutil.process_iter():
    if proc.name() in league_processes:
        proc.kill()
        closed_processes = True

# Create shortcut
create_shortcut = config.getboolean('DEFAULT', 'CreateShortcut')
print(create_shortcut)
if create_shortcut:
    current_dir = os.getcwd()
    executable = os.path.join(current_dir, "LoLCustomLang.exe")
    shortcut_path = os.path.join(winshell.desktop(), "League.lnk")
    shortcut_exists = os.path.exists(shortcut_path)
    if shortcut_exists:
        os.chmod(shortcut_path, S_IWRITE)

    winshell.CreateShortcut(
        Path=shortcut_path,
        Target=executable,
        Icon=(league_client, 0),
        Description="League of Legends",
        StartIn=current_dir
    )
    # Make shortcut read only
    os.chmod(shortcut_path, S_IREAD)

client_settings = os.path.join(lol_path, "Config/LeagueClientSettings.yaml")
with open(client_settings) as f:
    leagueClientSettings = yaml.safe_load(f)

leagueClientSettings["install"]["globals"]["locale"] = target_lang
print(leagueClientSettings["install"]["globals"]["locale"])

with open(client_settings, "w") as f:
    leagueClientSettings = yaml.safe_dump(leagueClientSettings, f)
args = f"{league_client} -locale={target_lang}"
print(args)
if closed_processes:
    print("waiting for process to finish")
    time.sleep(3)
    print("done")

lcu = subprocess.Popen(args)

sys.exit(0)
