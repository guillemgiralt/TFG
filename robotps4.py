
import os
import pprint
import pygame
import paho.mqtt.publish as publish
import sys
import logging
import time

class PS4Controller(object):
    """Class representing the PS4 controller. Pretty straightforward functionality."""

    controller = None
    axis_data = None
    button_data = None
    hat_data = None
    CROSS_BUTTON    = 0
    CIRCLE_BUTTON   = 1
    TRIANGLE_BUTTON = 2
    SQUARE_BUTTON   = 3
    L2_BUTTON       = 6
    R2_BUTTON       = 7
    SHARE_BUTTON    = 8

    def init(self):
        """Initialize the joystick components"""
        
        pygame.init()
        pygame.joystick.init()
        self.controller = pygame.joystick.Joystick(0)
        self.controller.init()

    def value2pos (self, value):
        position = (value + 1.0) / 2.0
        return min(max(position, 0.0),1.0)
        
    def listen(self):
        """Listen for events to happen"""
        
        if not self.axis_data:
            self.axis_data = {}

        if not self.button_data:
            self.button_data = {}
            for i in range(self.controller.get_numbuttons()):
                self.button_data[i] = False

        if not self.hat_data:
            self.hat_data = {}
            for i in range(self.controller.get_numhats()):
                self.hat_data[i] = (0, 0)

        quit        = False
        left_arm    = False
        left_arm_p  = -1.0
        right_arm   = False
        right_arm_p = -1.0
        neckLR      = False
        neckLR_p    = -1.0
        while not quit:
            for event in pygame.event.get():
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
                        if left_arm:
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
                            logging.debug("right_arm: {}{}".format(position, right_arm_p))
                            if position != right_arm_p:
                                publish.single ("robot/body/right_arm/move", payload=str(position) , hostname='localhost')

                elif event.type == pygame.JOYBUTTONDOWN:
                    print "pressed down the {} button".format(event.button)
                    if event.button == self.L2_BUTTON:
                        left_arm = True
                    elif event.button == self.R2_BUTTON:
                        right_arm = True
                    elif event.button == self.CIRCLE_BUTTON:
                        neckLR = True
                    
                elif event.type == pygame.JOYBUTTONUP:
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
                        
                elif event.type == pygame.JOYHATMOTION:
                    print "pressed hat {} button".format(event.hat)
                    if event.hat == 0:
                        if event.value == (1, 0):
                            print "right"
                        if event.value == (-1, 0):
                            print "left"
                        if event.value == (0, 1):
                            print "up"
                        if event.value == (0, -1):
                            print "down"


if __name__ == "__main__":
    
    format = "%(asctime)s: %(message)s"
    logging.basicConfig(format=format, level=logging.DEBUG, datefmt="%H:%M:%S")

    ps4 = PS4Controller()
    ps4.init()
    ps4.listen()
