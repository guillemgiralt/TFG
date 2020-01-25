
import time
import threading
import logging
from robotservo import RobotServo

class RobotHead:
    """
    This class implements the robot head methods.
    """

    def __init__ (self, globalLock):
        """
        Initialize and instantiate the servo motors for the head.
        """
        self._initialized = False
        self._globalLock  = globalLock
        self._leftEye     = RobotServo(5, 65, 50, globalLock)
        self._rightEye    = RobotServo(6,110,140, globalLock)
        return

    def initialize(self):
        """
        Initialize the head, move the motors to its initial state.
        """
        if not self._initialized:
            self._initialized = True
            self._leftEye.initialize()
            self._rightEye.initialize()
        return
    
    def left_eye_move(self, position):
        self._leftEye.move(position, 1.0, 100)
        self._leftEye.wait()
        return

    def right_eye_move(self, position):
        self._rightEye.move(position, 1.0, 100)
        self._rightEye.wait()
        return


    def shutdown(self):
        self._leftEye.shutdown()
        self._rightEye.shutdown()
        return
    
if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    
    globalLock = threading.Lock()
    
    robothead = RobotHead(globalLock)
    robothead.initialize()
    
    robothead.right_eye_move(1.0)
    robothead.left_eye_move(1.0)
    
    time.sleep(3)
    
    robothead.right_eye_move(0.0)
    robothead.left_eye_move(0.0)
    
    time.sleep(3)
    
    robothead.shutdown()


    
    

