import paho.mqtt.publish as publish
import sys
publish.single (sys.argv[1], payload=sys.argv[2] , hostname='localhost')

