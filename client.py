import socket

def request_file(server_ip, server_port, file_path):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server_ip, server_port))
        print(f"Connected to server at {server_ip}:{server_port}")

        request = f"GET {file_path} HTTP/1.1\r\nHost: {server_ip}\r\n\r\n"
        sock.send(request.encode())
        print(f"Sent request for {file_path}")

        response = sock.recv(4096).decode()
        print("Response from server:")
        print(response)

    except ConnectionRefusedError:
        print("Failed to connect to the server. Make sure the server is running.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        sock.close()
        print("Connection closed.")

if __name__ == "__main__":
    server_ip = "124.0.0.1"
    server_port = 80
    file_path = "/jarkom.html"  # Change this to the desired file path
    request_file(server_ip, server_port, file_path)
