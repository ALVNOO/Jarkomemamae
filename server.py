import socket
import signal
import sys
import os

def inisiasi(port=80):
    addr = ("127.0.0.1", port)
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(addr)
    sock.listen(1)
    print(f"Server initialized on {addr}")
    return {"socket": sock, "addr": addr}

def read_file(path):
    content = ""
    with open(path, "r") as f:
        content = f.read()
    return content

def normalisasi(path):
    path = f".{path}"
    if path.endswith("/"):
        path = path[:-1]
    if os.path.isdir(path):
        path += "/index.html"
    return path

def serve(http, callback=lambda host, port: None):
    def __sigint_handler(sig, frame):
        close(http)
        sys.exit(0)

    signal.signal(signal.SIGINT, __sigint_handler)
    callback(http["addr"][0], http["addr"][1])

    while True:
        (csock, addr) = http["socket"].accept()
        print(f"Accepted connection from {addr}")
        msg = csock.recv(4096).decode()
        if not msg:
            csock.close()
            continue

        head = msg.rstrip().split("\n")[0].split()
        if len(head) < 2:
            csock.send(f"HTTP/1.1 400 Bad Request\r\n".encode())
            csock.close()
            continue

        path = normalize_path(head[1])
        print(f"Requested path: {path}")

        if not os.path.exists(path):
            csock.send(f"HTTP/1.1 404 Not Found\r\n".encode())
            csock.close()
            continue

        content = read_file(path)
        csock.send(f"HTTP/1.1 200 OK\n\n{content}\r\n".encode())
        print(f"Sent content of {path} to {addr}")
        csock.close()

def close(http):
    print("Shutting down server...")
    http["socket"].close()

if __name__ == "__main__":
    http = inisiasi()
    serve(http, lambda host, port: print(f"Serving HTTP on {host} port {port} ..."))
