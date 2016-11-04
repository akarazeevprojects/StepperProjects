#!/usr/bin/python

import RPi.GPIO as GPIO
import sys
import os
import time
import argparse
 
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
 
enable_pin = 18
coil_A_1_pin = 4
coil_A_2_pin = 17
coil_B_1_pin = 23
coil_B_2_pin = 24
relay_pin = 9 

GPIO.setup(relay_pin, GPIO.OUT)
GPIO.setup(enable_pin, GPIO.OUT)
GPIO.setup(coil_A_1_pin, GPIO.OUT)
GPIO.setup(coil_A_2_pin, GPIO.OUT)
GPIO.setup(coil_B_1_pin, GPIO.OUT)
GPIO.setup(coil_B_2_pin, GPIO.OUT)
 
GPIO.output(enable_pin, 1)

def shoot(delay):
  GPIO.output(relay_pin, GPIO.LOW)
  time.sleep(delay)
  GPIO.output(relay_pin, GPIO.HIGH)
 
def forward(delay, steps): 
  for i in range(0, steps):
    setStep(1, 0, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    time.sleep(delay)
    setStep(1, 0, 0, 1)
    time.sleep(delay)
 
def backwards(delay, steps):  
  for i in range(0, steps):
    setStep(1, 0, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 0, 1)
    time.sleep(delay)
    setStep(0, 1, 1, 0)
    time.sleep(delay)
    setStep(1, 0, 1, 0)
    time.sleep(delay)
  
def setStep(w1, w2, w3, w4):
  GPIO.output(coil_A_1_pin, w1)
  GPIO.output(coil_A_2_pin, w2)
  GPIO.output(coil_B_1_pin, w3)
  GPIO.output(coil_B_2_pin, w4)

####################################
# Max Steps: 28000
# Time per 1000: 12 sec with delay=3
####################################

try:
  parser = argparse.ArgumentParser()
  parser.add_argument('direct', help='direction of the motor', type=int)
  parser.add_argument('number', help='number of photos', type=int)
  parser.add_argument('seconds', help='time per shot', type=int)
  parser.add_argument('-d','--delay', help='delay in forward/backwards', 
                      default=3, type=float)
  parser.add_argument('-l','--limit', help='quantity of big steps', 
                      default=28, type=int)
  parser.add_argument('-p','--pause', help='pause between big steps', 
                      default=0, type=float)
  parser.add_argument('-s','--steps', help='quantity of steps per big step', 
                      default=1000, type=int)

  args = parser.parse_args()

  direct = args.direct
  number = args.number
  limit = args.limit
  seconds = args.seconds
  pause = args.pause
  delay = args.delay
  steps = args.steps
  
  limit = number
  steps = int(28000. / float(limit))
  timing = (steps * limit * 4. * delay) / 1000.
  pause = int(((number * seconds) - timing) / limit)
  tot_time = int(timing + (pause * limit))
  
  print '|+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'
  print '|'
  print '+       Start with parameters:'
  print '| Direction: {}'.format(direct)
  print '+ Big steps: {}'.format(limit)
  print '| Steps per Big step: {}'.format(steps)
  print '|        Total steps: {}'.format(steps * limit)
  print '+ Time per shot: {} sec'.format(seconds)
  print '| Delay: {} msec'.format(delay)
  print '+ Time per forward/backwards: {} sec'.format((steps * 4. * delay) / 1000.)
  print '|        Total Time: {}h. {}m. {}s.'.format(tot_time / 3600, (tot_time / 60) % 3600, tot_time % 60)
  print '|            ({} sec)'.format(tot_time)
  print '|+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+'

  count = 0 
  while count < limit:
    count += 1

    shoot(seconds)
    
    if direct:
      forward(int(delay) / 1000.0, int(steps))
    else:
      backwards(int(delay) / 1000.0, int(steps))
    print 'Curr.count: {}/{}'.format(count,limit) 

  print 'Count is', count
  print 'Stop'
  setStep(0,0,0,0) # to release the coils
  GPIO.cleanup()

except KeyboardInterrupt:
  print 'Finish...'
  setStep(0,0,0,0)
  GPIO.cleanup()
