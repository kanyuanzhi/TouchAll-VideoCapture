import cv2
from config_utils import Config
from socket_client import Client
from json import loads
from random import randint

config = Config()
video_server_host, video_server_port = config.get_video_server_config()
data_center_host, data_center_port = config.get_data_center_config()

camera_host = config.get_value("camera_host")

image_quality = config.get_value("image_quality")

client_of_data_center = Client(data_center_host, data_center_port)
client_of_data_center.connect()
client_of_video_server = Client(video_server_host, video_server_port)
client_of_video_server.connect()


def capture(camera_id, camera_host, image_quality):
    if camera_host == "0":
        camera_host = 0
    cap = cv2.VideoCapture(camera_host)
    while True:
        ret, frame = cap.read()
        encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), image_quality]
        image = cv2.imencode('.jpg', frame, encode_param)[1]
        image_byte = image.tobytes()
        client_of_video_server.send_to_video_server(camera_id, 50, image_byte)


if __name__ == "__main__":
    register = {
        "data_type": 50,
        "camera_host": camera_host
    }
    client_of_data_center.send_to_data_center(register)
    message_bytes = client_of_data_center.conn.recv(1024)
    message_str = message_bytes.decode()
    message_json = loads(message_str)
    use_mysql = message_json["use_mysql"]
    if use_mysql:
        camera_id = message_json["camera_id"]
        text = "监控摄像机在数据中心注册成功，当前设备ID: {}"
    else:
        camera_id = randint(65535, 70000)
        text = "当前数据中心未连接至mysql，设备无法获取正确ID，已经为监控摄像机分配临时ID: {}供测试使用"
    print(text.format(camera_id, camera_host))
    capture(camera_id, camera_host, image_quality)
