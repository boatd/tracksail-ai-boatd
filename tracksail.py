# Python wrapper to interface with Tracksail-AI

# Copyright 2013-2014 Louis Taylor

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import socket

import boatd
assert boatd.VERSION == 1.1

driver = boatd.Driver()

def _float(v):
    if v:
        return float(v[:-1])
    else:
        return None

class Tracksail(object):
    def __init__(self, host='localhost', port=5555):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((host, port))
        self._rudderPos = 0

    def _send_command(self, command):
        self._socket.send(command)
        return self._socket.recv(256)

    @property
    def windDirection(self):
        """Return the direction of the wind"""
        return _float(self._send_command('get wind_dir'))

    def bearing(self):
        """Return the bearing of the boat"""
        return _float(self._send_command('get compass'))

    @property
    def sailPosition(self):
        return _float(self._send_command('get sail'))

    @sailPosition.setter
    def sailPosition(self, value):
        self._send_command('set sail {}'.format(int(value)))

    @property
    def rudderPosition(self):
        return self._rudderPos

    @rudderPosition.setter
    def rudderPosition(self, value):
        value_rounded = int(round(value))
        self._send_command('set rudder {}'.format(value_rounded))

    @property
    def latitude(self):
        return self._send_command('get northing')

    @property
    def longitude(self):
        return self._send_command('get easting')

tracksail = Tracksail()

@driver.heading
def tracksail_heading():
    return tracksail.bearing()

@driver.wind_direction
def tracksail_wind():
    return tracksail.windDirection

@driver.position
def tracksail_lat_long():
    return (tracksail.latitude, tracksail.longitude)

@driver.rudder
def tracksail_set_rudder(angle):
    if angle < 0:
        tracksail.rudderPosition = -1 * angle
    else:
        tracksail.rudderPosition = 360 - angle
