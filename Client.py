import socket
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

        # Initialize var for server and client
        self.server_host = '127.0.0.1'
        self.server_port = 12345
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_host, self.server_port))

        self.server_path = R"server_data"

        self.files_arr = [item for item in os.listdir(self.server_path)]

        self.file_count = len(self.files_arr)

        # Set instruction
        self.label = ttk.Label(root, text="Select a file to upload or write the number of the file you want to download/delete : ")
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

        # Set field to enter a number for file number
        self.file_num = tk.StringVar()
        self.file_num_entry = ttk.Entry(root, validate='key', textvariable=self.file_num)
        self.file_num_entry['validatecommand'] = (self.file_num_entry.register(self.validate_entry), '%P')
        self.file_num_entry.pack(pady=10, ipadx=100)

        # Set button to start upload file
        self.start_upload_button = ttk.Button(root, text="Start Upload", command=lambda: self.StartAction("Upload"))
        self.start_upload_button.pack(pady=10)

        # Set button to start download file
        self.start_download_button = ttk.Button(root, text="Start Download", command=lambda: self.StartAction("Download"))
        self.start_download_button.pack(pady=10)

        # Set button to start delete file
        self.start_delete_button = ttk.Button(root, text="Delete File", command=lambda: self.StartAction("Delete"))
        self.start_delete_button.pack(pady=10)

        # Set button to show files's server
        self.start_show_files_button = ttk.Button(root, text="Show Server's Files", command=self.WriteFilesOnScreen)
        self.start_show_files_button.pack(pady=10)

        # Set lable
        self.status_label = ttk.Label(root, text="System status :")
        self.status_label.pack(pady=10)

        # Set area for status for every file
        self.text_status = tk.Text(root, height=20, width=100, state="disabled", background="black")
        self.text_status.pack(pady=10)
        self.text_status.tag_configure("defult", foreground="white")
        self.text_status.tag_configure("title", foreground="green")
        self.text_status.tag_configure("action", foreground="blue")

        # Set quit button
        self.quit_button = ttk.Button(root, text="Quit", command=lambda: self.StartAction("Quit")) # root.quit
        self.quit_button.pack(pady=10)
        
        # Update the path area if the user choose a file
        self.root.drop_target_register(DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.UpdateFileEntry)

        self.WriteFilesOnScreen()

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

    def WriteOnScreen(self, result, tag):
        # The function get result and tag that the result is the message and the tag is the color of the message and show it to the user
        self.text_status.config(state=tk.NORMAL)
        self.text_status.insert(tk.END, result + "\n\n", tag)
        self.text_status.config(state=tk.DISABLED)
        self.text_status.see(tk.END)

    def UpdateFilesArr(self):
        # The function update the arr of the files and the count by the folder
        self.files_arr = [item for item in os.listdir(self.server_path)]
        self.file_count += 1

    def WriteFilesOnScreen(self):
        # The function write on the screen the files list of the server
        self.UpdateFilesArr()
        if len(self.files_arr) == 0:
            self.WriteOnScreen("Server is empty.", "title")
        else:
            self.WriteOnScreen("Files list : ", "title")
            for i in range(len(self.files_arr)):
                self.WriteOnScreen(f"{i + 1} - {self.files_arr[i]}", "defult")


    def StartAction(self, action):
        # The function get action and do the action
        if action == "Delete":
            # The action send the server request to delete the file that its number is what the user entered
            if not self.file_num.get() == "":
                file_name = self.files_arr[int(self.file_num.get()) - 1]
                self.client_socket.send(f"{action},{file_name}".encode('utf-8'))
        elif action == "List":
            # The action send the server action to list all the files
            self.client_socket.send(f"{action}".encode('utf-8'))
        elif action == "Download":
            # The action send the server request to download the file with his action, file name, size and content of the file
            if not self.file_num.get() == "":
                file_name = self.files_arr[int(self.file_num.get()) - 1]
                file_chose_path = os.path.join(self.server_path, file_name)
                file_size = os.path.getsize(file_chose_path)

                with open(file_chose_path, 'rb') as file:
                    file_content = file.read()

                send_data = f"{action},{file_name},{file_size}"
                self.client_socket.send(send_data.encode('utf-8'))
                self.client_socket.sendall(file_content)

        elif action == "Upload":
            # The action send the server request to upload the file to the server with his action, file name, size and content of the file
            file_chose_path = self.file_path.get()
            if not self.file_path.get() == "":

                file_name = os.path.basename(file_chose_path)
                file_size = os.path.getsize(file_chose_path)
                with open(file_chose_path, 'rb') as file:
                    file_content = file.read()

                send_data = f"{action},{file_name},{file_size}"
                self.client_socket.send(send_data.encode('utf-8'))
                self.client_socket.sendall(file_content)

        elif action == "Quit":
            # The action send the server request to close the program
            self.client_socket.send(action.encode('utf-8'))
        
        # Check if the server can send a return message
        if action == "Upload" and not self.file_path.get() == "" \
        or action == "Download" and not self.file_num.get() == "" \
        or action == "Delete" and not self.file_num.get() == "" \
        or action == "Quit":
            
            # Get the data from server and show a message to the user
            data = self.client_socket.recv(1024).decode('utf-8')
            cmd, msg = data.split(",")

            if cmd == "DISCONNECTED":
                self.WriteOnScreen(f"[SERVER]: {msg}", "action")
                self.client_socket.close()
                self.root.quit()
                
            elif cmd == "ERROR":
                self.WriteOnScreen(f"[SERVER]: {msg}", "action")

            elif cmd == "OK":
                self.WriteOnScreen(f"{msg}", "action")
                self.UpdateFilesArr()
            self.file_num.set("")
            self.file_path.set("")

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = SystemFiles(root)
    root.mainloop()