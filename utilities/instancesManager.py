import socket
import threading
import time

class OtherInstanceError(Exception):
    pass

class ProgramInstanceManager:
    _server_running = False
    _server_closed = False
    
    def __init__(self, port=35217, ip="127.0.0.1"):
        self.ip, self.port = ip, port
        is_first = self.check_instance()
        if not is_first:
            raise OtherInstanceError()

        self.setup_server()

    def check_instance(self):
        # setup a TCP socket with 2 sec timeout
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        try:
            sock.connect((self.ip, self.port))
        except socket.timeout:
            # no connection was made in time
            # so we can assume that we are the
            # only one
            return True
        sock.close()
        return False

    def setup_server(self):
        # setup a TCP server socket with 2 sec timeout
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.serversock.settimeout(2)
        self.serversock.bind((self.ip, self.port))

        self.server_thread = threading.Thread(target=self._server_run)
        self.server_thread.start()

    def _server_run(self):
        self._server_running = True
        self.serversock.listen(5)

        while self._server_running:
            try:
                conn, addr = self.serversock.accept()
                conn.close()
            except socket.timeout:
                pass

        self.serversock.close()
        self._server_closed = True

    def shutdown(self):
        self._server_running = False
        while not self._server_closed:
            time.sleep(0.1)