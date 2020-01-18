
import time
import threading
from SunFounder_PCA9685 import Servo

class RobotServo(threading.Thread):
    """
    This class implements the robot servo methods.
    """

    def __init__ (self, servoId, zeroAngle, oneAngle, logging):
        """
        Initialize and instantiate the servo motors.
        """
        threading.Thread.__init__(self)
        self._servoId   = servoId
        self._servo     = Servo.Servo(servoId)
        self._zeroAngle = zeroAngle
        self._oneAngle  = oneAngle
        self._cvmove    = threading.Condition()
        self._cvstop    = threading.Condition()
        self._operate   = False
        self._stop      = False
        self._target    = 0.0
        self._speed     = 0.0
        self._steps     = 0
        self._logging   = logging
        self._shutdown  = False
        self._position  = 0.0
        self._initial   = 0.0
        return

    def initialize(self, position):
        """
        Initialize the motor, move the motors to its initial state.
        """
        self._servo.setup()
        self._servo.write(self.to_angle(position))
        self._position = position
        self.start()
        return
    
    def shutdown(self):
        """
        Shutdown the motor, stop the thread..
        """
        self._logging.debug ("shutdown({}).".format(self._servoId))
        self._cvmove.acquire()
        
        # wait for pending operations.
        #
        while self._operate:
            self._cvmove.wait()

        # set the shutdown flag and wakeup the servo thread.
        #
        self._shutdown = True
        self._operate  = True
        self._cvmove.notify()
        
        self._cvmove.release()
        self._logging.debug ("shutdown({}): done.".format(self._servoId))

        return
    
    def position(self):
        return self._position

    def to_angle(self, position):
        angle = (self._oneAngle - self._zeroAngle) * position + self._zeroAngle
        return (int)(angle)

    def move(self, position, speed=0.0, steps=10):
        """
        Move the motor to a given position with a given speed.
        """
        self._logging.debug ("move({}): position={} speed={} steps={}.".format(self._servoId, position, speed, steps))
        self._cvmove.acquire()
        
        # wait for pending operations.
        #
        while self._operate:
            self._cvmove.wait()

        # set the target position and wakeup the servo thread.
        #
        self._operate = True
        self._target  = position
        self._speed   = speed
        self._steps   = steps
        self._cvmove.notify()
        
        self._cvmove.release()
        self._logging.debug ("move({}): done.".format(self._servoId))
        return

    def wait(self):
        """
        Wait until a pending move is completed.
        """
        self._logging.debug ("wait({}): start.".format(self._servoId))
        self._cvmove.acquire()
        
        # wait until the thread has completed.
        #
        while self._operate:
            self._cvmove.wait()
            
        self._cvmove.release()
        self._logging.debug ("wait({}): done.".format(self._servoId))
        return

    def stop(self):
        self._stop = True
        return

    def run(self):
        """
        Move thread entry point.
        """
        self._logging.debug ("run({}): starting.".format(self._servoId))
        while not self._shutdown:
            
            self._logging.debug ("run({}): waiting movement.".format(self._servoId))
            
            # wait until a movement is requested.
            #
            self._cvmove.acquire()
            while not self._operate:
                self._cvmove.wait()
            self._cvmove.release()
            
            if not self._shutdown:
                # perform the movement.
                #
                self._logging.debug ("run({}): target={}, speed={}, steps={})".format(self._servoId, self._target, self._speed ,self._steps))
                if (self._speed == 0.0):
                    # direct move.
                    #
                    self._servo.write(self.to_angle(self._target))
                    self._position = self._target
                else:
                    # compute the travel distance and the delay to use.
                    #
                    distance = abs(self._target - self._position)
                    increment = distance / self._steps
                    delay     = (distance / self._speed) / self._steps

                    # start moving...
                    #
                    current = self._position + increment
                    self._stop = False
                    while ((not self._stop) and (current < self._target)):
                        self._servo.write(self.to_angle(current))
                        time.sleep (delay)
                        current = current + increment

                    # movement done, store the position.
                    #
                    if self._stop:
                        self._position = current
                    else:
                        self._servo.write(self.to_angle(self._target))
                        self._position = self._target
                        
                self._logging.debug ("run({}): done.".format(self._servoId))
            
                # we are not operate anymore and wakeup people waiting
                #
                self._cvmove.acquire()
                self._operate = False
                self._cvmove.notify()
                self._cvmove.release()
            
        self._logging.debug ("run({}): finished.".format(self._servoId))
        self._servo.write(self.to_angle(self._initial))

        return
