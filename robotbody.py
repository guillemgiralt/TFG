
import time
import threading
import logging

from SunFounder_PCA9685 import Servo

from robothead import RobotHead
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
        self._globalLock  = globalLock
        self._neck        = RobotServo(2, 90, 180, globalLock)
        self._leftarm     = RobotServo(1,100,   0, globalLock)
        self._rightarm    = RobotServo(0,  0, 100, globalLock)
        return

    def initialize(self):
        """
        Initialize the body, move the motors to its initial state.
        """
        if not self._initialized:
            self._initialized = True
            self._neck.initialize (0.0)
            self._leftarm.initialize (0.0)
            self._rightarm.initialize(0.0)
        return
    
    def left_arm_up(self):
        self._leftarm.move(1.0)
        self._leftarm.wait()
        return

    def left_arm_down(self):
        self._leftarm.move(0.0)
        self._leftarm.wait()
        return
    
    def left_arm_move(self, position):
        self._leftarm.move(position)
        self._leftarm.wait()
        return
    
    def right_arm_up(self):
        self._rightarm.move(1.0)
        self._rightarm.wait()
        return

    def right_arm_down(self):
        self._rightarm.move(0.0)
        self._rightarm.wait()
        return

    def right_arm_move(self, position):
        self._rightarm.move(position)
        self._rightarm.wait()
        return

    def neck_up(self):
        self._neck.move(1.0)
        self._neck.wait()
        return

    def neck_down(self):
        self._neck.move(0.0)
        self._neck.wait()
        return
    
    def neck_move(self, position):
        self._neck.move(position)
        self._neck.wait()
        return
    
    def shutdown(self):
        self._neck.shutdown()
        self._leftarm.shutdown()
        self._rightarm.shutdown()
        return


if __name__ == "__main__":
    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    
    globalLock = threading.Lock()
    
    robotbody = RobotBody(globalLock)
    robotbody.initialize()
    
    robotbody.right_arm_up()
    robotbody.left_arm_up()
    robotbody.neck_up()
    
    time.sleep(5)
    
    robotbody.right_arm_down()
    robotbody.left_arm_down()
    robotbody.neck_down()
    
    robotbody.shutdown()

