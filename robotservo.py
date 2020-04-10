
import time
import logging
import threading
from SunFounder_PCA9685 import Servo

## Aquest clase encapsula els moviments de baix nivell del motor
#  en una interficie mes simple. Permet convertir el moviments
#  d'angle a un valor de coma floatant en un rang [0.0, 1.0]
#
class RobotServo(threading.Thread):
    
    ## Crea la instancia del motor.
    #
    # @param[in] servoId el identificador del servo.
    # @param[in] zeroAngle el angle del motor que correspondra a la posicio 0.0
    # @param[in] oneAngle el angle del motor que correspondra a la posico 1.0
    # @param[in] globalLock el mecanisme de global sincronització que limita l'accés al recurs compartit de la placa.
    #
    def __init__ (self, servoId, zeroAngle, oneAngle, globalLock):
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

    ## Inicialitza el motor, arrenca el fil d'execucio i el mou a la seva position inicial.
    #
    def initialize(self):
        self._globalLock.acquire()
        self._servo.setup()
        self._globalLock.release()
        self._position = -1.0
        self.start()
        return
    
    ## Para el motor i tanca el fil d'execution.
    #
    def shutdown(self):
        logging.debug ("shutdown({}).".format(self._servoId))
        self._cvmove.acquire()
        
        # espera que acabin les operacions pendents.
        #
        while self._operate:
            self._cvmove.wait()

        # posem la senyal de parada i despertem el fil d'execucio.
        #
        self._shutdown = True
        self._operate  = True
        self._cvmove.notify()
        
        self._cvmove.release()
        logging.debug ("shutdown({}): done.".format(self._servoId))

        return
    
    ## Obte la posicio actual del motor.
    #
    # @return la posicio actual del motor en el rang de [0.0, 1.0]
    #
    def position(self):
        self._cvmove.acquire()
        position = self._position
        self._cvmove.release()
        return position

    ## Mou el motor a una posisio donada amb una velocitat i/o un nombre de passos donats.
    #
    # @param[in] position la posicio final del motor en el rang [0.0,1.0]
    # @param[in] speed la velocitar del moviment en unitats per segon. El valor de defecte 0.0 indica que cal fer el moviment a velocitat maxima.
    # @param[in] steps el nombre de passos per tal de fer el moviments (per defecte 10).
    #
    def move(self, position, speed=0.0, steps=10):
        logging.debug ("move({}): position={} speed={} steps={}.".format(self._servoId, position, speed, steps))
        self._cvmove.acquire()
        
        # esperem que acabin les operacions pendent.
        #
        while self._operate:
            self._cvmove.wait()

        if speed == 0.0:
            # moviment directe, podem fer-ho en el mateix fil de qui ens crida.
            #
            self._globalLock.acquire()
            self._servo.write(self._to_angle(position))
            self._globalLock.release()
            self._position = position
        else:
            # fixem la posicio final, velocitat i nombre de passos i despertem el fil d'execucio.
            #
            self._target  = position
            self._speed   = speed
            self._steps   = steps
            self._operate = True
            self._cvmove.notify()
        
        self._cvmove.release()
        logging.debug ("move({}): done.".format(self._servoId))
        return

    ## Espera que acabi el moviment pendent.
    #
    def wait(self):
        logging.debug ("wait({}): start.".format(self._servoId))
        self._cvmove.acquire()
        
        # esperem a que acabi el moviment.
        #
        while self._operate:
            self._cvmove.wait()
            
        self._cvmove.release()
        logging.debug ("wait({}): done.".format(self._servoId))
        return

    ## Atura el moviment actual si n'hi ha.
    #
    def stop(self):
        logging.debug ("stop{}): start.".format(self._servoId))
        self._cvmove.acquire()
        
        # aturem el moviment.
        #
        self._cvstop.acquire()
        self._stop = True
        self._cvstop.notify()
        self._cvstop.release()
        
        # esperem a que acabi.
        #
        while self._operate:
            self._cvmove.wait()
            
        self._cvmove.release()
        logging.debug ("stop({}): done.".format(self._servoId))
        return

    ## Funcio privada que converteix una posicio entre [0.0, 1.0] al angle del motor a fer servir.
    #
    # @param[in] position la posicio entre [0.0, 1.0].
    # @return el angle del motor que correspon la posicio donada,
    #
    def _to_angle(self, position):
        angle = (self._oneAngle - self._zeroAngle) * position + self._zeroAngle
        return (int)(angle)

    ## Punt d'entrada del fil execution del motor.
    #
    def run(self):
        logging.debug ("run({}): starting.".format(self._servoId))

        # mentre no arribi el shutdown esperarem un moviment.
        #
        while not self._shutdown:
            
            logging.debug ("run({}): waiting movement.".format(self._servoId))
            
            # esperem a que es demani algun moviment o arribi un shutdown.
            #
            self._cvmove.acquire()
            while not self._operate:
                self._cvmove.wait()
            self._cvmove.release()
            
            if not self._shutdown:
                # hem rebut un moviment.
                #
                logging.debug ("run({}): target={}, speed={}, steps={})".format(self._servoId, self._target, self._speed ,self._steps))
                
                # calculem el increment per cada pas i el seu retard.
                #
                increment = (self._target - self._position) / self._steps
                delay     = (abs(self._target - self._position) / self._speed) / self._steps

                # comencem a moure i ho repetim tantes vegades com calgui o ens aturin.
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

                # moviment acabat, emmagatzamem la posicio final.
                #
                if self._stop:
                    logging.debug ("run({}): stopped at current={})".format(self._servoId, current))
                    self._position = current
                else:
                    logging.debug ("run({}): completed at current={})".format(self._servoId, self._target))
                    self._position = self._target
                self._cvmove.release()
                        
                logging.debug ("run({}): done.".format(self._servoId))
            
                # no hem de fer res-mes, despertem a qui estigui adormit esperant el seu torn.
                #
                self._cvmove.acquire()
                self._operate = False
                self._cvmove.notify()
                self._cvmove.release()
            
        logging.debug ("run({}): finished.".format(self._servoId))
        self._servo.write(self._to_angle(self._initial))

        return
