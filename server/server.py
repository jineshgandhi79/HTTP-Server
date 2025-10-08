import sys
from socket_server import start_server
from config import HOST, PORT, MAX_THREADS

def main():
    host = HOST
    port = PORT
    threads = MAX_THREADS
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    if len(sys.argv) > 2:
        host = sys.argv[2]
    if len(sys.argv) > 3:
        threads = int(sys.argv[3])
    start_server(host, port, threads)

if __name__ == "__main__":
    main()
