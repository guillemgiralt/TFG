
import time
import threading
import logging
from robotservo import RobotServo

class RobotBody:
    """
    This class implements the robot body methods.
    """

    def __init__ (self, globalLock):
        """
        Initialize and instantiate the servo motors for the body.
        """
        self._initialized = False
        self._neck        = RobotServo(2, 90, 180, globalLock)
        self._leftArm     = RobotServo(1,100,   0, globalLock)
        self._rightArm    = RobotServo(0,  0, 100, globalLock)
        return

    def initialize(self):
        """
        Initialize the body, move the motors to its initial state.
        """
        if not self._initialized:
            self._neck.initialize ()
            self._leftArm.initialize ()
            self._rightArm.initialize()
            
            self._neck.move (0.0)
            self._leftArm.move (0.0)
            self._rightArm.move (0)
            
            self._neck.wait()
            self._leftArm.wait()
            self._rightArm.wait()
            
            self._initialized = True
        return
    
    def left_arm_move(self, position):
        self._leftArm.move (position, 0.75,30)
        return
    
    def right_arm_move(self, position):
        self._rightArm.move (position, 0.75,30)
        return

    def neck_move(self, position):
        self._neck.move (position, 0.75,30)
        return
    
    def shutdown(self):
        if self._initialized:
            self._neck.shutdown()
            self._leftArm.shutdown()
            self._rightArm.shutdown()
            self._initialized = False
        return


if __name__ == "__main__":
    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    
    globalLock = threading.Lock()
    
    robotbody = RobotBody(globalLock)
    robotbody.initialize()
    
    time.sleep(3)
    
    robotbody.right_arm_move(1.0)
    robotbody.left_arm_move(1.0)
    robotbody.neck_move(1.0)
    
    time.sleep(3)
    
    robotbody.right_arm_move(0.0)
    robotbody.left_arm_move(0.0)
    robotbody.neck_move(0.0)
    
    time.sleep(3)
    
    robotbody.shutdown()

