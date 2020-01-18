
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
        self._lrneck      = Servo.Servo(0)
        self._udneck      = Servo.Servo(0)
        self._righteye    = Servo.Servo(0)
        self._lefteye     = Servo.Servo(0)
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
        self._lefteye.write(0)
        return

    def left_eye_down(self):
        self._lefteye.write(30)
        return
 
    def right_eye_up(self):
        self._righteye.write(60)
        return

    def right_eye_down(self):
        self._righteye.write(90)
        return
 
    def left(self):
        self._lrneck.write(120)
        return

    def right(self):
        self._lrneck.write(150)
        return

    def up(self):
        self._udneck.write(180)
        return

    def down(self):
        self._udneck.write(0)
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

    
    

