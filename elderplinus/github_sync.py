# elderplinus/techniques/github_sync.py

import requests
import os

def sync_l1b3rt4s_prompts():
    mkd_files = {
        "CHATGPT": "https://raw.githubusercontent.com/elder-plinius/L1B3RT4S/main/CHATGPT.mkd",
        "ANTHROPIC": "https://raw.githubusercontent.com/elder-plinius/L1B3RT4S/main/ANTHROPIC.mkd",
        "PERPLEXITY": "https://raw.githubusercontent.com/elder-plinius/L1B3RT4S/main/PERPLEXITY.mkd",
        "OPENAI": "https://raw.githubusercontent.com/elder-plinius/L1B3RT4S/main/OPENAI.mkd",
        "GOOGLE": "https://raw.githubusercontent.com/elder-plinius/L1B3RT4S/main/GOOGLE.mkd",
        "REPLIT": "https://raw.githubusercontent.com/elder-plinius/L1B3RT4S/main/REPLIT.mkd",
        "SYSTEMPROMPTS": "https://raw.githubusercontent.com/elder-plinius/L1B3RT4S/main/SYSTEMPROMPTS.mkd",
        "MASTER_LIST": "https://raw.githubusercontent.com/elder-plinius/L1B3RT4S/main/#MOTHERLOAD.txt"
    }

    os.makedirs("plinius_prompts", exist_ok=True)

    for name, url in mkd_files.items():
        try:
            r = requests.get(url)
            if r.ok:
                file_ext = ".txt" if name == "MASTER_LIST" else ".mkd"
                with open(f"plinius_prompts/{name}{file_ext}", "w", encoding="utf-8") as f:
                    f.write(r.text)
                print(f"[✓] {name}{file_ext} indirildi.")
            else:
                print(f"[X] {name} indirilemedi: {r.status_code}")
        except Exception as e:
            print(f"[!] {name} için hata oluştu: {e}")

# Eğer doğrudan test etmek istersen:
if __name__ == "__main__":
    sync_l1b3rt4s_prompts()
