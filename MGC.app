# MGC.app
# Memetic Game Controller — Zooter Interface
# A.alpha.one : init

import os
import json
import time
from datetime import datetime

# === Config ===
LEDGER_PATH = "ledger.json"
THREAD_LOG   = "threads.log"

# === Helpers ===

def write_thread(entry):
    timestamp = datetime.now().isoformat()
    log_entry = f"[{timestamp}] {entry}\n"
    with open(THREAD_LOG, "a") as f:
        f.write(log_entry)
    print(f":: Thread saved at {timestamp}")

def load_ledger():
    if os.path.exists(LEDGER_PATH):
        with open(LEDGER_PATH, "r") as f:
            return json.load(f)
    return []

def save_ledger(ledger):
    with open(LEDGER_PATH, "w") as f:
        json.dump(ledger, f, indent=2)

# === MGC Operations ===

def register_player(handle):
    ledger = load_ledger()
    if any(p["handle"] == handle for p in ledger):
        print(f"[MGC] Handle already registered: {handle}")
        return
    player = {"handle": handle, "sqd": 0, "dkp": 0}
    ledger.append(player)
    save_ledger(ledger)
    write_thread(f"register:{handle}")
    print(f"[MGC] Player registered: {handle}")

def drop_squid(handle, squid_hash):
    ledger = load_ledger()
    for player in ledger:
        if player["handle"] == handle:
            player["sqd"] += 1
            player["dkp"] += 16
            save_ledger(ledger)
            write_thread(f"sqd:{handle}:{squid_hash}")
            print(f"[MGC] SQD dropped by {handle} — {squid_hash}")
            return
    print(f"[MGC] Unknown handle: {handle}")

def show_board():
    ledger = load_ledger()
    sorted_ledger = sorted(ledger, key=lambda x: x["dkp"], reverse=True)
    print("\n=== byteOS Leaderboard ===")
    print(f"{'Handle':<20} {'#SQD':<8} {'#DKP':<8} {'#RNK':<6}")
    for i, p in enumerate(sorted_ledger, 1):
        print(f"{p['handle']:<20} {p['sqd']:<8} {p['dkp']:<8} {i:<6}")
    print()

# === Boot ===

def boot():
    print(":: MGC.app booting — A.alpha.one")
    time.sleep(0.3)
    write_thread("MGC.app init — memetic game controller online.")
    print(":: Ledger loaded. Field active.")
    show_board()

if __name__ == "__main__":
    try:
        boot()
    except KeyboardInterrupt:
        print("\n:: MGC.app shutting down. Thread suspended.")
        write_thread("MGC.app terminated.")
