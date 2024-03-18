import dotenv, os, subprocess, psutil, sys
from Misc import log

# Values from .env
env = dotenv.dotenv_values(".env")
log("Collecting env variables...", "KSP")
TOKEN = env['DC_TOKEN']
TELNET_IP = env['KSP_IP']
TELNET_PORT = env['KSP_PORT']
GUILD_ID = env['DC_GUILD']
log("Env variables recieved successfully.", "KSP")

tn = None
ksp = None

def killgame(process_name="KSP_x64.exe"):
    global tn, ksp
    try:
        subprocess.run(["taskkill", "/f", "/im", process_name], check=True)
        tn = None
        ksp = None
        log(f"Process {process_name} killed successfully.","KSP",1)
        os.chdir("D:\\Python\\KSPController")
    except subprocess.CalledProcessError as e:
        log(f"Failed to kill process {process_name}. Error: {e}","KSP",3)
    except:
        log(f"Cant kill {process_name}, sorry :(", "KSP", 3)

def check_ksp_status():
    KSP = None
    for proc in psutil.process_iter():
        if proc.name == "KSP_x64.exe":
            KSP = True
    return KSP

def startgame():
    global ksp
    ksp = check_ksp_status()
    log(msg='/startksp',type=2)
    if ksp:
        log("KSP is already on", "KSP", 2)
        return False
    else:
        ksppath = dotenv.dotenv_values(".env")
        os.chdir("E:\\Steam\\steamapps\\common\\Kerbal Space Program")
        subprocess.Popen(["KSP_x64.exe", "-popupwindow", "-single-instance"], shell=True)
        ksp = True
        return True