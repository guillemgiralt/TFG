
import threading
import time
import logging
import paho.mqtt.client as mqtt
import argparse
import sys

from robot import Robot

def convert_position (position):
    """
    Convert a string position into its floating point coordinate in the range [0.0, 1.0]
    
    Parameters
    ----------
        position : string.
            The new position as strinf. The following string values will be honnored as well:
               - "left"  : will be translated to 0.0
               - "right" : will be translated to 1.0
               - "down"  : will be translated to 0.0
               - "up"    : will be translated to 1.0

    Returns
    -------
        float
            The floating point coordinate in the range [0.0, 1.0] or -1.0 if the string is not valid or the position is out of range.
    """
    position = position.replace(",",".")
    if (position == "up"):
        p = 1.0
    elif (position == "down"):
        p = 0.0
    elif (position == "left"):
        p = 1.0
    elif (position == "right"):
        p = 0.0
    else:
        try:
            p = (float)(position)
            if ((p < 0.0) or (p > 1.0)):
                logging.error ("positon out of range: {}".format(position))
                p = -1.0
        except ValueError:
            logging.error ("invalid float: {}".format(position))
            p = -1.0
    return p
    

# The callback for when a PUBLISH message is received from the server.
#
def on_message(client, robot, msg):
    
    logging.debug("topic={} payload={}".format(msg.topic ,msg.payload))
            
    if (msg.topic.startswith("robot/body/")):
        #----------------------------------
        # operate with the body.
        #----------------------------------
        tokens = msg.topic.split('/')
        if (len(tokens) == 4):
            part   = tokens[2]
            action = tokens[3]
            if (part == "right_arm"):
                if (action == "move"):
                    position = convert_position(msg.payload)
                    if (position >= 0.0):
                        logging.debug('right arm move: "{}"'.format(position))
                        robot.body().right_arm_move(position)
                else:
                    logging.error('invalid right arm action: "{}"'.format(action))
            elif (part == "left_arm"):
                if (action == "move"):
                    position = convert_position(msg.payload)
                    if (position >= 0.0):
                        logging.debug('left arm move: "{}"'.format(position))
                        robot.body().left_arm_move(position)
                else:
                    logging.error('invalid left arm action: "{}"'.format(action))
            elif (part == "neck"):
                if (action == "move"):
                    position = convert_position(msg.payload)
                    if (position >= 0.0):
                        logging.debug('left neck move: "{}"'.format(position))
                        robot.body().neck_move(position)
                else:
                    logging.error('invalid neck action: "{}"'.format(action))
            else:
                logging.error('invalid body part: "{}"'.format(part))
        else:
            logging.error('invalid body command: "{}"'.format(msg.topic))
            

    elif (msg.topic.startswith("robot/head/")):
        #----------------------------------
        # operate with the head.
        #----------------------------------
        tokens = msg.topic.split('/')
        if (len(tokens) == 4):
            part   = tokens[2]
            action = tokens[3]
            if (part == "right_eye"):
                if (action == "move"):
                    position = convert_position(msg.payload)
                    if (position >= 0.0):
                        logging.debug('right eye move: "{}"'.format(position))
                        robot.head().right_eye_move(position)
                else:
                    logging.error('invalid right arm action: "{}"'.format(action))
                
            elif (part == "left_eye"):
                if (action == "move"):
                    position = convert_position(msg.payload)
                    if (position >= 0.0):
                        logging.debug('left eye move: "{}"'.format(position))
                        robot.head().left_eye_move(position)
                else:
                    logging.error('invalid left arm action: "{}"'.format(action))
                
            elif (part == "neck_UD"):
                if (action == "move"):
                    position = convert_position(msg.payload)
                    if (position >= 0.0):
                        logging.debug('neck UD move: "{}"'.format(position))
                        robot.head().neck_UD_move(position)
                else:
                    logging.error('invalid neck UD action: "{}"'.format(action))
                    
            elif (part == "neck_LR"):
                if (action == "move"):
                    position = convert_position(msg.payload)
                    if (position >= 0.0):
                        logging.debug('neck LR move: "{}"'.format(position))
                        robot.head().neck_LR_move(position)
                else:
                    logging.error('invalid neck LR action: "{}"'.format(action))
            else:
                logging.error('invalid head part: "{}"'.format(part))
        else:
            logging.error('invalid head command: "{}"'.format(msg.topic))


    elif (msg.topic == "robot/dance"):
        #----------------------------------
        # initialze the robot and terminate.
        #----------------------------------
        logging.debug('dance')
        print("dance")

    elif (msg.topic == "robot/initialize"):
        #----------------------------------
        # initialze the robot and terminate.
        #----------------------------------
        logging.debug('initialize')
        robot.initialize ()

    elif (msg.topic == "robot/shutdown"):
        #----------------------------------
        # shutdown the robot and terminate.
        #----------------------------------
        logging.debug('shutdown')
        robot.shutdown ()

    elif (msg.topic == "robot/quit"):
        #----------------------------------
        # quit.
        #----------------------------------
        robot.shutdown ()
        client.disconnect()

    else:
        logging.error('invalid command: "{}"'.format(msg.topic))

if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Robot MQTT Interface.')
    parser.add_argument('-d', '--debug', action="store_true", dest="debug", default=False, help="enable debug mode")
    args = parser.parse_args()

    format = "%(asctime)s: %(message)s"
    if args.debug:
        logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    else:
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
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
    shutdown = False
    client.loop_forever()
    
    

