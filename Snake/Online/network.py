import socket, json


class Network:

    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        self.s.connect((self.host, self.port))
        conf_data = json.loads(self.s.recv(1024).decode('ascii'))
        with open('config.json', 'w') as f:
            json.dump(conf_data, f)
        

    def send_data(self, keys):
        info = json.loads(open('config.json', 'r').read())
        if keys:
            key = keys[0]
        else:
            key = "no_key"
        data_to_send = {"keys": [f'snake_{info["id"]}_{key}'], "dead": False}
        data_to_send = bytes(json.dumps(data_to_send), encoding='ascii')
        self.s.sendall(data_to_send)

    def get_data(self):
        data = self.s.recv(1024).decode("ascii")
        data = data.replace("'", '"')
        return json.loads(data)