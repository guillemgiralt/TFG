
import time
import threading
import logging
from robotservo import RobotServo

## Aquest clase encapsula els moviments del cos del robot.
#  El cos del robot inclou els seguents motors.
#
#  - leftArm : controla el braç esquerra que es moura amunt (posicio 1.0) i avall (posicio 0.0).
#  - rightArm : controla el braç dret es moura amunt (posicio 1.0) i avall (posicio 0.0).
#  - neck :  que controlla el moviment del cap del robot que es moura cap amunt (posicio 1.0) i a una posicio horitzontal (posicio 0.0).
#
class RobotBody:

    ## Instancia tots els motors del cos del robot.
    # @param[in] globalLock el mecanisme de global sincronització que limita l'accés al recurs compartit de la placa.
    #
    def __init__ (self, globalLock):
        self._initialized = False                               
        self._neck        = RobotServo(2, 90, 180, globalLock) 
        self._leftArm     = RobotServo(1,100,   0, globalLock)
        self._rightArm    = RobotServo(0,  0, 100, globalLock)
        return

    ## Inicialitza el cos del robot i mou els seus elements a la posicio inicial.
    #
    def initialize(self):
        if not self._initialized:
            self._neck.initialize ()
            self._leftArm.initialize ()
            self._rightArm.initialize()
            
            self._neck.move     (0.0, 1.0, 10)
            self._leftArm.move  (0.0, 1.0, 10)
            self._rightArm.move (0.0, 1.0, 10)
            
            self._neck.wait()
            self._leftArm.wait()
            self._rightArm.wait()
            
            self._initialized = True
        return
    
    ## Mou el braç esquerra amunt i avall.
    #
    # @param[in] position la posicio final del braç en el rang [0.0,1.0]. El valor 0.0 indica moure el braç a la posicio inferior i el valor 1.0 la posicio superior.
    # @param[in] speed la velocitar del moviment en unitats per segon. El valor de defecte 0.0 indica que cal fer el moviment a velocitat maxima.
    # @param[in] steps el nombre de passos per tal de fer el moviments (per defecte 10).
    #
    def left_arm_move(self, position, speed=0.0, steps=10):
        self._leftArm.move (position, speed, steps)
        return
    
    ## Mou el braç dret amunt i avall.
    #
    # @param[in] position la posicio final del braç en el rang [0.0,1.0]. El valor 0.0 indica moure el braç a la posicio inferior i el valor 1.0 a la posicio superior.
    # @param[in] speed la velocitar del moviment en unitats per segon. El valor de defecte 0.0 indica que cal fer el moviment a velocitat maxima.
    # @param[in] steps el nombre de passos per tal de fer el moviments (per defecte 10).
    #
    def right_arm_move(self, position, speed=0.0, steps=10):
        self._rightArm.move (position, speed, steps)
        return

    ## Mou el coll amunt i avall.
    #
    # @param[in] position la posicio final del coll en el rang [0.0,1.0]. El valor 0.0 indica moure el coll a la posicio inferior i el valor 1.0 a la posicio superior.
    # @param[in] speed la velocitar del moviment en unitats per segon. El valor de defecte 0.0 indica que cal fer el moviment a velocitat maxima.
    # @param[in] steps el nombre de passos per tal de fer el moviments (per defecte 10).
    #
    def neck_move(self, position, speed=0.0, steps=10):
        self._neck.move (position, speed, steps)
        return
    
    ## Posa el cos del robot la seva posicio initial i atura tots els fils d'execucio del seus elements.
    #
    def shutdown(self):
        if self._initialized:
            
            self._neck.move     (0.0, 1.0, 10)
            self._leftArm.move  (0.0, 1.0, 10)
            self._rightArm.move (0.0, 1.0, 10)
            
            self._neck.wait()
            self._leftArm.wait()
            self._rightArm.wait()
            
            self._neck.shutdown()
            self._leftArm.shutdown()
            self._rightArm.shutdown()
            
            self._initialized = False
        return


if __name__ == "__main__":
    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    
    globalLock = threading.Lock()
    
    robotbody = RobotBody(globalLock)
    robotbody.initialize()
    
    time.sleep(3)
    
    robotbody.right_arm_move(1.0)
    robotbody.left_arm_move(1.0)
    robotbody.neck_move(1.0)
    
    time.sleep(3)
    
    robotbody.right_arm_move(0.0)
    robotbody.left_arm_move(0.0)
    robotbody.neck_move(0.0)
    
    time.sleep(3)
    
    robotbody.shutdown()

