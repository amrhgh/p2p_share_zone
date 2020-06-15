import socket
import threading

SERVER_TIMEOUT = 1


class ServerThread(threading.Thread):
    """
    udp server manage by this thread
    """
    def __init__(self, sock):
        super().__init__()
        self.sock = sock
        self.is_server_stop = False
        self.sock.settimeout(SERVER_TIMEOUT)

    def run(self):
        while True:
            try:
                data, addr = self.sock.recvfrom(1024)
                print(data, addr)
            except socket.timeout:  # TODO: find better solution to recvfrom block function
                # server run until is_server_stop is False
                if self.is_server_stop:
                    self.sock.close()
                    break

    def stop_server(self):
        self.is_server_stop = True


class DiscoverConnection:
    """
    this class manage udp connection to exchange zones between clients
    """

    def __init__(self,
                 connection_ip,
                 connection_port):
        self.server_address = (connection_ip, connection_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.server_address)
        self.stop_server = False
        self.server = self.start_server()

    def start_server(self):
        """
        create a thread to run udp server
        """
        server = ServerThread(self.sock)
        server.start()
        return server

    def send_zone(self, server_ip, server_port):
        self.sock.sendto(b'hi', (server_ip, server_port))

    def close(self):
        """
        stop thread server and close connection
        """
        self.server.stop_server()

