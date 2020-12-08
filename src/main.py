import tkinter as tk
import inputparsing
import paho.mqtt.client as mqtt
import time
import logging
import json
import datetime
import random

HEIGHT = 700
WIDTH = 1000
ONLINEUSERS_COLOR = '#018786'
MESSAGE_COLOR = '#800080'
INPUT_COLOR = '#192734'
onlineUsersNameList = []
onlineUsersStatusList = []

# Event handling function ----------------------------------------------


def sendMessage():
    messageContents = inputTxt.get("1.0", "end")
    inputTxt.delete("1.0", "end")
    currentTime = int(time.time())
    jsonInPy = {"timestamp": currentTime,
                "name": configList[2], "message": messageContents}
    jsonToSend = json.dumps(jsonInPy)
    logging.info("The json to be sent: " + jsonToSend)
    client.publish(configList[3] + "/message",
                   payload=jsonToSend, qos=1, retain=0)


def enterPressed(Event):
    sendMessage()


# Creates The GUI ----------------------------------------------------------------

# Creates the root gui
root = tk.Tk()
root.title("MQTT CHAT ROOM")
root.geometry(str(WIDTH) + "x" + str(HEIGHT))

# Creates the frame and textbox for the user online info
onlineUsers = tk.Frame(root)
onlineUsers.place(relwidth=0.4, relheight=0.75)
onlineText = tk.Text(onlineUsers, bg=ONLINEUSERS_COLOR, bd=5, pady=20, padx=20)
onlineText.place(relheight=1, relwidth=1)
onlineText.config(state='disabled')

# Creates the message box which shows all the user messages
messages = tk.Frame(root)
messages.place(relx=0.4, relwidth=0.6, relheight=0.75)
messageTxt = tk.Text(messages, bg=MESSAGE_COLOR, bd=5, pady=20, padx=20)
messageTxt.place(relheight=1, relwidth=1)


inputBox = tk.Frame(root)
inputBox.place(rely=0.75, relwidth=1, relheight=0.25)
inputSendBtn = tk.Button(inputBox, text="Send",
                         bg='white', command=sendMessage)
inputSendBtn.place(relx=0.8, relheight=1, relwidth=0.2)
inputTxt = tk.Text(inputBox, bg=INPUT_COLOR, bd=5,
                   pady=20, padx=20, fg='white')
inputTxt.place(relheight=1, relwidth=0.8)

# Event Bindings
root.bind('<Return>', enterPressed)

# Helper Functions -------------------------------------------------------------------------------


def printMessage(messageJson):
    epochTime = messageJson["timestamp"]
    epochTime = int(epochTime)
    timeRecieve = datetime.datetime.fromtimestamp(epochTime)
    # messageTxt.insert("end", timeRecieve)
    messageTxt.config(state='normal')
    messageTxt.insert(
        "end", str(timeRecieve) + " " + messageJson["name"] + ": " + messageJson["message"] + '\n')
    messageTxt.config(state='disabled')


# def printOnline(username):
#    onlineText.config(state='normal')
#    onlineText.insert(
#        "end", username["name"] + ": " + str(username["online"]) + '\n')
#    onlineText.config(state='disabled')

def printOnline(username, status):
    onlineText.config(state='normal')
    statusString = "null"
    x = 0
    print(username)
    print(status)
    onlineText.delete('1.0', "end")
    while x < len(username):
        if status[x]:
            statusString = "online"
        else:
            statusString = "offline"
        onlineText.insert(
            "end", username[x] + ": " + statusString + '\n')
        x = x + 1
    onlineText.config(state='disabled')


def createLastWill():
    jsonInPy = {"name": configList[2], "online": 0}
    jsonToSend = json.dumps(jsonInPy)
    logging.info("The last will: " + jsonToSend)
    return jsonToSend


# MQTT HANDLERS FOR PYTHON -------------------------------------------------------


def on_message(client, userdata, message):
    # print(str(message.payload.decode("utf-8")))
    nameAlreadyExists = False
    statusUpdated = False
    indexToUpdate = -1
    x = 0
    logging.info("message received " + str(message.payload.decode("utf-8")))
    logging.info("message topic=" + message.topic)
    logging.info("message qos=" + str(message.qos))
    logging.info("message retain flag=" + str(message.retain))
    tempString = str(message.payload.decode("utf-8"))
    # print(tempString)
    if "timestamp" in tempString:
        try:
            jsonToPy = json.loads(tempString)
            printMessage(jsonToPy)
        except json.decoder.JSONDecodeError:
            logging.info("Invalid format recieved")
    elif "online" in tempString:
        try:
            jsonToPy = json.loads(tempString)
            if len(onlineUsersNameList) is 0:
                onlineUsersNameList.append(jsonToPy["name"])
                onlineUsersStatusList.append(jsonToPy["online"])
            while x < len(onlineUsersNameList):
                if onlineUsersNameList[x] == jsonToPy["name"]:
                    nameAlreadyExists = True
                    indexToUpdate = x
                    if onlineUsersStatusList[x] == jsonToPy["online"]:
                        statusUpdated = True
                        break
                x = x + 1
            if not statusUpdated and indexToUpdate is not -1:
                onlineUsersStatusList[indexToUpdate] = jsonToPy["online"]
            if not nameAlreadyExists:
                onlineUsersNameList.append(jsonToPy["name"])
                onlineUsersStatusList.append(jsonToPy["online"])
            printOnline(onlineUsersNameList, onlineUsersStatusList)

         #   if jsonToPy['name'] not in onlineUsers:
         #       onlineUsersList.append((jsonToPy["name"], jsonToPy["online"]))
         #       printOnline(jsonToPy)

            # jsonToPy = json.loads(tempString)
            # printOnline(jsonToPy)
            # else:
            #    print("Not there")
        except json.decoder.JSONDecodeError:
            logging.info("Invalid format recieved")


def on_publish(client, userdata, mid):
    logging.info("message succesfully sent")


def on_connect(client, userdata, flags, rc):
    logging.info("Connected")
    jsonInPy = {"name": configList[2], "online": 1}
    jsonToSend = json.dumps(jsonInPy)
    logging.info("The json to be sent: " + jsonToSend)
    client.publish(configList[3] + "/status",
                   payload=jsonToSend, qos=1, retain=1)


def on_disconnect(client, userdata, rc):
    logging.info("Disconnected")
    jsonInPy = {"name": configList[2], "online": 0}
    jsonToSend = json.dumps(jsonInPy)
    logging.info("The json to be sent: " + jsonToSend)
    client.publish(configList[3] + "/status",
                   payload=jsonToSend, qos=1, retain=1)


configList = inputparsing.mqtt_check_inputs()
print(configList)
# generates random Client for MQTT
randomizeClient = f'{configList[3]}-{random.randint(0, 1000)}'
client = mqtt.Client(randomizeClient, clean_session=False)
lastWillJson = createLastWill()
print(lastWillJson)
client.on_message = on_message
client.on_connect = on_connect
client.on_publish = on_publish
client.on_disconnect = on_disconnect
client.will_set("+/status", lastWillJson, qos=1, retain=1)
client.connect(configList[0], int(configList[1]))
client.loop_start()
client.subscribe("+/message", qos=1)
client.subscribe("+/status", qos=1)
time.sleep(0.5)
root.mainloop()
client.loop_stop()
on_disconnect(client, 0, 0)
