import threading
from queue import Queue
from utils import log
from http_handler import handle_request
from config import BUFFER_SIZE

class ThreadPool:
    def __init__(self, max_threads=10):
        self.queue = Queue()
        self.threads = []
        self.max_threads = max_threads
        for _ in range(max_threads):
            t = threading.Thread(target=self.worker, daemon=True)
            t.start()
            self.threads.append(t)

    def worker(self):
        while True:
            client_socket, addr = self.queue.get()
            log(f"Connection from {addr}")
            try:
                request_bytes = client_socket.recv(BUFFER_SIZE)
                if request_bytes:
                    response = handle_request(request_bytes)
                    client_socket.sendall(response)
            except Exception as e:
                log(f"Error handling request: {e}")
            finally:
                client_socket.close()
                self.queue.task_done()

    def add_connection(self, client_socket, addr):
        if self.queue.qsize() >= self.max_threads:
            log("Thread pool saturated, queuing connection")
        self.queue.put((client_socket, addr))
