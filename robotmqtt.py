
import threading
import time
import logging
import json
import paho.mqtt.client as mqtt

from robot import Robot


def convert_position (jpos):
    """
    Convert a JSON position into its floating point coordinate in the range [0.0, 1.0]
    
    Parameters
    ----------
        position : float or string.
            The JSON position. If the valure received is an string it will be translated according to the 
            following rules:
               - "left"  : will be translated to 0.0
               - "right" : will be translated to 1.0
               - "down"  : will be translated to 0.0
               - "up"    : will be translated to 1.0

    Returns
    -------
        float
            The floating point coordinate in the range [0.0, 1.0].
    """
    if ((type(jpos) is unicode) or (type(jpos) is str)):
        if (jpos == "up"):
            return 1.0
        elif (jpos == "down"):
            return 0.0
        elif (jpos == "left"):
            return 0.0
        elif (jpos == "right"):
            return 1.0
        else:
            raise ValueError("unknown positon: {}".format(jpos))
            
    elif ((type(jpos) is float) or (type(jpos) is int)):
        if ((jpos >= 0.0) and (jpos <= 1.0)):
            return (float)(jpos)
        else:
            raise ValueError("positon out of range: {}".format(jpos))
    else:
        raise TypeError("invalid type: {}".format(type(jpos)))
    

# The callback for when a PUBLISH message is received from the server.
#
def on_message(client, robot, msg):
    
    logging.debug("topic={} payload={}".format(msg.topic ,msg.payload))
            
    try:
        if (msg.topic.startswith("robot/body/")):
            #----------------------------------
            # operate with the body.
            #----------------------------------

            # process the parameters.
            #
            params = json.loads(msg.payload)
            logging.debug("params={}".format(params))
            
            position = convert_position(params["position"])

            # get the body part.
            #
            part = msg.topic.replace("robot/body/", "")
            if (part == "right_arm"):
                robot.body().right_arm_move(position)
            elif (part == "left_arm"):
                robot.body().left_arm_move(position)
            elif (part == "neck"):
                robot.body().neck_move(position)
            else:
                raise SyntaxError('invalid part: "{}"'.format(part))

        elif (msg.topic.startswith("robot/head/")):
            #----------------------------------
            # operate with the head.
            #----------------------------------

            # process the parameters.
            #
            params = json.loads(msg.payload)
            logging.debug("params={}".format(params))
            
            position = convert_position(params["position"])

            # get the head part.
            #
            part = msg.topic.replace("robot/head/", "")
            if (part == "left_eye"):
                robot.head().left_eye_move(position)
            elif (part == "right_eye"):
                robot.head().right_eye_move(position)
            else:
                raise SyntaxError('invalid part: "{}"'.format(part))

        elif (msg.topic == "robot/shutdown"):
            #----------------------------------
            # shutdown the robot and terminate.
            #----------------------------------

            robot.shutdown ()
            client.disconnect()
            
    except ValueError as e:
        msg = 'value error: "{}"'.format(e)
        logging.debug(msg)
    except TypeError as e:
        msg = '"type error: {}"'.format(e)
        logging.debug(msg)
    except SyntaxError as e:
        msg = '"syntax error: {}"'.format(e)
        logging.debug(msg)

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
    shutdown = False
    client.loop_forever()
    
    

