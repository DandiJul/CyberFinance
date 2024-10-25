import requests
import time
import json
import logging
from colorama import Fore, Style, init
import asyncio

# Initialize colorama
init()

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')

def read_api_keys():
    with open("token.txt", 'r') as f:
        api_keys = [line.strip() for line in f]

    if not api_keys:  # If list is empty, add a default element
        api_keys.append("default_key")

    with open("data.txt", 'r') as f:
        hashes = [line.strip() for line in f]

    while len(api_keys) < len(hashes):
        api_keys.append(api_keys[-1])

    return api_keys

def read_hashes():
    with open("data.txt", 'r') as f:
        return [line.strip() for line in f]

api_keys = read_api_keys()
hashes = read_hashes()

def get_time_stamp():
    return time.strftime("[%Y-%m-%d %H:%M:%S]")

def format_unix_timestamp(timestamp):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))

def update_tokens(api_key, hash_val, account_index, total_accounts):
    response = requests.post("https://api.cyberfin.xyz/api/v1/game/initdata",
                             headers={
                                 'Content-Type': "application/json",
                                 'Secret-Key': 'cyberfinance'
                             },
                             data=json.dumps({'initData': hash_val}))
    if response.ok:
        data = response.json()
        token = data['message']['accessToken']
        logging.info(f"{Fore.GREEN} Token diperbarui untuk Akun {account_index}/{total_accounts}{Style.RESET_ALL}")
        return token
    else:
        if api_key:
            logging.info(f"{Fore.RED} Gagal memperbarui token untuk Akun {account_index}/{total_accounts}, menggunakan token sebelumnya.{Style.RESET_ALL}")
            return api_key
        else:
            logging.info(f"{Fore.RED} Gagal memperbarui token untuk Akun {account_index}/{total_accounts}, tidak ada token sebelumnya.{Style.RESET_ALL}")
            return None

def claim_mining_rewards(api_key, account_index, total_accounts):
    response = requests.get('https://api.cyberfin.xyz/api/v1/game/mining/gamedata',
                            headers={
                                'Authorization': f"Bearer {api_key}",
                                'Content-Type': 'application/json',
                                'Secret-Key': 'cyberfinance'
                            })
    if not response.ok:
        logging.info(f"{Fore.RED} Gagal mengambil data penambangan untuk Akun {account_index}/{total_accounts}{Style.RESET_ALL}")
        return
    data = response.json()
    mining_data = data['message']['miningData']
    current_time = int(time.time())
    crack_time = mining_data['crackTime']
    if current_time >= crack_time:
        claim_response = requests.get('https://api.cyberfin.xyz/api/v1/mining/claim',
                                      headers={
                                          'Authorization': f"Bearer {api_key}",
                                          'Content-Type': 'application/json',
                                          'Secret-Key': 'cyberfinance'
                                      })
        if not claim_response.ok:
            logging.info(f"{Fore.RED} Gagal klaim hadiah penambangan untuk Akun {account_index}/{total_accounts}{Style.RESET_ALL}")
            return
        claim_data = claim_response.json()
        logging.info(f"{Fore.GREEN} Berhasil klaim untuk Akun {account_index}/{total_accounts}, Total Balance: {claim_data['message']['userData']['balance']}, Waktu Klaim Berikutnya: {format_unix_timestamp(crack_time)}{Style.RESET_ALL}")
    else:
        logging.info(f"{Fore.YELLOW} Belum waktunya klaim untuk Akun {account_index}/{total_accounts}, Waktu Klaim Berikutnya: {format_unix_timestamp(crack_time)}{Style.RESET_ALL}")

