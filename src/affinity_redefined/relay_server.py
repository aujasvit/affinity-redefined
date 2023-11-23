import socketserver
import json
import event
import server_settings
import pickle
import encrypt

class Server(socketserver.BaseServer):
    def __init__(self, key: encrypt.Key):
        self.key = key
        self.relay_list_path = server_settings.relay_list_path

class TCPHandler(socketserver.BaseRequestHandler):

    def handle(self):
        self.data = self.request.recv(1024).strip()
        
        if self.data[0] == "EVENT":
            event = json.loads(self.data[1])

            if event["kind"] == event.Event.UPDATE_RELAY_LIST:
                #Updating relay list
                with open(self.server.relay_list_path, "w") as F:
                    F.write(event["content"])

            elif event["kind"] == event.Event.NEW_RELAY_ADDITION:
                #New relay joining event
                server_info = event["content"] #(ip, port, lat, lon)
                with open(self.server.relay_list_path, "ab") as F:
                    pickle.dump(server_info, F)
                
                with open(self.server.relay_list_path, "rb") as F:
                    # Make new event of type 15000 to push updated relay list to all relays
                    updated_list = F.read()
                    updated_list_event = event.Event(key = self.server.key.public_key_hex, kind = event.Event.UPDATE_RELAY_LIST, tags = [], content = updated_list)
                    trasmit_data = ["EVENT", updated_list_event.json_string]
                    F.seek(0)
                    while True:
                        try:
                            (ip,lat,lon) = pickle.load(F)
                            if ip == server_info[0]:
                                continue
                            # Send transmit_data
                            
                        except EOFError:
                            break

        elif self.data[0] == "REQ":
            filters = json.loads(self.data[2])
            if event.Event.UPDATE_RELAY_LIST in filters["kinds"]:
                updated_list = []
                with open(self.server.relay_list_path, "rb") as F:
                        updated_list = F.read()

                updated_list_event = event.Event(key = self.server.key.public_key_hex, kind = event.Event.UPDATE_RELAY_LIST, tags = [], content = updated_list)
                trasmit_data = ["EVENT", updated_list_event.json_string]
                self.request.sendall(updated_list)