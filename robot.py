
import time
import threading

from robothead  import RobotHead
from robotbody  import RobotBody

## Aquest clase encapsula el robot. El robot inclou 2 elements:
#
#  - body : que conte els motors dels 2 braços i el coll.
#  - head : que conte els motors del ulls i el moviment del cap.
#
class Robot:

    ## Instancia tots els elemets del robot i el mecanisme de global sincronització que limita l'accés al recurs compartit de la placa.
    # @param[in] name el nom del robot.
    #
    def __init__ (self, name):
        self._initialized = False
        self._name        = name
        self._globalLock  = threading.Lock()

        # Create the head and the body.
        #
        self._head = RobotHead(self._globalLock)
        self._body = RobotBody(self._globalLock)

        return

    ## Inicialitza el robot i mou els seus elements a la posicio inicial.
    #
    def initialize(self):
        if not self._initialized:
            self._initialized = True
            self._head.initialize()
            self._body.initialize ()
        return
    
    ## Obte el nom del robot assignat durant la creacio.
    # @return el nom del robot assignat durant la creacio.
    #
    def name(self):
        return self._name
    
    ## Obte l'objecte que permet operar amb el cap del robot.
    # @return el cap del robot.
    #
    def head(self):
        return self._head
    
    ## Obte l'objecte que permet operar amb el cos del robot.
    # @return el cap del robot.
    #
    def body(self):
        return self._body
    
    ## Posa el robot la seva posicio initial i atura tots els fils d'execucio del seus elements.
    #
    def shutdown(self):
        """
        Shutdown the robot.
        """
        if self._initialized:
            self._body.shutdown()
            self._head.shutdown()
            self._initialized = False
        return


