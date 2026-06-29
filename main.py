import pyautogui as pyg
import time, os, json, webbrowser
from util import *
from pathlib import Path

config = json.load(open("config.json", "r"))

def GetFilename(url:str):
    return url.rsplit("#", 1)[1]

def Download(url:str):
    if not webbrowser.open(url):
        return False
    
    time.sleep(config["open_link_sleep"])

    pyg.click(config["dl_btn_pos"][0], config["dl_btn_pos"][1])
    if config["close_ad_page"]:
        time.sleep(.4)
        pyg.hotkey("ctrl", "w") #this closes ad page
    pyg.click(config["dl_btn_pos"][0], config["dl_btn_pos"][1])
    time.sleep(config["redirect_sleep"])
    pyg.hotkey("ctrl", "w")

    return True

def SubstringInList(target_string:str, string_list, remove_ext = True):
    if remove_ext: target_string = target_string.rsplit(".", 1)[0]
    return any(target_string in s for s in string_list)

if __name__ == "__main__":
    LogInfo("Please ensure you've set download button position with assign.py")

    links_path = input("Enter links txt file: ")
    if not os.path.exists(links_path):
        LogError(f"{links_path} does not exists!")
        quit(1)

    links = []
    with open(links_path, "r") as f:
        for l in f.read().split("\n"):
            if len(l) <= 1:
                continue

            links.append(l)
            LogInfo(f"{l[:40]}... Added")

    LogInfo(f"Found {len(links)} link(s)!")

    failed = []
    current_sessions = 0

    for l in links:
        LogInfo(f"Downloading {l}")
        if Download(l):
            LogInfo("Success!")
        else:
            LogError("Failed!")
            failed.append(l)
            continue

        current_sessions += 1
        if config["max_sessions"] != -1 and current_sessions >= config["max_sessions"]:
            timeout = config["sessions_timeout"]
            LogInfo(f"Waiting {timeout}s to complete {current_sessions} session(s)")
            time.sleep(timeout)
            current_sessions = 0
        
        else: time.sleep(.1)

    LogInfo("Verifying downloaded files...")
    downloaded_files = os.listdir(Path(config["download_path"]))
    print(downloaded_files)
    for l in links:
        fname = GetFilename(l)

        if not SubstringInList(fname, downloaded_files):
            LogError(f"Not found (or still downloading): {fname} ({l})")
            failed.append(l)

    if len(failed) != 0:
        with open("failed.txt","w") as log:
            for l in failed:
                log.write(l+"\n")
        
        LogInfo("Failed link(s) written to failed.txt")