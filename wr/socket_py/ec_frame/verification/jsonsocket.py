import json
import socket
import struct
import time
from multiprocessing.pool import ThreadPool

def _send(conn, msg):
    sent = 0
    while sent < len(msg):
        sent += conn.send(msg[sent:])


def _read(conn, size):
    data = b''
    while len(data) < size:
        data_tmp = conn.recv(size - len(data))
        data += data_tmp
        if data_tmp == '':
            raise RuntimeError("socket connection broken")
    return data


def _msg_length(conn):
    d = _read(conn, 4)
    s = struct.unpack('!I', d)
    return s[0]

class JsonSocket(object):
    def __init__(self, address='127.0.0.1', port=5489):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # self.conn = self.socket
        self._timeout = None
        self._address = address
        self._port = port

    def send_obj(self, obj, conn):
        msg = json.dumps(obj)
        frmt = "=%ds" % len(msg)
        packed_msg = struct.pack(frmt, msg.encode('ascii'))
        packed_hdr = struct.pack('!I', len(packed_msg))
        _send(conn, packed_hdr)
        _send(conn, packed_msg)

    def read_obj(self, conn):
        size = _msg_length(conn)
        data = _read(conn, size)
        frmt = "=%ds" % size
        msg = struct.unpack(frmt, data)
        return json.loads(msg[0])

    def close(self):
        self.socket.close()

    def _get_timeout(self):
        return self._timeout

    def _set_timeout(self, timeout):
        self._timeout = timeout
        self.socket.settimeout(timeout)

    def _get_address(self):
        return self._address

    def _set_address(self, address):
        pass

    def _get_port(self):
        return self._port

    def _set_port(self, port):
        pass

    timeout = property(_get_timeout, _set_timeout, doc='Get/set the socket timeout')
    address = property(_get_address, _set_address, doc='read only property socket address')
    port = property(_get_port, _set_port, doc='read only property socket port')


class JsonServer(JsonSocket):
    def __init__(self, address='127.0.0.1', port=8080, capacity = 1):
        super(JsonServer, self).__init__(address, port)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((self.address, self.port))
        self.capacity = capacity

    def receive(self, client):
        data = self.read_obj(client)
        client.close()
        return data


    def serve(self):
        # self.socket.listen(self.capacity)
        # pool = ThreadPool(processes=self.capacity)
        # input_data = [None] * self.capacity
        # for i in range(self.capacity):
        #     client, _ = self.socket.accept()
        #     client.settimeout(self.timeout)
        #     input_data[i] = pool.apply_async(self.receive, (client,))
        # pool.close()
        # pool.join()
        # self.socket.close()
        # return input_data
        self.socket.listen(self.capacity)
        # pool = ThreadPool(processes=self.capacity)
        input_data = [None] * self.capacity
        client = [None] * self.capacity
        for i in range(self.capacity):
            client[i], _ = self.socket.accept()
            client[i].settimeout(self.timeout)
            # input_data[i] = pool.apply_async(self.receive, (client,))
            input_data[i] = self.receive(client[i])
        # pool.close()
        # pool.join()
        self.socket.close()
        return input_data


class JsonClient(JsonSocket):
    def __init__(self, address='127.0.0.1', port=5489):
        super(JsonClient, self).__init__(address, port)

    def connect(self):
        for i in range(10):
            try:
                self.socket.connect((self.address, self.port))
            except socket.error as msg:
                print("SockThread Error: %s" % msg)
                time.sleep(3)
                continue
            return True
        return False

