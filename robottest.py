
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
    
    right = RobotServo(0,0,100, globalLock)
    right.initialize(0.0)

    left = RobotServo(1,100,0,globalLock)
    left.initialize(0.0)

    neck = RobotServo(2, 110, 180, globalLock)
    neck.initialize(0.0)

    neckBodyUD = RobotServo(3,120, 95, globalLock)
    neckBodyUD.initialize(0.0)

    neckBodyLR = RobotServo(4,0,180, globalLock)
    neckBodyLR.initialize(0.0)

    leftEye    = RobotServo(5, 65, 50, globalLock)
    leftEye.initialize(0.0)

    rightEye   = RobotServo(6,110,140, globalLock)
    rightEye.initialize(0.0)

    
    right.move(0.0)
    left.move(0.0)
    neck.move(0.0)
    neckBodyUD.move(0.0)
    neckBodyLR.move(0.0)
    leftEye.move(1.0)
    rightEye.move(1.0)
    right.wait()
    left.wait()
    neck.wait()
    neckBodyUD.wait()
    neckBodyLR.wait()
    leftEye.wait()
    rightEye.wait()

    
    for i in range(3):
        right.move(1.0, 0.75,100)
        left.move(1.0, 0.75, 100)
        neck.move(1.0, 0.75, 100)
        neckBodyUD.move(1.0, 0.75, 100)
        neckBodyLR.move(1.0, 0.75, 100)
        leftEye.move(0.0, 1, 100)
        rightEye.move(0.0, 1, 100)
        right.wait()
        left.wait()
        neck.wait()
        neckBodyUD.wait()
        neckBodyLR.wait()
        leftEye.wait()
        rightEye.wait()
        
        right.move(0.0, 0.75, 100)
        left.move(0.0, 0.75, 100)
        neck.move(0.0, 0.75, 100)
        neckBodyUD.move(0.0, 0.75, 100)
        neckBodyLR.move(0.0, 0.75, 100)
        leftEye.move(1.0, 1, 100)
        rightEye.move(1.0, 1,100)
        right.wait()
        left.wait()
        neck.wait()
        neckBodyUD.wait()
        neckBodyLR.wait()
        leftEye.wait()
        rightEye.wait()
    

    right.shutdown()
    left.shutdown()
    neck.shutdown()
    neckBodyUD.shutdown()
    neckBodyLR.shutdown()
    leftEye.shutdown()
    rightEye.shutdown()
    
    

