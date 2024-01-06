import socket
import os
import threading

# Initialize var for the server and client
server_host = '127.0.0.1'
server_port = 12345
server_path = "server_data"
client_path = "client_data"

def handle_client(client_socket, client_address):
    print(f"Connecting with : {client_address}")
    while True:
        # Get the action that the client sent
        data = client_socket.recv(1024).decode('utf-8')
        data = data.split(",")
        action = data[0]

        # Check if action is list
        if action == "List":
            # Return the client a message include the files details
            files = os.listdir(server_path)
            send_data = "OK,"

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                send_data += "\n".join(f for f in files)
            client_socket.send(send_data.encode('utf-8'))

        # Check if action is upload
        elif action == "Upload":
            # Get the rest data and upload the file to the server and return to the client appropriate message
            file_name = data[1]
            file_size = int(data[2])
            
            file_content = b""
            while len(file_content) < file_size:
                file_content += client_socket.recv(1024)

            filepath = f"{server_path}\{file_name}"
            with open(filepath, "wb") as f:
                f.write(file_content)

            send_data = "OK,File uploaded successfully."
            client_socket.send(send_data.encode('utf-8'))

        # Check if action is download
        elif action == "Download":
            # Get the rest data and download the file to the client folder and return to the client appropriate message
            file_name = data[1]
            file_size = int(data[2])
            file_path = os.path.join(server_path, file_name)
            destination_path = os.path.join(client_path, file_name)

            if os.path.exists(file_path):

                file_content = b""
                while len(file_content) < file_size:
                    file_content += client_socket.recv(1024)

                with open(destination_path, 'wb') as file:
                    file.write(file_content)

                client_socket.send(f"OK,The file downloaded for client_data folder successfully.".encode('utf-8'))

            else:
                client_socket.send("ERROR,File not found.".encode('utf-8'))

        # Check if action is deleted
        elif action == "Delete":
            # Get the rest data and delete the file from the server and return to the client appropriate message
            files = os.listdir(server_path)
            send_data = "OK,"
            filename = data[1]

            if len(files) == 0:
                send_data += "The server directory is empty"
            else:
                if filename in files:
                    os.remove(f"{os.getcwd()}\{server_path}\{filename}")
                    send_data += "File deleted successfully."
                else:
                    send_data += "File not found."

            client_socket.send(send_data.encode('utf-8'))

        # Check if action is quit
        elif action == "Quit":
            break
    # Exit
    client_socket.send(f"DISCONNECTED, Server disconnected".encode('utf-8'))
    client_socket.close()
    print(f"[DISCONNECTED] {client_address} disconnected")

def main():
    print("[STARTING] Server is starting")
    # Initalize server socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((server_host, server_port))
    server_socket.listen()
    print(f"Server listen to {server_host} : {server_port}")

    while True:
        # Wait for request and run thread to do the request
        client_socket, client_address = server_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    main()