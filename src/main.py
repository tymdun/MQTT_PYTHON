import tkinter as tk
import inputparsing
import paho.mqtt.client as mqtt
import time
import logging
import json
import datetime

HEIGHT = 700
WIDTH = 1000
ONLINEUSERS_COLOR = '#018786'
MESSAGE_COLOR = '#800080'
INPUT_COLOR = '#192734'

# Event handling function ----------------------------------------------


def sendMessage():
    messageContents = inputTxt.get("1.0", "end")
    inputTxt.delete("1.0", "end")
    currentTime = int(time.time())
    jsonInPy = {"timestamp": currentTime,
                "name": configList[2], "message": messageContents}
    jsonToSend = json.dumps(jsonInPy)
    logging.info("The json to be sent: " + jsonToSend)
    client.publish("tymdun/message", payload=jsonToSend, qos=1, retain=1)


def enterPressed(Event):
    sendMessage()


# Creates the gui parameters to follow
# Creates the root gui
root = tk.Tk()
root.title("MQTT CHAT ROOM")
root.geometry(str(WIDTH) + "x" + str(HEIGHT))

# Creates the frame and textbox for the user online info
onlineUsers = tk.Frame(root)
onlineUsers.place(relwidth=0.4, relheight=0.75)
onlineText = tk.Text(onlineUsers, bg=ONLINEUSERS_COLOR, bd=5, pady=20, padx=20)
onlineText.place(relheight=1, relwidth=1)
# onlineText.insert(tk.END, "HELLO WORLD")
onlineText.config(state='disabled')

# Creates the message box which shows all the user messages
messages = tk.Frame(root)
messages.place(relx=0.4, relwidth=0.6, relheight=0.75)
messageTxt = tk.Text(messages, bg=MESSAGE_COLOR, bd=5, pady=20, padx=20)
messageTxt.place(relheight=1, relwidth=1)
# messageTxt.insert(tk.END, "HELLO WORLD")
# messageTxt.config(state='disabled')

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

# MQTT HANDLERS FOR PYTHON -------------------------------------------------------


def on_message(client, userdata, message):
    print(str(message.payload.decode("utf-8")))
    logging.info("message received " + str(message.payload.decode("utf-8")))
    logging.info("message topic=" + message.topic)
    logging.info("message qos=" + str(message.qos))
    logging.info("message retain flag=" + str(message.retain))
    tempString = str(message.payload.decode("utf-8"))
    print(tempString)
    try:
        jsonToPy = json.loads(tempString)
        # print(jsonToPy)
        epochTime = jsonToPy["timestamp"]
        epochTime = int(epochTime)
        timeRecieve = datetime.datetime.fromtimestamp(epochTime)
        messageTxt.insert("end", timeRecieve)
        messageTxt.config(state='normal')
        messageTxt.insert("end", " " + str(message.payload.decode("utf-8")))
        messageTxt.config(state='disabled')
    except json.decoder.JSONDecodeError:
        logging.info("Invalid format recieved")


def on_publish(client, userdata, mid):
    logging.info("message succesfully sent")


configList = inputparsing.mqtt_check_inputs()
print(configList)
client = mqtt.Client(configList[2], clean_session=False)
client.on_message = on_message
client.on_publish = on_publish
client.connect(configList[0], int(configList[1]))
client.loop_start()
client.subscribe("+/message", qos=1)
time.sleep(0.5)

# exit()


# button = tk.Button(inputBox, text="TEST BUTTON", bg='black')
# button.place(relheight=0.05, relwidth=0.1, rely=0.95, relx=0.5)

root.mainloop()
client.loop_stop()
