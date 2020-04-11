
import time
import threading
import logging
from robotservo import RobotServo

## Aquest clase encapsula els moviments del cap del robot.
#  El cap del robot inclou els seguents elements.
#
#  - ull dret : que es moura amunt (posicio 1.0) i avall (posicio 0.0).
#  - ull esquerra :  que es moura amunt (posicio 1.0) i avall (posicio 0.0).
#  - neckUD :  que es moura cap amunt (posicio 1.0) i avall (posicio 0.0).
#  - neckLR :  que es moura cap amunt (posicio 1.0) i avall (posicio 0.0).
#
class RobotHead:

    # Instancia tots els motors del cap del robot.
    # @param[in] globalLock el mecanisme de global sincronització que limita l'accés al recurs compartit de la placa.
    #
    def __init__ (self, globalLock):
        self._initialized = False
        self._globalLock  = globalLock
        self._leftEye     = RobotServo(5, 75, 50, globalLock)
        self._rightEye    = RobotServo(6,120,150, globalLock)
        self._neckUD      = RobotServo(3,90,130, globalLock)
        self._neckLR      = RobotServo(4,0,180, globalLock)
        return

    ## Inicialitza el cap del robot i mou els seus elements a la posicio inicial.
    #
    def initialize(self):
        if not self._initialized:
            
            self._leftEye.initialize()
            self._rightEye.initialize()
            self._neckUD.initialize()
            self._neckLR.initialize()
            
            self._leftEye.move (0.0)
            self._rightEye.move (0.0)
            self._neckUD.move (0.0, 0.75, 30)
            self._neckLR.move (0.5, 0.5 , 30)
            
            self._leftEye.wait()
            self._rightEye.wait()
            self._neckUD.wait()
            self._neckLR.wait()
            
            self._initialized = True
        return
    
    ## Mou l'ull esquerra  amunt i avall.
    #
    # @param[in] position la posicio final del ull en el rang [0.0,1.0]. El valor 0.0 indica moure l'ull a la posicio inferior i el valor 1.0 la posicio superior.
    # @param[in] speed la velocitar del moviment en unitats per segon. El valor de defecte 0.0 indica que cal fer el moviment a velocitat maxima.
    # @param[in] steps el nombre de passos per tal de fer el moviments (per defecte 10).
    #
    def left_eye_move(self, position, speed=0.0, steps=10):
        self._leftEye.move(position, speed, steps)
        return

    ## Mou l'ull dret  amunt i avall.
    #
    # @param[in] position la posicio final del ull en el rang [0.0,1.0]. El valor 0.0 indica moure l'ull a la posicio inferior i el valor 1.0 la posicio superior.
    # @param[in] speed la velocitar del moviment en unitats per segon. El valor de defecte 0.0 indica que cal fer el moviment a velocitat maxima.
    # @param[in] steps el nombre de passos per tal de fer el moviments (per defecte 10).
    #
    def right_eye_move(self, position, speed=0.0, steps=10):
        self._rightEye.move(position, speed, steps)
        return
    
    ## Mou el cap amunt i avall.
    #
    # @param[in] position la posicio final del cap en el rang [0.0,1.0]. El valor 0.0 indica moure el cap a la posicio inferior i el valor 1.0 la posicio superior.
    # @param[in] speed la velocitar del moviment en unitats per segon. El valor de defecte 0.0 indica que cal fer el moviment a velocitat maxima.
    # @param[in] steps el nombre de passos per tal de fer el moviments (per defecte 10).
    #
    def neck_UD_move(self, position, speed=0.0, steps=10):
        self._neckUD.move(position, speed, steps)
        return

    ## Mou el cap esquerra i dreta.
    #
    # @param[in] position la posicio final del cap en el rang [0.0,1.0]. El valor 0.0 indica moure el cap cap a l'esquerra i el valor 1.0 cap a la dreta.
    # @param[in] speed la velocitar del moviment en unitats per segon. El valor de defecte 0.0 indica que cal fer el moviment a velocitat maxima.
    # @param[in] steps el nombre de passos per tal de fer el moviments (per defecte 10).
    #
    def neck_LR_move(self,  position, speed=0.0, steps=10):
        self._neckLR.move(position, speed, steps)
        return
    
    ## Posa el cap del robot la seva posicio initial i atura tots els fils d'execucio del seus elements.
    #
    def shutdown(self):
        if self._initialized:
            
            self._leftEye.move (1.0)
            self._rightEye.move (1.0)
            self._neckUD.move (0.0, 0.75, 30)
            self._neckLR.move (0.5, 0.5 , 30)
            
            self._leftEye.wait()
            self._rightEye.wait()
            self._neckUD.wait()
            self._neckLR.wait()
            
            self._leftEye.shutdown()
            self._rightEye.shutdown()
            self._neckUD.shutdown()
            self._neckLR.shutdown()
            
            self._initialized = False
        return
    
if __name__ == "__main__":

    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    
    globalLock = threading.Lock()
    
    robothead = RobotHead(globalLock)
    robothead.initialize()
    
    robothead.right_eye_move(1.0)
    robothead.left_eye_move(1.0)
    robothead.neck_UD_move(1.0)
    robothead.neck_LR_move(1.0)
    time.sleep(3)
    
    robothead.right_eye_move(0.0)
    robothead.left_eye_move(0.0)
    robothead.neck_UD_move(0.0)
    robothead.neck_LR_move(0.0)
    time.sleep(3)
    
    robothead.shutdown()


    
    

