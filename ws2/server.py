import socket
import datetime

HOST = '127.0.0.1'  # Localhost
PORT = 50007        # Arbitrary non-privileged port

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f"Server listening on {HOST}:{PORT}")
        while True:
            conn, addr = s.accept()
            with conn:
                print(f"Connected by {addr}")
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    message = data.decode()
                    print(f"Received: {message}")
                    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                    ack = f"Acknowledged at {timestamp}"
                    conn.sendall(ack.encode())
                print(f"Connection with {addr} closed.")

if __name__ == "__main__":
    main()