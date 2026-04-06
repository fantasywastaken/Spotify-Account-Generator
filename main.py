import httpx
import sys
import os
import json
import threading
from time import sleep, perf_counter
from random import choice, choices, randint, uniform
from string import ascii_letters, ascii_lowercase, digits
from datetime import datetime
from colorama import Fore, init

init()

PRINT_LOCK = threading.Lock()
FILE_LOCK = threading.Lock()
COUNTER_LOCK = threading.Lock()

V1_API_KEYS = [
    "a1e486e2729f46d6bb368d6b2bcda326",
    "4c7a36d5260abca4af282779720cf631",
]


class Logger:
    created = 0

    @staticmethod
    def success(content):
        with PRINT_LOCK:
            now = datetime.now().strftime("%H:%M:%S")
            print(
                f"  {Fore.GREEN}[+]{Fore.RESET} "
                f"{Fore.WHITE}{content}{Fore.RESET}"
                f"  {Fore.LIGHTBLACK_EX}({now}){Fore.RESET}"
            )

    @staticmethod
    def error(content):
        pass

    @staticmethod
    def info(content):
        pass

    @staticmethod
    def thread_closed(content):
        pass


def set_terminal_title(title):
    if sys.platform.startswith("win"):
        try:
            from ctypes import windll
            windll.kernel32.SetConsoleTitleW(title)
        except Exception:
            pass
    else:
        sys.stdout.write(f"\x1b]2;{title}\x07")
        sys.stdout.flush()


def title_changer(target):
    set_terminal_title("Initializing...")
    start = perf_counter()
    while True:
        sleep(0.5)
        elapsed = perf_counter() - start
        speed = round(Logger.created / max(elapsed / 60, 0.001), 1)
        base = f"Spotify Creator | Created: {Logger.created} | Speed: {speed}/m | {round(elapsed, 1)}s"
        if target > 0:
            remaining = target - Logger.created
            set_terminal_title(f"{base} | Remaining: {remaining}")
            if remaining <= 0:
                sleep(3)
                Logger.thread_closed("Target reached. Shutting down.")
                sleep(2)
                os._exit(0)
        else:
            set_terminal_title(base)


def generate_username():
    vowels = choices("aeiouy", k=randint(3, 5))
    consonants = choices("bcdfghjklmnpqrstvwxyz", k=randint(4, 6))
    nick = [f"{v}{c}" for v, c in zip(vowels, consonants)]
    prefix = ""
    sep1 = ""
    suffix = ""
    if choice((True, False)):
        sep1 = "_" if choice((True, False)) else ""
        prefix = choice((
            "Mr", "Ms", "Sir", "Doctor", "Lord", "Lady", "General", "Captain",
            "Glide", "Dazzle", "Daydream", "Micro", "Lion", "Punch", "Hawk",
            "Sandy", "Hound", "Rusty", "Tigress", "Commando", "Invincible",
            "Detective", "Vanguard", "Storm", "Marine", "Saber", "Thunder",
            "Discoverer", "Explorer", "Cardinal", "Winner", "Bee", "Coach",
            "Munchkin", "Teddy", "Scout", "Smarty", "Dolly", "Princess",
            "Pumpkin", "Sunshine", "Bestie", "Sugar", "Juliet", "Magician",
            "Alpha", "Grace", "Buck", "King", "Chief", "Ace", "Mortal",
            "Speedy", "Bug", "Senior", "Bear", "Insomnia", "Creature",
            "Miracle", "SuperHero", "Boss", "Meow", "Rapunzel", "Drum",
        ))
    if choice((True, False)):
        sep2 = "_" if choice((True, False)) else ""
        suffix = f"{sep2}{randint(1, 99)}"
    return prefix + sep1 + "".join(nick).capitalize() + suffix


def generate_password():
    base = "".join(choices(ascii_letters + digits, k=12))
    return base + choice("!@#$%&*") + str(randint(0, 9))


def generate_birthday():
    return f"{randint(1970, 2004)}-{randint(1, 12):02d}-{randint(1, 28):02d}"


def generate_mail():
    domains = [
        "gmail.com", "yahoo.com", "outlook.com", "hotmail.com",
        "protonmail.com", "icloud.com", "mail.com", "zoho.com",
        "yandex.com", "aol.com", "gmx.com", "fastmail.com",
    ]
    name = "".join(choices(ascii_lowercase + digits, k=randint(8, 14)))
    return f"{name}@{choice(domains)}"


