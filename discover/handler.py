import socket
import threading
from time import sleep

from db.zone_manager import return_zone_in_string, update_zone
from conf.conf_reader import config

SERVER_TIMEOUT = 1


class ServerThread(threading.Thread):
    """
    udp server manage by this thread, this server is used for receive zones file to update client zone
    Discover Connection has an object of this class which is used to control udp server
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
                if data:
                    update_zone(data, addr)
            except socket.timeout:  # TODO: find better solution to recvfrom block function
                # server run until is_server_stop is False
                if self.is_server_stop:
                    break


class SendZoneThread(threading.Thread):
    def __init__(self, connection):
        super().__init__()
        self.connection = connection
        self.is_thread_stop = False

    def run(self):
        interval = config.getint('Discover', 'send_zone_interval')
        while not self.is_thread_stop:
            clients_list = return_zone_in_string()  # get list of all clients
            for client in clients_list[:-1]:  # last record in zone is the current client
                name, ip, port, distance = client.split()
                self.connection.send_zone(clients_list, ip, port)
            sleep(interval)


class DiscoverConnection:
    """
    this class manage udp connection to exchange zones between clients
    """

    def __init__(self,
                 connection_ip,
                 connection_port,
                 start_receiving_server=True,
                 start_send_zone_thread=True):
        self.server_address = (connection_ip, connection_port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(self.server_address)
        self.stop_server = False
        if start_receiving_server:
            self.server = self.start_server()
        if start_send_zone_thread:
            self.send_zone_thread = self.start_sending_zone_thread()

    def start_server(self):
        """
        create a thread to run udp server
        """
        server = ServerThread(self.sock)
        server.start()
        return server

    def send_zone(self, zone, receiver_ip, receiver_port):
        """
        send zone for receiver_ip:receiver_port
        :param zone: zone pass as list so must be converted to byte before sending
        :return: length of bytes are sent
        """
        zone = bytes('\n'.join(zone), encoding='UTF-8')
        try:
            return self.sock.sendto(zone, (receiver_ip, int(receiver_port)))
        except Exception:   # server might be unreachable or other issues
            pass

    def start_sending_zone_thread(self):
        """
        send zone for all clients included in zone file
        """
        send_thread = SendZoneThread(self)
        send_thread.start()
        return send_thread

    def close(self):
        """
        stop thread server and close connection
        """
        if hasattr(self, 'server'):
            self.server.is_server_stop = True
            self.server.join()
        if hasattr(self, 'send_zone_thread'):
            self.send_zone_thread.is_thread_stop = True
            self.send_zone_thread.join()
        self.sock.close()


def start_discover_connection():
    ip = config.get('General', 'ip')
    port = config.getint('Discover', 'port')
    DiscoverConnection(ip, port)
