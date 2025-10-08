import socket
from thread_pool import ThreadPool
from config import HOST, PORT, MAX_THREADS

def start_server(host=HOST, port=PORT, max_threads=MAX_THREADS):
    pool = ThreadPool(max_threads)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen(50)
        print(f"HTTP Server started on http://{host}:{port}")
        print(f"Thread pool size: {max_threads}")
        print(f"Serving files from 'resources' directory")
        print("Press Ctrl+C to stop the server")
        while True:
            client_sock, addr = s.accept()
            pool.add_connection(client_sock, addr)
