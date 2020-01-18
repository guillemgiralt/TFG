
from robothead import RobotHead
from robotbody import RobotBody
from robotservo import RobotServo
import threading
import time
import logging

if __name__ == "__main__":
    #robothead = RobotHead()
    #robotbody = RobotBody(robothead)
    #robotbody.initialize()

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    
    right = RobotServo(0,0,100,logging)
    right.initialize(0.0)

    left = RobotServo(1,100,0,logging)
    left.initialize(0.0)

    right.move(0.5)
    left.move(0.5)
    right.wait()
    left.wait()
    
    right.move(1.0, 0.1, 20)
    right.wait()
    
    left.move(1.0, 0.1, 10)
    left.wait()

    right.shutdown()
    left.shutdown()
    
    
    

