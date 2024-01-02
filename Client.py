import socket
import Server
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import TkinterDnD, DND_FILES
import requests
import os
import time

class SystemFiles():
    def __init__(self, root):
        self.root = root
        # Set title
        self.root.title("System Upload - Download files")

        self.file_count = len([item for item in os.listdir(R"C:\Users\raz\Desktop\פרויקטים מועדון המתכנתים\מערכת מאובטחת להעלאת והורדת קבצים\UploadDownloadFilesSecSys\files")])

        # Set instruction
        self.label = ttk.Label(root, text="Select a file ot upload or write the number of the file you want to download : ")
        self.label.pack(pady=10)

        # Set file path var
        self.file_path = tk.StringVar()
        self.file_path_entry = ttk.Entry(root, textvariable=self.file_path, state="readonly")
        self.file_path_entry.pack(pady=10, ipadx=100)

        # Set button to browse a single file
        self.browse_file_button = ttk.Button(root, text="Browse File", command=self.BrowseFile)
        self.browse_file_button.pack(pady=10)

        # Set instruction
        self.label_for_num = ttk.Label(root, text="Select the number of the file : ")
        self.label_for_num.pack(pady=10)

        # 
        self.file_num = tk.StringVar()
        self.file_num_entry = ttk.Entry(root, validate='key')
        self.file_num_entry['validatecommand'] = (self.file_num_entry.register(self.validate_entry), '%P')
        self.file_num_entry.pack(pady=10, ipadx=100)

        # Set button to start the scan
        self.start_upload_button = ttk.Button(root, text="Start Upload", command=self.StartUpload)
        self.start_upload_button.pack(pady=10)

        # Set button to start the scan
        self.start_download_button = ttk.Button(root, text="Start Download", command=self.StartDownload)
        self.start_download_button.pack(pady=10)

        # Set lable
        self.status_label = ttk.Label(root, text="System status :")
        self.status_label.pack(pady=10)

        # Set area for stuts for every file
        self.text_status = tk.Text(root, height=20, width=100, state="disabled", background="black")
        self.text_status.pack(pady=10)
        self.text_status.tag_configure("defult", foreground="white")

        # Set quit button
        self.quit_button = ttk.Button(root, text="Quit", command=root.quit)
        self.quit_button.pack(pady=10)
        
        # Update the path area if the user choose a file or folder
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.UpdateFileEntry)

    def BrowseFile(self):
        # The function ask directory of the file and set it as path
        file_path = filedialog.askopenfilename()
        if file_path:
            self.file_path.set(file_path)

    def validate_entry(self, text):
        # Only allow digits
        try:
            text = int(text)
            if text in range(1, self.file_count + 1):
                return True
        except:
            text = str(text)
            self.file_num.set(text[:-1])
            if len(text) == 0:
                return True
        return False
    
    def UpdateFileEntry(self, event):
        # The function update the path if the user define path
        file_path = event.data
        self.file_path.set(file_path)

    def StartDownload():
        pass

    def StartUpload():
        pass




    def start_client():
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_host = '127.0.0.1'
        server_port = 12345

        client_socket.connect((server_host, server_port))
        print(f"Connected to {server_host} : {server_port}")

        while True:
            message = input("Enter your mwssage ('exit' - quit) : ")
            if message.lower() == 'exit':
                break

            client_socket.sendall(message.encode('utf-8'))
            data = client_socket.recv(1024)
            ret_message = data.decode('utf-8')

            print(f"Server's answer : {ret_message}")

        print("Lost connection")
        client_socket.close()

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = SystemFiles(root)
    root.mainloop()