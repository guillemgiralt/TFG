
import os
import pprint
import pygame
import paho.mqtt.publish as publish
import sys
import logging
import time
import argparse

## Aquest clase encapsula el controllador deel robot a travers d'un comanament de la PS4.
#
#  - El controlador del comanament de la PS4 es fa a travers del paquet de Python @b pygame
#  que permet obtenir els events de moviment i botons del mateix.
#  
#  - El client de MQQT que permet enviar les comanes cap al robot es fa a travers del paquet de Python @b paho
#    que permet publicar events de MQTT tant a brokers locals com remots.
#
class RobotPS4Controller(object):

    ##  el boto amb una creu del comanament de la PS4.
    #
    CROSS_BUTTON    = 0
    
    ##  el boto amb un cercle del comanament de la PS4.
    #
    CIRCLE_BUTTON   = 1
    
    ##  el boto amb un triangle del comanament de la PS4.
    #
    TRIANGLE_BUTTON = 2
    
    ##  el boto amb un cuadrat del comanament de la PS4.
    #
    SQUARE_BUTTON   = 3

    ##  el boto L1 del comanament de la PS4.
    #
    L1_BUTTON       = 4
    
    ##  el boto R1 del comanament de la PS4.
    #
    R1_BUTTON       = 5
    
    ##  el boto L2 del comanament de la PS4.
    #
    L2_BUTTON       = 6
    
    ##  el boto R2 del comanament de la PS4.
    #
    R2_BUTTON       = 7

    ##  el boto SHARE del comanament de la PS4.
    #
    SHARE_BUTTON    = 8
    
    ##  el boto OPTIONS del comanament de la PS4.
    #
    OPTIONS_BUTTON    = 9
    
    ## Instancia el modul de @b pygame i espera a que hi hagi un joystick conectat.
    #
    def init(self):
        pygame.init()

        # esperem que hi hagi un joystick conectat.
        #
        pygame.joystick.init()
        if (pygame.joystick.get_count() == 0):
            joyready = False
            while (not joyready):
                pygame.joystick.quit()
                time.sleep (1.0)
                pygame.joystick.init()
                joyready = (pygame.joystick.get_count() != 0)
            
        ## instancia i inicialitza el controlador de la PS4.
        #
        self._controller = pygame.joystick.Joystick(0)
        self._controller.init()

    ## transforma la coordenada del joystick a la posicio del motor en el rang [0.0, 1.0]
    #  @param[in] value la coordenada el joystick.
    #  @return la posicio del motor en el rang [0.0, 1.0]
    #
    def value2pos (self, value):
        position = (value + 1.0) / 2.0
        return min(max(position, 0.0),1.0)
        
    ## comença a escoltar events (moviments del joystick i pulsacions del botons)
    #  i els converteix a comanes de MQTT cap al robot.
    #  @note aquesta funcio es quedara bloquejada fins que es pitji el boto amb la creu.
    #
    def listen(self):
        
        quit           = False
        left_arm       = False
        left_arm_p     = -1.0
        right_arm      = False
        right_arm_p    = -1.0
        neckLR         = False
        neckLR_p       = -1.0
        left_eye       = False
        left_eye_p     = -1.0
        right_eye      = False
        right_eye_p    = -1.0
        neck_Body_UD   = False
        neck_Body_UD_p = -1
        neck_UD        = False
        neck_UD_p      = -1
        actions        = False
        state          = 0
        
        # processem els events fins que no s'indiqui el final.
        #
        while not quit:
            
            # llegim un event (boto o moviments del joystick).
            #
            for event in pygame.event.get():

                # moviment del joystick.
                #
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:
                        if neckLR:
                            # moving the neck left-right.
                            #
                            position = self.value2pos(event.value)
                            logging.debug("neckLR: {} {}".format(position, neckLR_p))
                            if position != neckLR_p:
                                publish.single ("robot/head/neck_LR/move", payload=str(position) , hostname='localhost')
                                neckLR_p = position
                            
                    if event.axis == 1:
                        if left_arm==True and right_arm==True:
                            # moving the left and right arm up-down.
                            #
                            position = 1.0 - self.value2pos(event.value)
                            logging.debug("left_arm: {} {}".format(position, left_arm_p))
                            if position != left_arm_p:
                                publish.single ("robot/body/left_arm/move", payload=str(position) , hostname='localhost')
                            logging.debug("right_arm: {} {}".format(position, right_arm_p))
                            if position != right_arm_p:
                                publish.single ("robot/body/right_arm/move", payload=str(position) , hostname='localhost')
                                
                        elif left_eye==True and right_eye==True:
                            # moving the left and right arm up-down.
                            #
                            position = 1.0 - self.value2pos(event.value)
                            logging.debug("left_arm: {} {}".format(position, left_eye_p))
                            if position != left_eye_p:
                                publish.single ("robot/head/left_eye/move", payload=str(position) , hostname='localhost')
                            logging.debug("right_eye: {} {}".format(position, right_eye_p))
                            if position != right_eye_p:
                                publish.single ("robot/head/right_eye/move", payload=str(position) , hostname='localhost')
                        elif left_arm:
                            # moving the left arm up-down.
                            #
                            position = 1.0 - self.value2pos(event.value)
                            logging.debug("left_arm: {} {}".format(position, left_arm_p))
                            if position != left_arm_p:
                                publish.single ("robot/body/left_arm/move", payload=str(position) , hostname='localhost')

                        elif right_arm:
                            # moving the right arm up-down.
                            #
                            position = 1.0 - self.value2pos(event.value)
                            logging.debug("right_arm: {} {}".format(position, right_arm_p))
                            if position != right_arm_p:
                                publish.single ("robot/body/right_arm/move", payload=str(position) , hostname='localhost')
                                
                        elif left_eye:
                            # moving the left arm up-down.
                            #
                            position = 1.0 - self.value2pos(event.value)
                            logging.debug("left_eye: {} {}".format(position, left_eye_p))
                            if position != left_eye_p:
                                publish.single ("robot/head/left_eye/move", payload=str(position) , hostname='localhost')
                                
                        elif right_eye:
                            # moving the left arm up-down.
                            #
                            position = 1.0 - self.value2pos(event.value)
                            logging.debug("right_eye: {} {}".format(position, right_eye_p))
                            if position != right_eye_p:
                                publish.single ("robot/head/right_eye/move", payload=str(position) , hostname='localhost')
                        elif neck_UD:
                            # moving the left arm up-down.
                            #
                            position = 1.0 - self.value2pos(event.value)
                            logging.debug("neck_UD: {} {}".format(position, neck_UD_p))
                            if position != neck_UD_p:
                                publish.single ("robot/head/neck_UD/move", payload=str(position) , hostname='localhost')
                        elif neck_Body_UD:
                            # moving the left arm up-down.
                            #
                            position = 1.0 - self.value2pos(event.value)
                            logging.debug("neck_UD: {} {}".format(position, neck_Body_UD_p))
                            if position != neck_Body_UD_p:
                                publish.single ("robot/body/neck/move", payload=str(position) , hostname='localhost')
                                
                # boto cap avall.
                #
                elif event.type == pygame.JOYBUTTONDOWN:
                    logging.debug("down {} button".format(event.button))
                    if event.button == self.L2_BUTTON:
                        left_arm = True
                    elif event.button == self.R2_BUTTON:
                        right_arm = True
                    elif event.button == self.CIRCLE_BUTTON:
                        neckLR = True
                    elif event.button == self.R1_BUTTON:
                        right_eye = True
                    elif event.button == self.L1_BUTTON:
                        left_eye = True
                    elif event.button == self.TRIANGLE_BUTTON:
                        neck_Body_UD = True
                    elif event.button == self.SQUARE_BUTTON:
                        neck_UD = True
                    elif event.button == self.OPTIONS_BUTTON:
                        actions = True
                        
                # boto cap amunt.
                #
                elif event.type == pygame.JOYBUTTONUP:
                    logging.debug("up {} button".format(event.button))
                    if event.button == self.CROSS_BUTTON:
                        publish.single ("robot/quit", payload="" , hostname='localhost', qos=2)
                        quit = True
                    elif event.button == self.SHARE_BUTTON:
                        quit = True
                    elif event.button == self.L2_BUTTON:
                        left_arm = False
                    elif event.button == self.R2_BUTTON:
                        right_arm = False
                    elif event.button == self.CIRCLE_BUTTON:
                        neckLR = False
                    elif event.button == self.TRIANGLE_BUTTON:
                        neck_Body_UD = False
                    elif event.button == self.SQUARE_BUTTON:
                        neck_UD = False
                    elif event.button == self.R1_BUTTON:
                        right_eye = False
                    elif event.button == self.L1_BUTTON:
                        left_eye = False
                    elif event.button == self.OPTIONS_BUTTON:
                        actions = False
                        
                elif event.type == pygame.JOYHATMOTION:
                    if event.hat == 0:
                        logging.debug("HAT button {} actions={} state={}".format(event.value, actions, state))
                        if (actions == True) and (event.value != (0,0)):
                            if state == 0:
                                if event.value == (0,1):
                                    state = 1
                            elif state == 1:
                                if event.value == (0,-1):
                                    state = 2
                                else:
                                    state = 0
                            elif state == 2:
                                if event.value == (0,1):
                                    state = 3
                                else:
                                    state = 0
                            elif state == 3:
                                if event.value == (0,-1):
                                    publish.single ("robot/dance", payload=str(0.0) , hostname='localhost')
                                state = 0

                                    
if __name__ == "__main__":
    
    parser = argparse.ArgumentParser(description='Robot Joystick Interface.')
    parser.add_argument('-d', '--debug', action="store_true", dest="debug", default=False, help="enable debug mode")
    args = parser.parse_args()

    format = "%(asctime)s: %(message)s"
    if args.debug:
        logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")
    else:
        logging.basicConfig(format=format, level=logging.INFO, datefmt="%H:%M:%S")
    

    robotps4 = RobotPS4Controller()
    robotps4.init()
    robotps4.listen()
