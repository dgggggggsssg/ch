from binascii import hexlify
import random
import string
import time
from uuid import uuid4
import requests
import threading

token = input("Bot token: ")
chat_id = input("Your ID: ")

total_checks = 0
total_hits = 0
total_fails = 0
lock = threading.Lock()

def generate_random_name(length=4):
    characters = string.ascii_letters + string.digits + "_" + '.'
    return ''.join(random.choice(characters) for _ in range(length))

def check_username(username):
    global total_checks, total_hits, total_fails
    did = int(bin(int(time.time()) + random.randint(1, 10000))[2:] + "00101101010100010100011000000110", 2)
    iid = int(bin(int(time.time()) + random.randint(1, 10000))[2:] + "00101101010100010100011000000110", 2)
    udid = hexlify(random.randbytes(8)).decode()
    cdid = str(uuid4())
    tim = str(int(time.time()))

    url = "https://api16-normal-c-alisg.tiktokv.com/aweme/v1/unique/id/check/"
    params = {
        "unique_id": username,
        "device_platform": "android",
        "os": "android",
        "ssmix": "a",
        "_rticket": tim,
        "cdid": cdid,
        "channel": "googleplay",
        "aid": "1233",
        "app_name": "musical_ly",
        "version_code": "360404",
        "version_name": "36.4.4",
        "manifest_version_code": "2023604040",
        "update_version_code": "2023604040",
        "ab_version": "36.4.4",
        "resolution": "900*1600",
        "dpi": "300",
        "device_type": "ASUS_I003DD",
        "device_brand": "Asus",
        "language": "en",
        "os_api": "28",
        "os_version": "9",
        "ac": "wifi",
        "is_pad": "0",
        "current_region": "DE",
        "app_type": "normal",
        "sys_region": "US",
        "last_install_time": tim,
        "mcc_mnc": "26201",
        "timezone_name": "Asia/Shanghai",
        "residence": "DE",
        "app_language": "en",
        "carrier_region": "DE",
        "timezone_offset": "28800",
        "host_abi": "arm64-v8a",
        "locale": "en",
        "ac2": "wifi",
        "uoo": "0",
        "op_region": "DE",
        "build_number": "36.4.4",
        "region": "US",
        "ts": tim,
        "iid": iid,
        "device_id": did,
        "openudid": udid
    }

    headers = {
        'x-tt-req-timeout': '90000',
        'accept-encoding': 'gzip',
        'sdk-version': '2',
        'x-tt-token': '03bb03260308276b082728241611ce2aee046004594f3f0c440074ca29446b0fa7a6622cb76ec24f4d06ea7cbbc63c27f8ec4d72f9103f95e2c36a4f7c531a2e853bebf0ef8483bf862228bc9424ae29b0eff46abeeca9b4f641783734cf1b4ec3c19-CkA3NTBiODdiZDU5ZmExOTM5NDZkMDE3ZDYxMzY1ODljODAxOWY0ZmQxOWNkZDA3YjIyOGQ4YzRlN2Y5ZjcyOGZj-2.0.0',
        'passport-sdk-version': '30990',
        'x-tt-ultra-lite': '1',
        'user-agent': 'com.zhiliaoapp.musically.go/350302 (Linux; U; Android 12; ar_IQ; Infinix X6816; Build/RP1A.200720.011;tt-ok/3.12.13.21-ul)',
        'cookie': 'passport_csrf_token=db2b50a67a5b31f81d3b470168449001; ...',  # Add your full cookie here
    }

    response = requests.get(url=url, params=params, headers=headers)
    response.raise_for_status()
    response_text = response.text
    
    with lock:
        total_checks += 1  # Increment total checks BY @marenastore
        if '"is_valid":true' in response_text:
            total_hits += 1  # Increment total hits BY @marenastore
            message = f'New Username Hit: {username}  //  Total Checks: {total_checks}  //  Total Hits:  {total_hits}' 
            requests.post(f'https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text={message}')
            with open("hits.txt", "a") as f:
                f.write(f"New Username: {username} // Total Checks: {total_checks} // Total Hits BY @marenastore : {total_hits}\n")
        else:
            total_fails += 1  # Increment total fails BY @marenastore

        # Print status to terminal BY @marenastore
        print(f'CHECKED: {total_checks} : HIT: {total_hits}')

def thread_function():
    while True:
        try:
            username = generate_random_name()
            check_username(username)
        except Exception as e:
            print(f"Error: {e}")

def main():
    num_threads = 400  # Adjust the number of threads as needed BY @marenastore
    threads = []

    for _ in range(num_threads):
        t = threading.Thread(target=thread_function)
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

if __name__ == "__main__":
    main()
