#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
#  majordomo_mpd.py
#  
#  Copyright 2016 Giorgio Gilestro <giorgio@gilest.ro>
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

#http://pythonhosted.org/python-mpd2/topics/commands.html

from mpd import MPDClient
import logging

class mpd_connection(MPDClient):
    def __init__(self, host="localhost", port=6600):
        """
        """
        super(mpd_connection, self).__init__()
        
        # use_unicode will enable the utf-8 mode for python2
        # see http://pythonhosted.org/python-mpd2/topics/advanced.html#unicode-handling
        #self(use_unicode=True)
        self.connect(host, port)

    def isPlaying(self):
        """
        """
        return self.status()["state"] == "play"
        
    def getVolume(self):
        """
        """
        return int(self.status()["volume"])
        
        
    def toggle(self):
        """
        """
        if self.isPlaying(): 
            self.stop()
        else:
            self.play()
            
    def volume(self, vol):
        """
        """
        current_vol = self.getVolume()
        
        if str(vol).startswith("+") or str(vol).startswith("-"):
            vol = current_vol + int(vol)
        
        vol = int(vol)
        
        if vol > 0 and vol <=100:
            self.setvol(vol)
            logging.debug("Volume set to %s" % vol)

    def loadAlbum(self, title):
        """
        """
        self.stop()
        self.clear()
        songs = self.findadd( "album", title )
        self.play()
        
    def loadPlaylist(self, title):
        """
        """
        self.stop()
        self.clear()
        self.repeat(1)
        self.load(title)
        self.play()

            
        

if __name__ == '__main__':
    c = mpd_connection("radiopi")
    
