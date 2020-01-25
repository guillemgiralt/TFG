
import threading
import time
import logging
import json
import paho.mqtt.client as mqtt
from robot import Robot

# The callback for when a PUBLISH message is received from the server.
#
def on_message(client, robot, msg):
    
    logging.debug("topic={} payload={}".format(msg.topic ,msg.payload))
            
    if (msg.topic == "robot/right_arm"):
        # move the right arm.
        #
        params = json.loads(msg.payload)
        logging.debug("params={}".format(params))
        
        position = params["position"]
        if type(position) is unicode:
            if (position == "up"):
                robot.body().right_arm_up()
            elif (position == "down"):
                robot.body().right_arm_down()
            else:
                logging.debug("unkown positon: {}".format(position))
        elif type(position) is float:
            if ((position >= 0.0) and (position <= 1.0)):
                robot.body().right_arm_move(position)
            else:
                logging.debug("invalid positon: {}".format(position))
        else:
            logging.debug("invalid type: {}".format(type(position)))
            
    elif (msg.topic == "robot/left_arm"):
        # move the left arm.
        #
        params = json.loads(msg.payload)
        logging.debug("params={}".format(params))
        
        position = params["position"]
        if type(position) is unicode:
            if (position == "up"):
                robot.body().left_arm_up()
            elif (position == "down"):
                robot.body().left_arm_down()
            else:
                logging.debug("unkown positon: {}".format(position))
        elif type(position) is float:
            if ((position >= 0.0) and (position <= 1.0)):
                robot.body().left_arm_move(position)
            else:
                logging.debug("invalid positon: {}".format(position))
        else:
            logging.debug("invalid type: {}".format(type(position)))
            
    elif (msg.topic == "robot/neck_arm"):
        # move the neck arm.
        #
        params = json.loads(msg.payload)
        logging.debug("params={}".format(params))
        
        position = params["position"]
        if type(position) is unicode:
            if (position == "up"):
                robot.body().neck_up()
            elif (position == "down"):
                robot.body().neck_down()
            else:
                logging.debug("unkown positon: {}".format(position))
        elif type(position) is float:
            if ((position >= 0.0) and (position <= 1.0)):
                robot.body().neck_move(position)
            else:
                logging.debug("invalid positon: {}".format(position))
        else:
            logging.debug("invalid type: {}".format(type(position)))
            
    elif (msg.topic == "robot/shutdown"):
        # shutdown the robot
        #
        robot.shutdown ()

if __name__ == "__main__":
    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    
    # create the robot.
    #
    robot = Robot("walle")
    robot.initialize()
    
    # create the MQTT client.
    #
    client = mqtt.Client(robot.name(), True, robot)

    # connect to the broker.
    #
    client.connect("localhost", 1883, 60)

    # setup the callbacks and subscribe tho the robot topics.
    #
    client.on_message    = on_message
    client.subscribe("robot/#")

    # Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
    #
    client.loop_forever()
    

