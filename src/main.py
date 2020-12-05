import tkinter as tk
import inputparsing
import paho.mqtt.client as mqtt

HEIGHT = 700
WIDTH = 1000
NUMROWS = 8
NUMWINDOS = 8
ONLINEUSERS_COLOR = '#018786'
MESSAGE_COLOR = '#800080'
INPUT_COLOR = '#192734'

# print(inputparsing.mqtt_client_parse_arguments())
configList = inputparsing.mqtt_check_inputs()
print(configList)
client = mqtt.Client(configList[2], clean_session=False)
# client.connect(configList[0], configList[1])

# exit()

root = tk.Tk()
root.title("MQTT CHAT ROOM")
root.rowconfigure(NUMROWS)
root.columnconfigure(NUMWINDOS)
root.geometry(str(WIDTH) + "x" + str(HEIGHT))

# canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
# canvas.pack()


onlineUsers = tk.Frame(root)
onlineUsers.place(relwidth=0.4, relheight=0.75)
onlineText = tk.Text(onlineUsers, bg=ONLINEUSERS_COLOR, bd=5, pady=20, padx=20)
onlineText.place(relheight=1, relwidth=1)
onlineText.insert(tk.END, "HELLO WORLD")
onlineText.config(state='disabled')

messages = tk.Frame(root)
messages.place(relx=0.4, relwidth=0.6, relheight=0.75)
messageTxt = tk.Text(messages, bg=MESSAGE_COLOR, bd=5, pady=20, padx=20)
messageTxt.place(relheight=1, relwidth=1)
messageTxt.insert(tk.END, "HELLO WORLD")
# messageTxt.config(state='disabled')

inputBox = tk.Frame(root)
inputBox.place(rely=0.75, relwidth=1, relheight=0.25)
inputTxt = tk.Text(inputBox, bg=INPUT_COLOR, bd=5,
                   pady=20, padx=20, fg='white')
inputTxt.place(relheight=1, relwidth=1)

# Event handling function ----------------------------------------------


def sendMessage(Event):
    print("HERE")
    messageContents = inputTxt.get("1.0", "end")
    inputTxt.delete("1.0", "end")
    print(messageContents)


    # Event Bindings
root.bind('<Return>', sendMessage)


# button = tk.Button(inputBox, text="TEST BUTTON", bg='black')
# button.place(relheight=0.05, relwidth=0.1, rely=0.95, relx=0.5)


root.mainloop()
