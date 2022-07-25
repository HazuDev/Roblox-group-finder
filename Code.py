from genericpath import isdir
import sys, requests, threading, random, os
from termcolor import colored

class group:
    def __init__(self, name, groupId):
        self.Name = name
        self.Id = groupId

groupArray = []

def main():
    def isNumber(num):
        try:
            toNumber = int(num)
            return toNumber
        except:
            return None

    sys.stdout.write("---------\n")
    sys.stdout.write("Just some practice stuff\n")
    sys.stdout.write("---------\n")

    ask = input("Threads (Default 1) : ")
    toNumber = isNumber(ask)

    def getRandomId():
        global groupArray

        getId = False

        while getId == False:
            newId = random.randint(1000000, 15300000)

            if newId in groupArray:
                pass
            else:
                getId = True
                groupArray.append(newId)
                return newId

    def getGroupInfo():
        groupId = getRandomId()
        req = requests.get(f"https://www.roblox.com/groups/group.aspx?gid={groupId}")

        if "owned" not in req.text:
            newRequest = requests.get(f"https://groups.roblox.com/v1/groups/{groupId}")

            if "isLocked" not in newRequest.text and "owner" in newRequest.text:
                try:
                    if newRequest.json()["publicEntryAllowed"] == True and newRequest.json()["owner"] == None:
                        groupInfo = group(newRequest.json()["name"], newRequest.json()["id"])
                        print(colored(f"Found : {groupInfo.Id} / {groupInfo.Name}", "blue"))
                        input("Group founded (press enter to continue)")
                except:
                    input(f"Group founded : {groupId}")
                else:
                    try:
                        groupInfo = group(newRequest.json()["name"], newRequest.json()["id"])
                        print(colored(f"Found : {groupInfo.Id} / {groupInfo.Name} (Can't claim)", "red"))
                    except:
                        print(colored(f"Found : Banned group ({groupId})", "red"))
            else:
                try:
                    groupInfo = group(newRequest.json()["name"], newRequest.json()["id"])
                    print(colored(f"Found : {groupInfo.Id} / {groupInfo.Name} (Can't claim)", "red"))
                except:
                    print(colored(f"Found : Banned group ({groupId})", "red"))
        else:
            try:
                newRequest = requests.get(f"https://groups.roblox.com/v1/groups/{groupId}")
                groupInfo = group(newRequest.json()["name"], newRequest.json()["id"])
                print(colored(f"Found : {groupInfo.Id} / {groupInfo.Name} (Can't claim)", "red"))
            except:
                print(colored(f"Found : Banned group ({groupId})", "red"))
    
    if toNumber is None:
        print("Incorrect number, try again lol")
    else:
        while True:
            if threading.active_count() <= toNumber:
                threading.Thread(target = getGroupInfo).start()

if __name__ == "__main__":
    main()