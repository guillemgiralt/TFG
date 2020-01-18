
import time
from SunFounder_PCA9685 import Servo

class RobotServo:
    """
    This class implements the robot servo methods.
    """

    def __init__ (self, servoId, zeroAngle, oneAngle):
        """
        Initialize and instantiate the servo motors for the body.
        """
        self._servo     = Servo.Servo(servoId)
        self._zeroAngle = zeroAngle
        self._oneAngle  = oneAngle
        self._stop      = False
        return

    def initialize(self, position):
        """
        Initialize the body, move the motors to its initial state.
        """
        self._servo.setup()
        self.move (position)
        self._position = position
        return
    
    def position(self):
        return self._position

    def to_angle(self, position):
        angle = (self._oneAngle - self._zeroAngle) * position + self._zeroAngle
        return (int)(angle)

    def move(self, position, speed=0.0, steps=10):
        """
        Move ...
        """
        if (speed == 0.0):
            # direct move.
            self._servo.write(self.to_angle(position))
            self._position = position
        else:
            # compute the travel distance and the delay to use.
            distance = abs(position - self._position)
            increment = distance / steps
            delay     = (distance / speed) / steps
        
            current = self._position + increment
            self._stop = False
            while ((not self._stop) and (current < position)):
                self._servo.write(self.to_angle(current))
                time.sleep (delay)
                current = current + increment

            # store the position.
            if self._stop:
                self._position = current
            else:
                self._servo.write(self.to_angle(position))
                self._position = position
        return

    def stop(self):
        self._stop = True

    
