import json
import socket
from time import sleep


class Client:
    def __init__(self, address, port):
        self.address = address
        self.port = port
        self.conn = socket.socket()
        self.is_reconnecting = False

    def connect(self):
        count = 0
        while True:
            try:
                self.conn.connect((self.address, self.port))
                self.is_reconnecting = False
                print("Connection success after %d reconnection(s) at %s:%d" % (count, self.address, self.port))
                return
            except Exception as e:
                self.is_reconnecting = True
                self.conn = socket.socket()
                count += 1
                print(str(e) + " at %s:%d ...... %d" % (self.address, self.port, count))
                sleep(1)

    def send_to_video_server(self, camera_id, data_type, data_byte):
        data_byte = "header".encode() + (len(data_byte) + 8).to_bytes(length=4, byteorder="little", signed=True) \
                    + camera_id.to_bytes(length=4, byteorder="little", signed=True) \
                    + data_type.to_bytes(length=4, byteorder="little", signed=True) + data_byte
        try:
            self.conn.send(data_byte)
        except Exception as e:
            print(str(e) + ": Reconnecting " + str(self.address) + ":" + str(self.port))
            self.conn = socket.socket()
            self.connect()

    def send_to_data_center(self, data):
        data_json = json.dumps(data)
        data_byte = data_json.encode()
        data_byte = "header".encode() + len(data_byte).to_bytes(length=4, byteorder="little", signed=True) + data_byte
        try:
            self.conn.send(data_byte)
            print("send register information successfully")
        except Exception as e:
            print(str(e) + ": Reconnecting " + str(self.address) + ":" + str(self.port))
            self.conn = socket.socket()
            self.connect()


if __name__ == "__main__":
    client = Client("localhost", 9090)
    client.send("hello")