class SpotifyGen:
    def __init__(self):
        try:
            with open("config.json", "r", encoding="utf-8") as fh:
                self.config = json.load(fh)
        except (json.JSONDecodeError, FileNotFoundError) as exc:
            Logger.error(f"Config error: {exc}")
            sys.exit(1)

        self.threads = max(self.config.get("threads", 1), 1)
        self.target = self.config.get("target", 0)

        proxy_cfg = self.config.get("proxy", {})
        if proxy_cfg.get("enabled"):
            h = proxy_cfg["host"]
            p = proxy_cfg["port"]
            u = proxy_cfg.get("username", "")
            pw = proxy_cfg.get("password", "")
            if u and pw:
                self.proxy_url = f"http://{u}:{pw}@{h}:{p}"
            else:
                self.proxy_url = f"http://{h}:{p}"
            Logger.info(f"Proxy: {h}:{p}")
        else:
            self.proxy_url = None

    def _make_session(self):
        ua = (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
            "(KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36"
        )
        kw = {"headers": {"User-Agent": ua}, "timeout": 30}
        if self.proxy_url:
            kw["proxy"] = self.proxy_url
        return httpx.Client(**kw)

    def signup_v1(self, session, username, mail, password, birthday):
        bday = birthday.split("-")
        year, month, day = bday[0], bday[1].lstrip("0"), bday[2].lstrip("0")
        data = (
            f"birth_day={day}&birth_month={month}&birth_year={year}"
            f"&collect_personal_info=undefined&creation_flow=&creation_point=https://www.spotify.com/us/"
            f"&displayname={username}&email={mail}&gender={choice(['male', 'female'])}"
            f"&iagree=1&key={choice(V1_API_KEYS)}&password={password}&password_repeat={password}"
            f"&platform=www&referrer=&send-email=0&thirdpartyemail=0&fb=0"
        )
        headers = {
            "Accept": "*/*",
            "Content-Type": "application/x-www-form-urlencoded",
            "Referer": "https://www.spotify.com/",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en",
            "Host": "spclient.wg.spotify.com",
            "Origin": "https://www.spotify.com",
        }
        try:
            r = session.post(
                "https://spclient.wg.spotify.com/signup/public/v1/account",
                headers=headers, data=data,
            )
            if r.status_code == 200:
                resp = r.json()
                status = resp.get("status", 0)
                if status == 1:
                    return True
                elif status == 2:
                    Logger.error(f"Rejected: {resp.get('errors', {})}")
                else:
                    Logger.error(f"Status {status}: {r.text[:200]}")
            else:
                Logger.error(f"HTTP {r.status_code}")
        except Exception as exc:
            Logger.error(f"Signup error: {exc}")
        return False

    def worker(self):
        while True:
            if self.target > 0 and Logger.created >= self.target:
                break

            try:
                mail = generate_mail()
                username = generate_username()
                password = generate_password()
                birthday = generate_birthday()

                sleep(uniform(1, 2))

                session = self._make_session()
                Logger.info(f"Signing up {username}...")
                ok = self.signup_v1(session, username, mail, password, birthday)
                session.close()

                if ok:
                    with COUNTER_LOCK:
                        Logger.created += 1
                    Logger.success(f"{username} | {mail}")
                    with FILE_LOCK:
                        with open("accounts.txt", "a", encoding="utf-8") as fh:
                            fh.write(f"{username}:{mail}:{password}\n")
                    sleep(uniform(2, 4))
                else:
                    sleep(uniform(3, 6))

            except Exception as exc:
                Logger.error(f"{exc}")
                sleep(3)

        Logger.thread_closed(f"{threading.current_thread().name} finished.")

    def start(self):
        threads = []
        for i in range(self.threads):
            t = threading.Thread(target=self.worker, name=f"Worker-{i + 1}")
            t.start()
            threads.append(t)
            if self.threads > 1:
                sleep(3)

        for t in threads:
            t.join()

        print(f"\n  {Fore.GREEN}Done!{Fore.RESET} {Logger.created} accounts saved to accounts.txt")


if __name__ == "__main__":
    SpotifyGen().start()
