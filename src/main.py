import tkinter as tk
import inputparsing


inputparsing.mqtt_client_parse_arguments()

exit()

root = tk.Tk()

button = tk.Button(root, text="TEST BUTTON", bg='red')
button.pack()


root.mainloop()
