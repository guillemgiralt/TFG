
import time
import threading

from SunFounder_PCA9685 import Servo

from robothead import RobotHead
from robotbody import RobotBody
from robotservo import RobotServo

class Robot:
    """
    This class implements the robot methods.
    """

    def __init__ (self, name):
        """
        Initialize and instantiate the servo motors for the body.
        """
        self._initialized = False
        
        self._name = name
        
        self._globalLock = threading.Lock()
        
        self._head = RobotHead()
        self._body = RobotBody(self._globalLock)

        return

    def initialize(self):
        """
        Initialize the body, move the motors to its initial state.
        """
        if not self._initialized:
            self._initialized = True
            #self._head.initialize()
            self._body.initialize ()
        return
    
    def name(self):
        return self._name
    
    def head(self):
        return self._head
    
    def body(self):
        return self._body
    
    def shutdown(self):
        self._body.shutdown()
        return


