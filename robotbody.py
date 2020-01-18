
import time
from SunFounder_PCA9685 import Servo

from robothead import RobotHead

class RobotBody:
    """
    This class implements the robot body methods.
    """

    def __init__ (self, head):
        """
        Initialize and instantiate the servo motors for the body.
        """
        self._initialized = False
        self._head        = head
        self._neck        = Servo.Servo(0)
        self._leftarm     = Servo.Servo(0)
        self._rightarm    = Servo.Servo(0)
        return

    def initialize(self):
        """
        Initialize the body, move the motors to its initial state.
        """
        if not self._initialized:
            self._initialized = True
            self._head.initialize()
            self._neck.setup()
            self._leftarm.setup()
            self._rightarm.setup()
        return
    
    def head(self):
        return self._head
    
    def head_up(self):
        self._neck.write(0)
        return

    def head_down(self):
        self._neck.write(180)
        return
 
    def left_arm_up(self):
        self._leftarm.write(0)
        return

    def left_arm_down(self):
        self._leftarm.write(0)
        return
    
    def right_arm_up(self):
        self._rightarm.write(0)
        return

    def right_arm_down(self):
        self._rightarm.write(0)
        return


if __name__ == "__main__":
    robothead = RobotHead()
    robotbody = RobotBody(robothead)
    robotbody.initialize()
    robotbody.right_arm_up()
    robotbody.right_arm_down()
    robotbody.left_arm_up()
    robotbody.left_arm_down()
    robotbody.head_up()
    robotbody.head_down()
    
    robotbody.head().left_eye_up()
    robotbody.head().left_eye_down()
    robotbody.head().right_eye_up()
    robotbody.head().right_eye_down()
    robotbody.head().up()
    robotbody.head().down()
    robotbody.head().left()
    robotbody.head().right()
    

