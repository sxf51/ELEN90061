import socket

SERVER_IP = '127.0.0.1'
SERVER_PORT = 50007

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.connect((SERVER_IP, SERVER_PORT))
            print(f"Connected to server at {SERVER_IP}:{SERVER_PORT}")
            while True:
                msg = input("Enter message (type 'exit' to quit): ")
                s.sendall(msg.encode())
                if msg.lower() == "exit":
                    print("Exiting client.")
                    data = s.recv(1024)
                    print("Received from server:", data.decode())
                    s.shutdown(socket.SHUT_RDWR)
                    break
                data = s.recv(1024)
                print("Received from server:", data.decode())
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()