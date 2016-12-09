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
# http://pythonhosted.org/python-mpd2/topics/commands.html


import queue
import threading
import json
import logging
import optparse

import shlex, subprocess
from listeners import rfid, pipe, mouse
from actors import majordomo_mpd

class majordomo():
    def __init__(self, use_rfid=True, use_mouse=True, use_pipe=True, use_mpd="localhost:6600" ):
        """
        """
        self.queue = queue.Queue()
        
        self.actions = {}
        
        if use_rfid:
            rfid.RFIDdevice(device="AUTO", queue=self.queue, actions=self.actions)
            
        if use_mouse:
            mouse.mouseDevice(device="AUTO", queue=self.queue, actions=self.actions)
            
        if use_pipe:
            pipe.pipe("/tmp/pipefile", queue=self.queue, actions=self.actions)

        host, port = use_mpd.split(":")
        self.mpc = majordomo_mpd.mpd_connection(host, port)

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
            logging.debug("%s: %s" % (ct, cmd))
            self.execute(ct, cmd)

    def loadActions(self):
        """
        """
        #try:
        with open('majordomo.json', 'r') as configfile:
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
            logging.debug("Saved options to file")

    def learn(self, ct, cmd, action):
        """
        ct:         command_type    (e.g. mouse, rfid, pipe, etc)
        cmd:        command         (e.g. wheel_+1, 4f1eb730, play, etc)
        action:     action          (e.g. mpc stop or mpc volume +5)
        """
        self.actions[ct][command] = action
        
    def execute(self, ct, cmd):
        """
        Available types of actions:
        mpc       -> controls mpd through the python binding
        majordomo -> internal commands
        exec      -> send a command line output
        """
        if ct in self.actions:
            if cmd in self.actions[ct]:
                args = shlex.split(self.actions[ct][cmd])

                if args[0] == "majordomo":
                    try:
                        getattr(self, args[1])(args[2])
                    except:
                        getattr(self, args[1])()
                
                if args[0] == "mpc":
                    try:
                        getattr(self.mpc, args[1])(args[2])
                    except:
                        getattr(self.mpc, args[1])()
                
                if args[0] == "exec":
                    p = subprocess.Popen(args[1:])
                    logging.debug(self.actions[ct][cmd])
                    logging.debug(p.communicate())
        
    def quit(self):
        """
        """
        self.isListening = False
        
if __name__ == '__main__':
    parser = optparse.OptionParser()
 
    parser.add_option("-M", "--mouse", dest="mouse", default=False, help="Use mouse as listener", action="store_true")
    parser.add_option("-R", "--RFID", dest="RFID", default=False, help="Use RFID as listener", action="store_true")
    parser.add_option("--MPD", dest="mpd", default="localhost:6600", help="Define MPD host. default localhost:6600")

    parser.add_option("-D", "--debug", dest="debug", default=False, help="Shows all logging messages", action="store_true")
 
 
    (options, args) = parser.parse_args()
    option_dict = vars(options)
    
    if option_dict["debug"]:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.debug("Logger in DEBUG mode")
        
    
    m = majordomo(use_rfid = option_dict["RFID"], use_mouse = option_dict["mouse"], use_pipe = True, use_mpd = option_dict["mpd"])
