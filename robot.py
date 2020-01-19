
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
    
    globalLock = threading.Lock()
    
    right = RobotServo(0,0,100, globalLock, logging)
    right.initialize(0.0)

    left = RobotServo(1,100,0,globalLock, logging)
    left.initialize(0.0)

    right.move(1.0)
    left.move(0.0)
    right.wait()
    left.wait()
    
    right.move(0.0, 0.25)
    left.move(1.0, 0.25)
    
    time.sleep(1.0)
    right.stop()
    left.stop()
    
    right.move(1.0, 0.25)
    left.move(0.0, 0.25)
    
    right.wait()
    left.wait()

    right.shutdown()
    left.shutdown()
    
    
    

