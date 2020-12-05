import tkinter as tk
import inputparsing
import paho.mqtt.client as mqtt

# print(inputparsing.mqtt_client_parse_arguments())
configList = inputparsing.mqtt_check_inputs()
print(configList)
mqtt.Client(configList[2], clean_session=False, )

exit()

root = tk.Tk()

button = tk.Button(root, text="TEST BUTTON", bg='red')
button.pack()


root.mainloop()