def apply_auto_upgrade(api_key, account_index, total_accounts, auto_upgrade_egg, auto_upgrade_hammer):
    if auto_upgrade_egg:
        response = requests.post('https://api.cyberfin.xyz/api/v1/mining/boost/apply',
                                 headers={
                                     'Authorization': f"Bearer {api_key}",
                                     'Content-Type': 'application/json',
                                     'Secret-Key': 'cyberfinance'
                                 },
                                 data=json.dumps({'boostType': "EGG"}))
        if response.ok:
            logging.info(f"{Fore.GREEN} Berhasil apply EGG untuk Akun {account_index}/{total_accounts}{Style.RESET_ALL}")
        else:
            logging.info(f"{Fore.RED} Gagal apply EGG untuk Akun {account_index}/{total_accounts}{Style.RESET_ALL}")

    if auto_upgrade_hammer:
        response = requests.post('https://api.cyberfin.xyz/api/v1/mining/boost/apply',
                                 headers={
                                     'Authorization': f"Bearer {api_key}",
                                     'Content-Type': 'application/json',
                                     'Secret-Key': 'cyberfinance'
                                 },
                                 data=json.dumps({'boostType': "HAMMER"}))
        if response.ok:
            logging.info(f"{Fore.GREEN} Berhasil apply HAMMER untuk Akun {account_index}/{total_accounts}{Style.RESET_ALL}")
        else:
            logging.info(f"{Fore.RED} Gagal apply HAMMER untuk Akun {account_index}/{total_accounts}{Style.RESET_ALL}")

def auto_clear_tasks(api_key, account_index, total_accounts):
    tasks = [
        {"uuid": "bcf864fc-7b15-416c-b2d3-c70b5d894cad", "description": "Task 1"},
        {"uuid": "70282e59-f18e-4c86-9787-95a7bf0222ae", "description": "Task 2"},
        {"uuid": "daa79656-e41c-47ba-9fc5-68a6f9219bc2", "description": "Task 3"},
        {"uuid": "75bfab2c-d5a4-4ee5-8935-b933b2912d3f", "description": "Task 4"},
        {"uuid": "74ce3b22-d864-4eba-9c05-0ab94d27f344", "description": "Task 5"},
        {"uuid": "52cb5628-a60f-4a84-9646-868f587e6371", "description": "Task 6"},
        {"uuid": "93c04149-8f1f-4db2-b0a8-f6eaf685171b", "description": "Task 7"},
        {"uuid": "7885792d-dfb6-4775-897d-e9761643776a", "description": "Task 8"},
        {"uuid": "95029eb7-b05a-4de7-a900-e5db0965714d", "description": "Task 9"},
        {"uuid": "d1031f11-715c-45f0-9a1f-5fc4f44a3cea", "description": "Task 10"},
        {"uuid": "e1d5f45a-a0bc-4d7d-ad69-6e54c8ef4f28", "description": "Task 11"},
        {"uuid": "61f6ed32-8779-42d8-82fc-94b585b9b671", "description": "Task 12"},
        {"uuid": "b8b76cf8-dcf3-43d4-a4d0-175c3444e377", "description": "Task 13"},
        {"uuid": "d3bb4c3e-50e9-45aa-a90d-36b135588c54", "description": "Task 14"},
        {"uuid": "59ffbca3-83fc-4370-bfa9-85fd36bb255c", "description": "Task 15"},
        {"uuid": "65274e50-9000-4cc9-a9cc-ad48a9708b6f", "description": "Task 16"},
        {"uuid": "1e0a9faa-0810-4c35-af97-82e4d544ee51", "description": "Task 17"},
        {"uuid": "755364ac-a6a5-41ee-a0db-841ad18f7e75", "description": "Task 18"},
        {"uuid": "69b2b196-3161-4b59-92d8-b0c2ca9f0950", "description": "Task 19"},
        {"uuid": "642323ef-cbf9-4d7b-9d4d-72498bd1a2c1", "description": "Task 20"},
        {"uuid": "127f75b4-2419-48f4-a3fc-2f23838bc0e0", "description": "Task 21"},
        {"uuid": "e323144d-aa02-4740-9749-688e95f2da2c", "description": "Task 22"},
        {"uuid": "beafc2b6-7ad9-4830-83ed-5f1736e3af05", "description": "Task 23"},
        {"uuid": "9c9d894d-e318-4714-b144-721f209d0346", "description": "Task 24"},
        {"uuid": "ebb484a3-d570-4b92-8479-44920e05d4fc", "description": "Task 25"}
    ]

    for task in tasks:
        response = requests.patch(f'https://api.cyberfin.xyz/api/v1/gametask/complete/{task["uuid"]}',
                                  headers={
                                      'Authorization': f"Bearer {api_key}",
                                      'Content-Type': 'application/json',
                                      'Secret-Key': 'cyberfinance'
                                  })
        if response.ok:
            logging.info(f"{Fore.GREEN} Task {task['uuid']} ({task['description']}) cleared untuk Akun {account_index}/{total_accounts}{Style.RESET_ALL}")
        else:
            logging.debug(f"Response status code: {response.status_code}")
            logging.debug(f"Response text: {response.text}")
            logging.info(f"{Fore.RED} Gagal clear task {task['uuid']} ({task['description']}) untuk Akun {account_index}/{total_accounts}{Style.RESET_ALL}")

