#!/usr/bin/env python2
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

import Queue
from listeners import rfid

class majordomo():
    def __init__(self, use_rfid=True):
        """
        """
        
        self.queue = Queue.Queue()
        if use_rfid:
            rfid_listener = rfid.RFIDdevice(device="auto", queue=self.queue)
            
m = majordomo()
