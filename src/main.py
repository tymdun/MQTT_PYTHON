import tkinter as tk
import inputparsing
import paho.mqtt.client as mqtt

HEIGHT = 700
WIDTH = 1000

# print(inputparsing.mqtt_client_parse_arguments())
configList = inputparsing.mqtt_check_inputs()
print(configList)
client = mqtt.Client(configList[2], clean_session=False)
#client.connect(configList[0], configList[1])

# exit()

root = tk.Tk()
root.title("MQTT CHAT ROOM")

canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()


onlineUsers = tk.Frame(root, bg='#018786')
onlineUsers.place(relwidth=0.4, relheight=0.75)
onlineText = tk.Text(onlineUsers)
onlineText.pack(pady=0.1, padx=0.1, fill='both')
onlineText.insert(tk.END, "HELLO WORLD")
onlineText.config(state='disabled')

messages = tk.Frame(root, bg='#800080')
messages.place(relx=0.4, relwidth=0.6, relheight=0.75)

inputBox = tk.Frame(root, bg='#192734')
inputBox.place(rely=0.75, relwidth=1, relheight=0.25)

button = tk.Button(inputBox, text="TEST BUTTON", bg='black')
button.place(relheight=0.05, relwidth=0.1, rely=0.95, relx=0.5)


root.mainloop()
