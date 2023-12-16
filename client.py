<<<<<<< Updated upstream
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090

class Client:
  def __init__(self, host, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host, port))

    msg = tkinter.Tk()
    msg.withdraw()

    self.nickname = simpledialog.askstring("Nickname", "Enter your Username", parent = msg)
    self.gui_done = False
    self.running = True
    gui_thread = threading.Thread(target=self.gui_loop)
    recieve_thread = threading.Thread(target=self.recieve)

    gui_thread.start()
    recieve_thread.start()

  def gui_loop(self):
    self.win = tkinter.Tk()
    self.win.config(bg="lightgray")

    self.chat_label = tkinter.Label(self.win, text="Chat: ", bg="lightgray")
    self.chat_label.config(font=("Arial", 12))
    self.chat_label.pack(padx=20, pady=5)

    self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
    self.text_area.pack(padx=20, pady=5)
    self.text_area.config(state='disabled')

    self.msg_label = tkinter.Label(self.win, text="Message: ", bg="lightgray")
    self.msg_label.config(font=("Arial", 12))
    self.msg_label.pack(padx=20, pady=5)

    self.input_area = tkinter.Text(self.win, height=3)
    self.input_area.pack(padx=20, pady=5)

    self.send_button = tkinter.Button(self.win, text="Send", command = self.write)
    self.send_button.config(font=("Arial", 12))
    self.send_button.pack(padx=20, pady=5)

    self.gui_done = True
    self.win.protocol("WM_DELETE_WINDOW", self.stop)
    
    self.win.mainloop()
    

  def stop(self):
    self.running = False
    self.win.destroy()
    self.sock.close()
    exit(0)
  
  def write(self):
    message = f"{self.nickname}: {self.input_area.get('1.0', 'end')}"
    self.sock.send(message.encode('utf-8'))
    self.input_area.delete('1.0', 'end')

  def recieve(self):
    while self.running:
      try:
        message = self.sock.recv(1024).decode('utf-8')
        if message == "NICK":
          self.sock.send(self.nickname.encode('utf-8'))
        else:
          if self.gui_done:
            self.text_area.config(state='normal')
            self.text_area.insert('end', message)
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
      except ConnectionAbortedError:
        break
      except:
        print("ERROR")
        self.sock.close()
        break

=======
import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = '127.0.0.1'
PORT = 9090

class Client:
  def __init__(self, host, port):
    self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.sock.connect((host, port))

    msg = tkinter.Tk()
    msg.withdraw()

    self.nickname = simpledialog.askstring("Nickname", "Enter your Username\t\t\t", parent = msg).capitalize()
    self.gui_done = False
    self.running = True
    gui_thread = threading.Thread(target=self.gui_loop)
    recieve_thread = threading.Thread(target=self.recieve)

    gui_thread.start()
    recieve_thread.start()

  def gui_loop(self):
    self.win = tkinter.Tk()
    self.win.title("Multi-Threaded Chat :)")
    self.win.config(bg="lightgray")

    self.chat_label = tkinter.Label(self.win, text=f"Chat: {self.nickname}", bg="lightgray")
    self.chat_label.config(font=("Arial", 18))
    self.chat_label.pack(padx=20, pady=5)

    self.text_area = tkinter.scrolledtext.ScrolledText(self.win)
    self.text_area.pack(padx=20, pady=5)
    self.text_area.config(state='disabled')

    self.msg_label = tkinter.Label(self.win, text="Message: ", bg="lightgray")
    self.msg_label.config(font=("Arial", 15))
    self.msg_label.pack(padx=20, pady=5)

    self.input_area = tkinter.Text(self.win, height=3)
    self.input_area.pack(padx=20, pady=5)

    self.send_button = tkinter.Button(self.win, text="Send", command = self.write)
    self.send_button.config(font=("Arial", 15))
    self.send_button.pack(padx=20, pady=5)

    self.gui_done = True
    self.win.protocol("WM_DELETE_WINDOW", self.stop)
    
    self.win.mainloop()
    

  def stop(self):
    self.running = False
    self.win.destroy()
    self.sock.close()
    exit(0)
  
  def write(self):
    message = f"\n {self.nickname}: {self.input_area.get('1.0', 'end')}"
    self.sock.send(message.encode('utf-8'))
    self.input_area.delete('1.0', 'end')

  def recieve(self):
    while self.running:
      try:
        message = self.sock.recv(1024).decode('utf-8')
        if message == "NICK":
          self.sock.send(self.nickname.encode('utf-8'))
        else:
          if self.gui_done:
            
            try:
              tmp = message.split(":")
              nick = tmp[0].strip()
              mssg = tmp[1].strip() + "\n"
            except IndexError:
              if len(tmp) == 1:
                    nick = ''
                    mssg = message + "\n"
            
            self.text_area.tag_config('name', foreground='red')
            self.text_area.tag_config('msg', foreground='blue')
            
            self.text_area.config(state='normal')
            self.text_area.insert('end', nick, 'name')
            self.text_area.insert('end', " > ")
            self.text_area.insert('end', mssg, 'msg')
            self.text_area.yview('end')
            self.text_area.config(state='disabled')
      except ConnectionAbortedError:
        break
      # except:
      #   print("ERROR")
      #   self.stop()
      #   break

>>>>>>> Stashed changes
client = Client(HOST, PORT)