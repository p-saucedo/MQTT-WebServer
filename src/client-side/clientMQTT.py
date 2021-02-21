import paho.mqtt.client as mqtt
import threading
from time import sleep

class MQTTClient:

    def __init__(self, hostname):
        self.hostname = hostname
        self.client = None
        self.topics_suscribed = []
        self.html = ''
        self.last_topic = ''

    def on_connect(self, client, userdata, flags, rc):
        print("MQTTClient connected with result code " + str(rc))
        self.client.subscribe("home")
        self.topics_suscribed.append("home")
        self.last_topic = self.topics_suscribed[-1]

    def on_message(self,client, userdata, msg):
        print(msg.topic + " " + str(msg.payload))
        self.html = msg.payload.decode("utf-8") 

    def run_client(self):

        def listen(client):
            client.loop_forever()

        

        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message

        self.client.connect(self.hostname, 1883, 60)

        x = threading.Thread(target=listen, args = (self.client,))
        x.start()

    def get_html(self):
        return self.html

    def suscribe(self, route):
        try:
            self.client.subscribe(route)
            self.html = ''
            sleep(1)

            if self.get_html() == '':
                return False
            else:
                return True
        except ValueError:
            return ''
            
        return ''

        