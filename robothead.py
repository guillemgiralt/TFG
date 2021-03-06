
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
        self._leftEye     = RobotServo(5, 75, 50, globalLock)
        self._rightEye    = RobotServo(6,120,150, globalLock)
        self._neckUD      = RobotServo(3,90,130, globalLock)
        self._neckLR      = RobotServo(4,0,180, globalLock)
        return

    def initialize(self):
        """
        Initialize the head, move the motors to its initial state.
        """
        if not self._initialized:
            
            self._leftEye.initialize()
            self._rightEye.initialize()
            self._neckUD.initialize()
            self._neckLR.initialize()
            
            self._leftEye.move (0.0)
            self._rightEye.move (0.0)
            self._neckUD.move (0.0, 0.75, 30)
            self._neckLR.move (0.5, 0.5 , 30)
            
            self._leftEye.wait()
            self._rightEye.wait()
            self._neckUD.wait()
            self._neckLR.wait()
            
            self._initialized = True
        return
    
    def left_eye_move(self, position, speed=0.0, steps=10):
        self._leftEye.move(position, speed, steps)
        return
    

    def right_eye_move(self, position, speed=0.0, steps=10):
        self._rightEye.move(position, speed, steps)
        return
    
    def neck_UD_move(self, position, speed=0.0, steps=10):
        self._neckUD.move(position, speed, steps)
        return

    def neck_LR_move(self,  position, speed=0.0, steps=10):
        self._neckLR.move(position, speed, steps)
        return
    
    def shutdown(self):
        if self._initialized:
            
            self._leftEye.move (1.0)
            self._rightEye.move (1.0)
            self._neckUD.move (0.0, 0.75, 30)
            self._neckLR.move (0.5, 0.5 , 30)
            
            self._leftEye.wait()
            self._rightEye.wait()
            self._neckUD.wait()
            self._neckLR.wait()
            
            self._leftEye.shutdown()
            self._rightEye.shutdown()
            self._neckUD.shutdown()
            self._neckLR.shutdown()
            
            self._initialized = False
        return
    
if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    
    globalLock = threading.Lock()
    
    robothead = RobotHead(globalLock)
    robothead.initialize()
    
    robothead.right_eye_move(1.0)
    robothead.left_eye_move(1.0)
    robothead.neck_UD_move(1.0)
    robothead.neck_LR_move(1.0)
    time.sleep(3)
    
    robothead.right_eye_move(0.0)
    robothead.left_eye_move(0.0)
    robothead.neck_UD_move(0.0)
    robothead.neck_LR_move(0.0)
    time.sleep(3)
    
    robothead.shutdown()


    
    

