import requests
import os

from pathlib import Path

url = "https://b78ac1045cca.ngrok.io"
key = "not-found"

os.system("mkdir -p ~/.config/pswm/")
os.system("touch ~/.config/pswm/keys")

with open(f"{str(Path.home())}/.config/pswm/keys", "r+") as file:
    key = file.readline()
    if key == '':
        file.write("not-found")
        key = "not-found"

def write_key(key):
    with open("/home/sumit/.config/pswm/keys", "r+") as file:
        file.truncate(0)
        file.write(key)

def add_password(website: str, password):
    site = website.casefold()
    global url
    url = f"{url}/POST/{key}/{site}:{password}"
    response = requests.get(url).json()
    if key == "not-found" and response["result"] == 1:
        write_key(response["key"])
    print("response")
    return response["result"]

def get_password(website: str):
    site = website.casefold()
    response = requests.get(f"{url}/GET/PASS/{key}/{site}").json()
    print(response)
    return {
        "success": True if response["result"] == "success" else False,
        "passwords": response["passwords"] if "passwords" in response else []
    }

if __name__ == '__main__':
    while True:
        print("What Would You Like To Do?")
        print("1. Add A Password")
        print("2. Get A Password")
        print("3. Replace The Current Fernet Key (you should only choose this if there is a security threat)")

        choice = input("Enter a index: ")
        if choice == "1":
            site = input("Name of the site: ")
            password = input("Enter your password: ")

            print("Adding...")
            # try:
            add_password(site, password)
            print("Added")
            # except:
            #     print("It Didn't Worked!!!")
            #     print("It was most likely due to a Fernet Key loss, We advice to immediately withdraw all your data!")
            break
        if choice == "2":
            site = input("Enter the name of the site: ")
            print("Making a Request to the API...")
            result = get_password(site)
            if result["success"] == True:
                print("Password found: ")
                print(result["passwords"])
            else:
                print("Password not found! Try re-checking the Fernet key and the site name")
            break
        if choice == "3":
            print("Feature under work....")
            break