# Add debug level logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

async def perform_tasks_for_session(session_data, auto_upgrade_egg, auto_upgrade_hammer):
    api_key = session_data['api_key']
    hash_val = session_data['hash_val']
    account_index = session_data['account_index']
    total_accounts = session_data['total_accounts']

    # Update tokens
    api_key = update_tokens(api_key, hash_val, account_index, total_accounts)

    # Claim mining rewards
    if api_key:
        claim_mining_rewards(api_key, account_index, total_accounts)

    # Apply auto upgrade
    if api_key:
        apply_auto_upgrade(api_key, account_index, total_accounts, auto_upgrade_egg, auto_upgrade_hammer)

def start_mining_bot(delay_minutes, auto_upgrade_egg, auto_upgrade_hammer):
    logging.info(f"Total Akun: {len(hashes)}")

    sessions = [{'api_key': api_keys[i], 'hash_val': hashes[i], 'account_index': i + 1, 'total_accounts': len(api_keys)}
                for i in range(len(api_keys))]

    # Initial clear tasks
    for session_data in sessions:
        account_index = session_data['account_index']
        logging.info(f"Clearing tasks for akun: {account_index}")
        try:
            auto_clear_tasks(session_data['api_key'], account_index, len(api_keys))
        except Exception as e:
            logging.error(f"[Akun {account_index}] Terjadi kesalahan saat clearing tasks:", exc_info=e)

    while True:
        logging.info(f"Menunggu {delay_minutes * 60} detik sebelum menjalankan tugas berikutnya...")
        time.sleep(delay_minutes * 60)
        for session_data in sessions:
            account_index = session_data['account_index']
            logging.info(f"Memulai script untuk akun: {account_index}")
            try:
                asyncio.run(perform_tasks_for_session(session_data, auto_upgrade_egg, auto_upgrade_hammer))
            except Exception as e:
                logging.error(f"[Akun {account_index}] Terjadi kesalahan:", exc_info=e)

if __name__ == "__main__":
    print(r"""
       ____      _               _____ _                            
      / ___|   _| |__   ___ _ __|  ___(_)_ __   __ _ _ __   ___ ___ 
     | |  | | | | '_ \ / _ \ '__| |_  | | '_ \ / _` | '_ \ / __/ _ \
     | |__| |_| | |_) |  __/ |  |  _| | | | | | (_| | | | | (_|  __/
      \____\__, |_.__/ \___|_|  |_|   |_|_| |_|\__,_|_| |_|\___\___|
           |___/                                                    
    ┌──────────────────────────┐
    │ By ZUIRE AKA SurrealFlux │
    └──────────────────────────┘
    """)
    auto_upgrade_egg_input = input("Auto upgrade EGG (Y or N) (Default N): ").strip().upper()
    auto_upgrade_hammer_input = input("Auto upgrade HAMMER (Y or N) (Default N): ").strip().upper()
    auto_upgrade_egg = auto_upgrade_egg_input == 'Y'
    auto_upgrade_hammer = auto_upgrade_hammer_input == 'Y'
    delay = int(input("Silahkan Masukkan Waktu Delay (dalam menit): "))
    start_mining_bot(delay, auto_upgrade_egg, auto_upgrade_hammer)
