#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  mouse.py
#  
#  Copyright 2014 Giorgio Gilestro <gg@kozak>
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#  

#!/bin/env python
#This works with any mouse

import evdev
import threading
import os
import logging

import subprocess
import datetime
  
class mouseDevice():
    def __init__(self, device, queue, actions):
        """
        Initialize the class
        device:     a unix path to the input device
        queue:      the queue to which commands should be sent
        """
        
        self.queue = queue
        actions["mouse"] = {}
        
        self._lastbtndown = None
        
        if device.upper() == "AUTO":
            device = self.__find_device()
        
        if device: 
            self.dev = evdev.InputDevice(device)
                
            self.startListening()

    def __find_device(self, string="event-mouse"):
        """
        Internal routine used to automatically find the path to the input device
        """
        
        p1 = subprocess.Popen(["ls", "/dev/input/by-id/", "-la"], stdout=subprocess.PIPE)
        p2 = subprocess.Popen(["grep", string], stdin=p1.stdout, stdout=subprocess.PIPE)
        t = p2.communicate()[0]
        t = t.decode('utf-8').strip()
        try:
            _, d = os.path.split( t.split("->")[1] )
            dev = os.path.join ("/dev/input", d)
            logging.debug("Found mouse at %s" % dev)
        except:
            logging.debug("Could not automatically find a device containing the string %s " % string)
            dev = None
            
        return dev

    
    def listeningLoop(self):
        """
        """
        DOUBLECLICKTIME = 250 # ms
        HOLDTIME = 1 # seconds
        
        WHEEL = 8
        LEFT_BTN = 272
        RIGHT_BTN = 273
        MIDDLE_BTN = 274
        
        self._doubleclicktime = datetime.datetime.now()
        
        DCTIME = datetime.timedelta(microseconds=DOUBLECLICKTIME*1000)
        HTIME = datetime.timedelta(seconds=HOLDTIME)
        
        for event in self.dev.read_loop():
            if event.code == WHEEL: 
                self.transmit( "WHEEL_%s" % event.value )
            
            elif event.code == MIDDLE_BTN and event.value == 1:
                self._middlebtndown = datetime.datetime.now()

            elif event.code == MIDDLE_BTN and event.value == 0:
                hold = datetime.datetime.now() - self._middlebtndown
                delta = datetime.datetime.now() - self._doubleclicktime 
                self._doubleclicktime = datetime.datetime.now()
                self._middlebtndown = False
                
                if delta < DCTIME:
                    doubleclick = True
                    value = 99
                elif hold >= HTIME:
                    value = hold.seconds
                else:
                    value = event.value

                self.transmit( "BTN_C_%s" % value )

            elif event.code == LEFT_BTN and event.value == 1:
                self._leftbtndown = datetime.datetime.now()
                
            elif event.code == LEFT_BTN and event.value == 0:
                hold = datetime.datetime.now() - self._leftbtndown
                delta = datetime.datetime.now() - self._doubleclicktime 
                self._doubleclicktime = datetime.datetime.now()
                self._leftbtndown = False
                
                if delta < DCTIME:
                    doubleclick = True
                    value = 99
                elif hold >= HTIME:
                    value = hold.seconds
                else:
                    value = event.value

                self.transmit( "BTN_A_%s" % value )

            elif event.code == RIGHT_BTN and event.value == 1:
                self._rightbtndown = datetime.datetime.now()
                

            elif event.code == RIGHT_BTN  and event.value == 0:
                hold = datetime.datetime.now() - self._rightbtndown
                delta = datetime.datetime.now() - self._doubleclicktime 
                self._doubleclicktime = datetime.datetime.now()
                self._rightbtndown = False

                
                if delta < DCTIME:
                    doubleclick = True
                    value = 99
                elif hold >= HTIME:
                    value = hold.seconds
                else:
                    value = event.value

                self.transmit( "BTN_B_%s" % value )
    

    def transmit(self,event_code):
        """
        """
        cmd = ("mouse", event_code)
        self.queue.put(cmd)
        
    def startListening(self):
        """
        """
        self.listening_thread = threading.Thread(target=self.listeningLoop)
        #self.listening_thread.daemon = True
        self.isListening = True
        self.listening_thread.start()
        
    def stopListening(self):
        """
        """
        self.isListening = False
        
