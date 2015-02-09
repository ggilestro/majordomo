#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  majordomo.py
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

#TODO
# http://www.hackerposse.com/~rozzin/journal/whole-home-pulseaudio.html
import queue
import threading
import json

import shlex, subprocess
from listeners import rfid, pipe, mouse


class majordomo():
    def __init__(self, use_rfid=True, use_pipe=True, use_mouse=True, verbose=False):
        """
        """
        self.verbose = verbose
        self.queue = queue.Queue()
        
        self.actions = {}
        
        if use_rfid:
            rfid.RFIDdevice(device="AUTO", queue=self.queue, actions=self.actions)
            
        if use_mouse:
            mouse.mouseDevice(device="/dev/input/event3", queue=self.queue, actions=self.actions)
            
        if use_pipe:
            pipe.pipe("/tmp/pipefile", queue=self.queue, actions=self.actions)

        self.loadActions()
            
        self.listening_thread = threading.Thread(target=self.readQueue)
        #self.listening_thread.daemon = True
        self.isListening = True
        self.listening_thread.start()
   
    def readQueue(self):
        """
        Listen from incoming commands. The queue is shared among several listeners (.e.g RFID, voice rec, etc)
        """
        while self.isListening:
            ct, cmd = self.queue.get()
            if self.verbose:
                print (ct, ":", cmd)
                
            self.execute(ct, cmd)

    def loadActions(self):
        """
        """
        #try:
        with open('/opt/majordomo/majordomo.json', 'r') as configfile:
            self.actions = json.load( configfile )
        #except:
            #self.actions["mouse"] = { 'WHEEL_1' : 'mpc volume +2' , 'WHEEL_-1' : 'mpc volume -2', 'BTN_A_0' : 'mpc prev', 'BTN_B_0' : 'mpc next', 'BTN_A_99' : 'mpc pause', 'BTN_B_99' : 'bin/mpc_load_radio.sh', 'BTN_A_2' : 'bin/say_time.sh'}
            #self.actions["rfid"] = { '4f1eb730' : 'mpsyt playurl E9XQ2MdNgKY', '0a5ce5bd' : 'mpsyt playurl E9XQ2MdNgKY' }
            #self.actions["pipe"] = { 'play' : 'mpc play', 'stop' : 'mpc stop', 'load_radio' : 'mpc clear ; mpc lsplaylists | mpc load ; mpc play' }
            #self.saveActions()
        
    def saveActions(self):
        """
        """
        with open('majordomo.json', 'w') as configfile:
            json.dump(self.actions, configfile, indent=4)

    def learn(self, ct, cmd, action):
        """
        ct:         command_type    (e.g. mouse, rfid, pipe, etc)
        cmd:        command         (e.g. wheel_+1, 4f1eb730, play, etc)
        action:     action          (e.g. mpc stop)
        """
        self.actions[ct][command] = action
        
    def execute(self, ct, cmd):
        """
        """
        if ct in self.actions:
            if cmd in self.actions[ct]:
                
                args = shlex.split(self.actions[ct][cmd])
                p = subprocess.Popen(args)

                if self.verbose:
                    print (self.actions[ct][cmd])
                    print (p.communicate())
        
    def quit(self):
        """
        """
        self.isListening = False
        
m = majordomo(verbose=True)
