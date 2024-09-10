import socket
import threading
import json

class SocketServer:
    def __init__(self, host='0.0.0.0', port=8888):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))
        self.clients = {}

    def start(self):
        self.sock.listen(5)
        print(f"Server listening on {self.host}:{self.port}")
        while True:
            client, address = self.sock.accept()
            client_thread = threading.Thread(target=self.handle_client, args=(client, address))
            client_thread.start()

    def handle_client(self, client, address):
        print(f"New connection from {address}")
        self.clients[address] = client
        while True:
            try:
                data = client.recv(1024)
                if not data:
                    break
                message = json.loads(data.decode('utf-8'))
                self.broadcast(message, address)
            except Exception as e:
                print(f"Error handling client {address}: {e}")
                break
        self.clients.pop(address, None)
        client.close()

    def broadcast(self, message, sender_address):
        for addr, client in self.clients.items():
            if addr != sender_address:
                try:
                    client.send(json.dumps(message).encode('utf-8'))
                except Exception as e:
                    print(f"Error broadcasting to {addr}: {e}")

if __name__ == "__main__":
    server = SocketServer()
    server.start()