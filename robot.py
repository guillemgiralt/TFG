
from robothead import RobotHead
from robotbody import RobotBody
from robotservo import RobotServo
import threading
import time
import logging

def my_move(z):
    logging.info("thread start")
    z.move(1.0, 0.1)
    logging.info("thread finish")
    logging.info("position={}".format(z.position()))
    return

if __name__ == "__main__":
    #robothead = RobotHead()
    #robotbody = RobotBody(robothead)
    #robotbody.initialize()

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    
    z = RobotServo(0,0,100)
    z.initialize(0.5)

    z.move(0.0)
    t = threading.Thread(target=my_move, args=(z,)) 
    logging.info("main start")
    t.start()
    logging.info("main started")
    time.sleep(5.0)
    logging.info("main stopping")
    #z.stop()
    logging.info("main stoped")
    print(z.position())
    
    

