import tkinter as tk
from tkinter import scrolledtext
import subprocess
import threading
import queue
import shlex

class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.queue = queue.Queue()
        self.grid()
        self.create_widgets()

    def create_widgets(self):
        self.eth_label = tk.Label(self, text="Network Adapter")
        self.eth_label.grid(row=0, column=0)
        self.eth_entry = tk.Entry(self)
        self.eth_entry.grid(row=0, column=1)

        self.mac_label = tk.Label(self, text="MAC Prefix")
        self.mac_label.grid(row=1, column=0)
        self.mac_entry = tk.Entry(self)
        self.mac_entry.grid(row=1, column=1)

        self.run_button = tk.Button(self)
        self.run_button["text"] = "Run Scan"
        self.run_button["command"] = self.run_tshark
        self.run_button.grid(row=2, column=0, columnspan=2)

        self.results_text = scrolledtext.ScrolledText(self, width=70, height=10)
        self.results_text.grid(row=3, column=0, columnspan=2)

        self.quit = tk.Button(self, text="QUIT", fg="red", command=self.master.destroy)
        self.quit.grid(row=4, column=0, columnspan=2)

        self.check_queue()

    def check_queue(self):
        while not self.queue.empty():
            line = self.queue.get()
            self.results_text.insert(tk.END, line)
        self.after(100, self.check_queue)

    def run_tshark(self):
        eth_interface = self.eth_entry.get()
        mac_prefix = self.mac_entry.get()
        command = f'tshark -l -i {eth_interface} -Y "(eth.src contains {mac_prefix})"'
        threading.Thread(target=self.run_command, args=(command,)).start()

    def run_command(self, command):
        process = subprocess.Popen(shlex.split(command), stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while process.poll() is None:
            output = process.stdout.readline()
            if output:
                self.queue.put(output.decode())
        rc = process.poll()

root = tk.Tk()
root.title("Vision MAC Scanner")
root.iconbitmap('C:\\Users\\Jack\\Desktop\\Scripts\\Vision\\Vision.ico') 
app = Application(master=root)
app.mainloop()

