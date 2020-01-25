
import time
import logging
import threading
from SunFounder_PCA9685 import Servo

class RobotServo(threading.Thread):
    """
    This class implements the robot servo methods.
    """

    def __init__ (self, servoId, zeroAngle, oneAngle, globalLock):
        """
        Initialize the robot servo instance

        Parameters
        ----------
        servoId : int
            The identifier of the motor servo.
        zeroAngle : float
            The motor angle that corresponds to the position 0.0
        oneAngle : float
            The motor angle that corresponds to the position 1.0
        globalLock : 
            The global thread lock to be used when writing the servo commands.

        """
        threading.Thread.__init__(self)
        self._servoId    = servoId
        self._servo      = Servo.Servo(servoId)
        self._zeroAngle  = zeroAngle
        self._oneAngle   = oneAngle
        self._globalLock = globalLock
        self._cvmove     = threading.Condition()
        self._cvstop     = threading.Condition()
        self._operate    = False
        self._stop       = False
        self._target     = 0.0
        self._speed      = 0.0
        self._steps      = 0
        self._shutdown   = False
        self._position   = 0.0
        self._initial    = 0.0
        return

    def initialize(self, position):
        """
        Initialize the motor, move the motors to its initial state.

        Parameters
        ----------
        position : float
            The initial servo position.

        """
        self._globalLock.acquire()
        self._servo.setup()
        self._servo.write(self._to_angle(position))
        self._globalLock.release()
        self._position = position
        self.start()
        return
    
    def shutdown(self):
        """
        Shutdown the motor and clean everything.
        """
        logging.debug ("shutdown({}).".format(self._servoId))
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
        logging.debug ("shutdown({}): done.".format(self._servoId))

        return
    
    def position(self):
        """
        Initialize the motor, move the motors to its initial state.

        Returns
        -------
        float
            The current position.
        """
        self._cvmove.acquire()
        position = self._position
        self._cvmove.release()
        return position

    def move(self, position, speed=0.0, steps=10):
        """
        Start moving the motor to a given position with a given speed/steps.

        Parameters
        ----------
        position : float
            The final servo position.
        speed : float, optional
            The movement speed in units per second. A value 0.0 (default) indicates to perform a direct move without any step.
        steps : int, optional
            The number of steps to perform (default is 10).

        """
        logging.debug ("move({}): position={} speed={} steps={}.".format(self._servoId, position, speed, steps))
        self._cvmove.acquire()
        
        # wait for pending operations.
        #
        while self._operate:
            self._cvmove.wait()

        # set the target position and wakeup the servo thread.
        #
        self._target  = position
        self._speed   = speed
        self._steps   = steps
        self._operate = True
        self._cvmove.notify()
        
        self._cvmove.release()
        logging.debug ("move({}): done.".format(self._servoId))
        return

    def wait(self):
        """
        Wait until a pending move is completed.
        """
        logging.debug ("wait({}): start.".format(self._servoId))
        self._cvmove.acquire()
        
        # wait until the thread has completed.
        #
        while self._operate:
            self._cvmove.wait()
            
        self._cvmove.release()
        logging.debug ("wait({}): done.".format(self._servoId))
        return

    def stop(self):
        """
        Stop the current movement.
        """
        logging.debug ("stop{}): start.".format(self._servoId))
        self._cvmove.acquire()
        
        # stop the current movement.
        #
        self._cvstop.acquire()
        self._stop = True
        self._cvstop.notify()
        self._cvstop.release()
        
        # wait until the thread has completed.
        #
        while self._operate:
            self._cvmove.wait()
            
        self._cvmove.release()
        logging.debug ("stop({}): done.".format(self._servoId))
        return

    def _to_angle(self, position):
        """
        Converts a position to its motor angle.

        Parameters
        ----------
        position : float
            The servo position to convert.

        Returns
        -------
        int
            The motor angle that corresponds to the given position.
        """
        angle = (self._oneAngle - self._zeroAngle) * position + self._zeroAngle
        return (int)(angle)

    def run(self):
        """
        Move thread entry point.
        """
        logging.debug ("run({}): starting.".format(self._servoId))
        while not self._shutdown:
            
            logging.debug ("run({}): waiting movement.".format(self._servoId))
            
            # wait until a movement is requested.
            #
            self._cvmove.acquire()
            while not self._operate:
                self._cvmove.wait()
            self._cvmove.release()
            
            if not self._shutdown:
                # perform the movement.
                #
                logging.debug ("run({}): target={}, speed={}, steps={})".format(self._servoId, self._target, self._speed ,self._steps))
                if (self._speed == 0.0):
                    # direct move.
                    #
                    self._globalLock.acquire()
                    self._servo.write(self._to_angle(self._target))
                    self._globalLock.release()
                    self._position = self._target
                else:
                    # compute the increment for each step and the delay to use.
                    #
                    increment = (self._target - self._position) / self._steps
                    delay     = (abs(self._target - self._position) / self._speed) / self._steps

                    # start moving...
                    #
                    self._cvmove.acquire()
                    current = self._position + increment
                    self._stop = False
                    while ((not self._stop) and (self._steps > 0)):
                        logging.debug ("run({}): current={})".format(self._servoId, current))
                        self._globalLock.acquire()
                        self._servo.write(self._to_angle(current))
                        self._globalLock.release()
                        current = current + increment
                        self._steps = self._steps - 1
                        self._cvmove.wait(delay)

                    # movement done, store the position.
                    #
                    if self._stop:
                        logging.debug ("run({}): stopped at current={})".format(self._servoId, current))
                        self._position = current
                    else:
                        logging.debug ("run({}): completed at current={})".format(self._servoId, self._target))
                        self._position = self._target
                    self._cvmove.release()
                        
                logging.debug ("run({}): done.".format(self._servoId))
            
                # we are not operate anymore and wakeup people waiting
                #
                self._cvmove.acquire()
                self._operate = False
                self._cvmove.notify()
                self._cvmove.release()
            
        logging.debug ("run({}): finished.".format(self._servoId))
        self._servo.write(self._to_angle(self._initial))

        return
