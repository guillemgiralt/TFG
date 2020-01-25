
import time
from SunFounder_PCA9685 import Servo

class RobotHead:
    """
    This class implements the robot head methods.
    """

    def __init__ (self):
        """
        Initialize and instantiate the servo motors for the head.
        """
        self._initialized = False
        self._lrneck      = Servo.Servo(4)
        self._udneck      = Servo.Servo(3)
        self._righteye    = Servo.Servo(6)
        self._lefteye     = Servo.Servo(5)
        return

    def initialize(self):
        """
        Initialize the head, move the motors to its initial state.
        """
        if not self._initialized:
            self._initialized = True
            self._lrneck.setup()
            self._udneck.setup()
            self._lefteye.setup()
            self._righteye.setup()
        return
    
    def left_eye_up(self):
        self._lefteye.write(40)
        return

    def left_eye_down(self):
        self._lefteye.write(80)
        return
 
    def right_eye_up(self):
        self._righteye.write(140)
        return

    def right_eye_down(self):
        self._righteye.write(110)
        return
 
    def left(self):
        self._lrneck.write(180)
        return

    def right(self):
        self._lrneck.write(0)
        return

    def up(self):
        self._udneck.write(180)
        return

    def down(self):
        self._udneck.write(100)
        return


if __name__ == "__main__":
    robothead = RobotHead()
    robothead.initialize()
    robothead.left_eye_up()
    robothead.left_eye_down()
    robothead.right_eye_up()
    robothead.right_eye_down()
    robothead.up()
    robothead.down()
    robothead.left()
    robothead.right()

    
    

