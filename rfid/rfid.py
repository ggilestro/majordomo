#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  rfid.py
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

#!/bin/env python2
import evdev
import threading
import os

class RFIDdevice():
    def __init__(self, device, useUDEV=True):
        """
        """
        self.useUDEV = useUDEV
        
        if self.useUDEV:
            self.dev = evdev.InputDevice(device)
        else:
            self.dev = open(device, 'r')
            
        self.getActions()
        self.startListening()
        
    def getActions(self):
        """
        """
        self.actions = {
            '0a5ce5bd' : '/opt/majordomo/bin/play-youtube E9XQ2MdNgKY'
                }
                    
    
    def listeningLoop(self):
        """
        """
        rfid_code = ""
        i =0
        
        scancodes = {
            # Scancode: ASCIICode
            0: None, 1: u'ESC', 2: u'1', 3: u'2', 4: u'3', 5: u'4', 6: u'5', 7: u'6', 8: u'7', 9: u'8',
            10: u'9', 11: u'0', 12: u'-', 13: u'=', 14: u'BKSP', 15: u'TAB', 16: u'q', 17: u'w', 18: u'e', 19: u'r',
            20: u't', 21: u'y', 22: u'u', 23: u'i', 24: u'o', 25: u'p', 26: u'[', 27: u']', 28: u'CRLF', 29: u'LCTRL',
            30: u'a', 31: u's', 32: u'd', 33: u'f', 34: u'g', 35: u'h', 36: u'j', 37: u'k', 38: u'l', 39: u';',
            40: u'"', 41: u'`', 42: u'LSHFT', 43: u'\\', 44: u'z', 45: u'x', 46: u'c', 47: u'v', 48: u'b', 49: u'n',
            50: u'm', 51: u',', 52: u'.', 53: u'/', 54: u'RSHFT', 56: u'LALT', 100: u'RALT'
        }        
                
        if self.useUDEV:

            for event in self.dev.read_loop():
                if event.type == evdev.ecodes.EV_KEY:
                    data = evdev.categorize(event)  # Save the event temporarily to introspect it
                    if data.keystate == 1:  # Down events only
                        character = u'{}'.format(scancodes.get(data.scancode))
                        if character == u'CRLF':
                            self.transmit( rfid_code )
                            rfid_code = ""
                        else:
                            rfid_code += character

        else:
            while i in range(20):
                for character in self.dev.read():
                        if ord(character) == 10: 
                            self.transmit(rfid_code)
                            rfid_code = ""
                        else:
                            rfid_code += str(character)


    def transmit(self,rfid_code):
        """
        """
        print "Received: %s\n" % rfid_code 
        self.execute(rfid_code)
        
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
        
    def learn(self, rfid, action):
        """
        """
        self.actions[rfid] = action
        
    def execute(self, rfid):
        """
        """
        if rfid in self.actions:
            os.system(self.actions[rfid])
        

        
r = RFIDdevice('/dev/input/event15')

