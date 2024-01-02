import socket

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_host = '127.0.0.1'
    server_port = 12345
    server_socket.bind((server_host, server_port))
    server_socket.listen(1)

    print(f"Server listen to {server_host} : {server_port}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"Connecting with : {client_address}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            
            message = data.decode('utf-8')
            print(f"The message received : {message}")

            client_socket.sendall(data)

        print(f"Lost connection with : {client_address}")
        client_socket.close()

if __name__ == '__main__':
    start_server()