import dotenv, requests, psutil, KSP, platform
from datetime import datetime
from colorama import init, Fore

init()

def now():
    return datetime.now().strftime("%H:%M:%S")
def today():
    return datetime.now().strftime("%Y-%m-%d")

def log(msg:str, exec:str="DEBUG", type:int=0):
    now_str = f"{today()} {now()}"
    logparts = [f'{Fore.LIGHTBLACK_EX}{now_str}{Fore.RESET}']
    if type == 0:
        logparts.append(f' {Fore.LIGHTWHITE_EX}DEBUG{Fore.RESET}    ')
    elif type == 1: 
        logparts.append(f' {Fore.LIGHTBLUE_EX}INFO{Fore.RESET}     ')
    elif type == 2: 
        logparts.append(f' {Fore.YELLOW}WARNING{Fore.RESET}  ')
    elif type == 3:
        logparts.append(f' {Fore.RED}ERROR{Fore.RESET}    ')
    logparts.append(f'{Fore.MAGENTA}{exec}{Fore.RESET}')
    logparts.append(f' {msg}')
    print("".join(logparts))

def OLDlog(exec:str, msg:str, type:int=1):
    log(msg,exec,type)

def get_dotenv():
    envvar = dotenv.dotenv_values()
    return envvar

def read_from_pastebin(url_code:str):
    if url_code.startswith("https://pastebin.com/"):
        code = pastebinfromurl(url_code)
    else:
        code = pastebinfromurl(f"https://pastebin.com/{url_code}")

    return code


def pastebinfromurl(url:str):
    response = requests.get(url)
    if response.status_code == 200:
        code = response.text
        return code
    else:
        return None
    

def status():
    cpu_usage = psutil.cpu_percent()
    ram_usage = round(psutil.virtual_memory().used / 1024**2)
    ram_total = round(psutil.virtual_memory().total / 1024**2)
    platform_info = platform.platform()
    global ksp
    global tn
    ksp = KSP.check_ksp_status()
    if not ksp:
        tn = None
    if tn:
        tn_status = f"Connected to {KSP.TELNET_IP}:{KSP.TELNET_PORT}"
    else:
        tn_status = f"Not connected"
    if ksp:
        ksp_status = f"Up and running"
    else:
        ksp_status = f"Not running"

    status = [cpu_usage,ram_usage,ram_total,platform_info,ksp_status,tn_status]
    return status
    # message = f"CPU:  {cpu_usage}%\nRAM:  {ram_usage}MB / {ram_total}MB\nPlatform: {platform_info}\n\nKSP status: {ksp_status}\nTelnet status: {tn_status}"
