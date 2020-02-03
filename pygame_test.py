#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# This file presents an interface for interacting with the Playstation 4 Controller
# in Python. Simply plug your PS4 controller into your computer using USB and run this
# script!
#
# NOTE: I assume in this script that the only joystick plugged in is the PS4 controller.
#       if this is not the case, you will need to change the class accordingly.
#
# Copyright © 2015 Clay L. McLeod <clay.l.mcleod@gmail.com>
#
# Distributed under terms of the MIT license.

import os
import pprint
import pygame
import paho.mqtt.publish as publish
import sys
import logging

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

        quit     = False
        left_arm = False
        neckLR   = False
        while not quit:
            for event in pygame.event.get():
                if event.type == pygame.JOYAXISMOTION:
                    if event.axis == 0:
                        if neckLR:
                            # moving the neck left-right.
                            #
                            position = self.value2pos(event.value)
                            logging.debug("neckLR: {}".format(position))
                            publish.single ("robot/head/neck_LR/move", payload=str(position) , hostname='localhost')
                            
                    if event.axis == 1:
                        if event.value > 0:
                            print "axis down"
                        if event.value < 0:
                            print "axis up"

                elif event.type == pygame.JOYBUTTONDOWN:
                    print "pressed down the {} button".format(event.button)
                    if event.button == self.L2_BUTTON:
                        left_arm = True
                    elif event.button == self.CIRCLE_BUTTON:
                        neckLR = True
                    
                elif event.type == pygame.JOYBUTTONUP:
                    print "pressed up the {} button".format(event.button)
                    if event.button == self.CROSS_BUTTON:
                        publish.single ("robot/quit", payload="" , hostname='localhost')
                        quit = True
                    elif event.button == self.L2_BUTTON:
                        left_arm = False
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
