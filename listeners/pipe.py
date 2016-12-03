#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  pipe.py
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
#  Listen from pipefile
#  e.g.:  echo "TEST COMMAND" > /tmp/pipefile

import os, tempfile
import logging
import threading

class pipe():
    def __init__(self, pipefile, queue, actions):
        """
        Reads from a pipe
        """
        self.pipefile = pipefile
        self.queue = queue
        actions["pipe"] = {}


        self.__makefifo()
        
        self.listening_thread = threading.Thread(target=self.listen_from_pipe)
        #self.listening_thread.daemon = True
        self.isListening = True
        self.listening_thread.start()

    def transmit(self, received):
        """
        """
        cmd = ("pipe", received)
        self.queue.put(cmd)

    def __makefifo(self):
        """
        """
        try:
            os.mkfifo(self.pipefile)
            logging.debug("Listening to FIFO Pipe at %s" % self.pipefile)
            return True
        except:
            logging.debug("Error creating FIFO Pipe %s. File already existing?" % self.pipefile)
            return False

    def listen_from_pipe(self):
        """
        """
        while self.isListening:
            logging.debug("Listening from PIPE %s" % self.pipefile)
            with open(self.pipefile) as fifo:
                self.transmit(fifo.read().strip())
        
        
if __name__ == '__main__':

    p = pipe("pipefile", "none")
