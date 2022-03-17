import pigpio 
import time
from datetime import datetime


'''
   1. script to initialise GPIO pins and all variables, import from config.json
   2. includes class decoder
   3. includes function to detect events 
   3. includes class Timer
'''


class decoder:

   #callback refers to the function that is being called when the wiegand reader reads an input 
   #entrance refers to the particular entrance and reader e.g. E1R1
   def __init__(self, pi, gpio_0, gpio_1, callback, entrance, bit_timeout=5):


      self.pi = pi
      self.gpio_0 = gpio_0
      self.gpio_1 = gpio_1

      self.callback = callback

      self.bit_timeout = bit_timeout

      self.entrance = entrance

      self.in_code = False

      self.pi.set_mode(gpio_0, pigpio.INPUT)
      self.pi.set_mode(gpio_1, pigpio.INPUT)

      self.pi.set_pull_up_down(gpio_0, pigpio.PUD_UP)
      self.pi.set_pull_up_down(gpio_1, pigpio.PUD_UP)
    
      self.cb_0 = self.pi.callback(gpio_0, pigpio.FALLING_EDGE, self._cb)
      self.cb_1 = self.pi.callback(gpio_1, pigpio.FALLING_EDGE, self._cb)        
            
   def _cb(self, gpio, level,tick):

      """
      Accumulate bits until both gpios 0 and 1 timeout.
      """

      if level < pigpio.TIMEOUT:

         if self.in_code == False:
            self.bits = 1
            self.num = 0

            self.in_code = True
            self.code_timeout = 0
            self.pi.set_watchdog(self.gpio_0, self.bit_timeout)
            self.pi.set_watchdog(self.gpio_1, self.bit_timeout)
         else:
            self.bits += 1
            self.num = self.num << 1

         if gpio == self.gpio_0:
            self.code_timeout = self.code_timeout & 2 # clear gpio 0 timeout
         else:
            self.code_timeout = self.code_timeout & 1 # clear gpio 1 timeout
            self.num = self.num | 1

      else:

         if self.in_code:

            if gpio == self.gpio_0:
               self.code_timeout = self.code_timeout | 1 # timeout gpio 0
            else:
               self.code_timeout = self.code_timeout | 2 # timeout gpio 1

            if self.code_timeout == 3: # both gpios timed out
               self.pi.set_watchdog(self.gpio_0, 0)
               self.pi.set_watchdog(self.gpio_1, 0)
               self.in_code = False
               self.callback(self.bits, self.num,self.entrance)
               return



   def cancel(self):

      """
      Cancel the Wiegand decoder.
      """

      self.cb_0.cancel()
      self.cb_1.cancel()







Relay_1 = 27 
Relay_2 = 13

E1_R1_D0= 22
E1_R1_D1= 10
#E1_R1_Buzz=
#E1_R1_Led=
E1_R2_D0=24
E1_R2_D1=25
#E1_R2_Buzz=
#E1_R2_Led=
E1_Mag= 6
E1_Button= 5

'''
E2_R1_D0=
E2_R1_D1=

E2_R1_Buzz=
E2_R1_Led=
E2_R2_D0=
E2_R2_D1=
E2_R2_Buzz=
E2_R2_Led=
E2_Mag=
E2_Button=
'''

#initialising pi
pi = pigpio.pi()

#initialising E1_Button for pushbutton1
pi.set_mode(E1_Button, pigpio.INPUT)
#pi.set_pull_up_down(E1_Button, pigpio.PUD_UP)

#E1_Mag for mag contact
pi.set_mode(E1_Mag, pigpio.INPUT) 
pi.set_pull_up_down(E1_Mag, pigpio.PUD_UP)
'''
#E1_R1_Buzz for Buzz
pi.set_mode(E1_R1_Buzz, pigpio.INPUT) 
pi.set_pull_up_down(E1_R1_Buzz, pigpio.PUD_UP)

#E1_R1_Led for Led
pi.set_mode(E1_R1_Led, pigpio.INPUT) 
pi.set_pull_up_down(E1_R1_Led, pigpio.PUD_UP)

#E1_R2_Buzz for Buzz
pi.set_mode(E1_R2_Buzz, pigpio.INPUT) 
pi.set_pull_up_down(E1_R2_Buzz, pigpio.PUD_UP)

#E1_R2_Led for Led
pi.set_mode(E1_R2_Led, pigpio.INPUT) 
pi.set_pull_up_down(E1_R2_Led, pigpio.PUD_UP)

#initialising E2_Button for pushbutton2
pi.set_mode(E2_Button, pigpio.INPUT)
pi.set_pull_up_down(E2_Button, pigpio.PUD_UP)

#E2_Mag for mag contact
pi.set_mode(E2_Mag, pigpio.INPUT) 
pi.set_pull_up_down(E2_Mag, pigpio.PUD_UP)

#E2_R1_Buzz for Buzz
pi.set_mode(E2_R1_Buzz, pigpio.INPUT) 
pi.set_pull_up_down(E2_R1_Buzz, pigpio.PUD_UP)

#E2_R1_Led for Led
pi.set_mode(E2_R1_Led, pigpio.INPUT) 
pi.set_pull_up_down(E2_R1_Led, pigpio.PUD_UP)

#E2_R1_Buzz for Buzz
pi.set_mode(E2_R2_Buzz, pigpio.INPUT) 
pi.set_pull_up_down(E2_R2_Buzz, pigpio.PUD_UP)

#E2_R1_Led for Led
pi.set_mode(E2_R2_Led, pigpio.INPUT) 
pi.set_pull_up_down(E2_R2_Led, pigpio.PUD_UP)
'''




