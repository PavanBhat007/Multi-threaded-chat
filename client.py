import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog
import random
import colorsys

HOST = '127.0.0.1'
PORT = 9090

class Client:
    def __init__(self, host, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.nickname = simpledialog.askstring("Nickname", "Enter your Username", parent=msg)
        self.gui_done = False
        self.running = True
        self.gui_ready_event = threading.Event()
        gui_thread = threading.Thread(target=self.gui_loop)
        
        receive_thread = threading.Thread(target=self.receive)
        gui_thread.start()
        self.gui_ready_event.wait()
        receive_thread.start()

    def gui_loop(self):
        self.win = tkinter.Tk()
        self.win.title("Community Chat Forum")
        self.win.geometry("500x600")
        self.win.config(bg="#333333")

        self.chat_label = tkinter.Label(self.win, text="COMMUNITY CHAT FORUM", bg="#4CAF50", fg="white", font=("Arial", 14, "bold"))
        self.chat_label.pack(padx=20, pady=5, fill=tkinter.X)

        self.chat_label = tkinter.Label(self.win, text=f"Username: {self.nickname}", bg="#333333", fg="#CCCCCC", font=("Arial", 10))
        self.chat_label.pack(padx=20, pady=5, fill=tkinter.X)

        self.chat_label = tkinter.Label(self.win, text=f"NOTE: Type \\PRIV <username> <message> to send a private chat", bg="#333333", fg="#CCCCCC", font=("Arial", 8))
        self.chat_label.pack(padx=20, pady=5, fill=tkinter.X)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.win, bg="#222222", fg="#FFFFFF", wrap=tkinter.WORD)
        self.text_area.pack(padx=20, pady=5, fill=tkinter.BOTH, expand=True)
        self.text_area.config(state='disabled')

        self.msg_label = tkinter.Label(self.win, text="Message: ", bg="#333333", fg="#CCCCCC", font=("Arial", 12))
        self.msg_label.pack(padx=20, pady=5, fill=tkinter.X)

        self.input_area = tkinter.Text(self.win, height=3, bg="#222222", fg="#FFFFFF")
        self.input_area.pack(padx=20, pady=5, fill=tkinter.X)
        self.input_area.bind("<Return>", self.write_on_enter)
        self.input_area.bind("<Shift-Return>", self.add_newline_on_shift_enter)

        self.send_button = tkinter.Button(self.win, text="Send", command=self.write, bg="#4CAF50", fg="white")
        self.send_button.config(font=("Arial", 12))
        self.send_button.pack(padx=20, pady=5, fill=tkinter.X)

        self.gui_ready_event.set()
        self.gui_done = True
        self.win.protocol("WM_DELETE_WINDOW", self.stop)

        self.win.mainloop()

    def random_color(self):
        # Generate a random hue value
        hue = random.random()
        
        # Convert the HSV color to RGB
        rgb = colorsys.hsv_to_rgb(hue, 0.8, 0.8)

        # Scale the RGB values to the range 0-255
        rgb = [int(val * 255) for val in rgb]

        # Return the color as a hexadecimal string
        return f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}"

    def write_on_enter(self, event):
        if event.state & 0x1:  # Check if Shift key is pressed
            self.input_area.insert(tkinter.END, '\n')
        else:
            self.write()

    def add_newline_on_shift_enter(self, event):
        self.input_area.insert(tkinter.END, '\n')

    def stop(self):
        self.running = False
        self.sock.send("\\QUIT".encode('utf-8'))
        self.sock.close()
        self.win.destroy()
        exit(0)

    def write(self):
        message = self.input_area.get('1.0', 'end').strip()
        if message:
            if message.startswith("\\PRIV"):
                self.sock.send(message.encode('utf-8'))
            else:
                message = f"{self.nickname}: {message}"
                self.sock.send(message.encode('utf-8'))
            self.input_area.delete('1.0', 'end')

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                print(message)
                if message == "NICK":
                    self.sock.send(self.nickname.encode('utf-8'))
                elif message.startswith("IPA"):
                    clt2 = message.split(":")[1].strip()
                    print(clt2)
                else:
                    if self.gui_done:
                        self.win.after(0, self.update_text_area, message)
            except ConnectionAbortedError:
                break
            except Exception as e:
                print(f"ERROR: {e}")
                self.sock.close()
                break
            
    def update_text_area(self, message):
        self.text_area.config(state='normal')

        # Split the message at the first colon
        split_message = message.split(":", 1)

        if len(split_message) == 2:
            username, rest_of_message = split_message
        else:
            # If the split fails, use the entire message as the username
            username = message
            rest_of_message = ""

        # Generate a random color for the username
        color = self.random_color()

        # Add a tag for the username with the random color and bold style
        self.text_area.tag_configure(username, foreground=color, font=('Arial', 10, 'bold'))

        # Insert the message with the colored and bold username
        self.text_area.insert(tkinter.END, f"{username}:", (username, username))
        self.text_area.insert(tkinter.END, rest_of_message + '\n')

        self.text_area.yview(tkinter.END)
        self.text_area.config(state='disabled')




client = Client(HOST, PORT)
