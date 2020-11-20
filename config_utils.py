import json


class Config:
    def __init__(self):
        with open("./videoCaptureConfig.json") as f:
            config_data = f.read()
            self.config = json.loads(config_data)

    def get_data_center_config(self):
        host = self.config["data_center"]["host"]
        port = self.config["data_center"]["port"]
        return host, port

    def get_video_server_config(self):
        host = self.config["video_server"]["host"]
        port = self.config["video_server"]["port"]
        return host, port

    def get_value(self, *args):
        value = self.config
        for k in args:
            value = value[k]
        return value
