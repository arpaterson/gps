#! /usr/bin/python
# Written by Dan Mandle http://dan.mandle.me September 2012
# License: GPL 2.0
 
import os
import io
import threading
import time
from gps import *
 
gpsd = None #seting the global variable
 
os.system('clear') #clear the terminal (optional)
 
class GpsPoller(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    global gpsd #bring it in scope
    gpsd = gps(mode=WATCH_ENABLE) #starting the stream of info
    self.current_value = None
    self.running = True #setting the thread running to true
 
  def run(self):
    global gpsd
    while self.running:
      gpsd.next() #this will continue to loop and grab EACH set of gpsd info to clear the buffer
 
if __name__ == '__main__':
 
  os.chdir('/var/www/logs')

  gpsp = GpsPoller() # create the thread
  try:
    unitname = os.uname()[1]
    starttime = time.strftime("%Y%m%d-%H%M%S")
    filename = unitname + '_' + starttime + '_log_GPS.csv'
    bufsize = 1
    fid = io.open(filename,'w', bufsize)
    fid.write(u'sysutc, latitude, longitude, gpsutc, gpsfixtime, altitude (m), eps, epx, ept, speed (m/s), climb, track, mode\r\n')
    gpsp.start() # start it up
    time.sleep(5)
      #It may take a second or two to get good data
      #print gpsd.fix.latitude,', ',gpsd.fix.longitude,'  Time: ',gpsd.utc
    while True:
 
      os.system('clear')

      fid.write(u'{:f}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}\r\n'.format(
					time.time(), 
				    	gpsd.fix.latitude,
					gpsd.fix.longitude,
					gpsd.utc,
					gpsd.fix.time,
					gpsd.fix.altitude,
					gpsd.fix.eps,
					gpsd.fix.epx,
					gpsd.fix.ept,
					gpsd.fix.speed,
					gpsd.fix.climb,
					gpsd.fix.track,
					gpsd.fix.mode,
					)
		)
 
      print
      print ' GPS reading'
      print '----------------------------------------'
      print 'latitude    ' , gpsd.fix.latitude
      print 'longitude   ' , gpsd.fix.longitude
      print 'time utc    ' , gpsd.utc,' + ', gpsd.fix.time
      print 'altitude (m)' , gpsd.fix.altitude
      print 'eps         ' , gpsd.fix.eps
      print 'epx         ' , gpsd.fix.epx
      print 'epv         ' , gpsd.fix.epv
      print 'ept         ' , gpsd.fix.ept
      print 'speed (m/s) ' , gpsd.fix.speed
      print 'climb       ' , gpsd.fix.climb
      print 'track       ' , gpsd.fix.track
      print 'mode        ' , gpsd.fix.mode
      print
      print 'sats        ' , gpsd.satellites
 
      time.sleep(1) #set to whatever
 
  except (KeyboardInterrupt, SystemExit): #when you press ctrl+c
    fid.close()
    print "\nKilling Thread..."
    gpsp.running = False
    gpsp.join() # wait for the thread to finish what it's doing
  print "Done.\nExiting."

