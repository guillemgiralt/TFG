
import time
import threading

from robothead  import RobotHead
from robotbody  import RobotBody

class Robot:
    """
    This class implements the robot methods.
    """

    def __init__ (self, name):
        """
        Create the robot.

        Parameters
        ----------
        name : string
            The robot nickname.
        """
        self._initialized = False
        self._name        = name
        self._globalLock  = threading.Lock()

        # Create the head and the body.
        #
        self._head = RobotHead(self._globalLock)
        self._body = RobotBody(self._globalLock)

        return

    def initialize(self):
        """
        Initialize the body, move the motors to its initial state.
        """
        if not self._initialized:
            self._initialized = True
            self._head.initialize()
            self._body.initialize ()
        return
    
    def name(self):
        """
        Get the robot nick name.

        Returns
        -------
        string
            The robot nick name.
        """
        return self._name
    
    def head(self):
        """
        Get the robot head.

        Returns
        -------
        object
            The robot head.
        """
        return self._head
    
    def body(self):
        """
        Get the robot body.

        Returns
        -------
        object
            The robot body.
        """
        return self._body
    
    def shutdown(self):
        """
        Shutdown the robot.
        """
        if self._initialized:
            self._body.shutdown()
            self._head.shutdown()
            self._initialized = False
        return


