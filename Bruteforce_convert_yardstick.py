import sys
import time
from rflib import *
from struct import *

# User defined parameters 
_digital_footprint = "011100110010000000010011100111000001100" # My footprint: (short transition from 'space to mark')
#_digital_footprint = "11000111010000" # BB King's footprint: (long transition from 'space to mark')
_frequency = 433890000
_baudrate = 4800
_modulation = "MOD_ASK_OOK"  # Modulation Type (not alterable in this version)
_mult = 3  # Number of times to transmit RF signal
_pad_bytes = 0 # Number of zero bytes for trailing padding
_method = "0" # Time period of 'valley' gap when transitioning from space to mark in footprint:
 # Short period (1 bit time period) : _method = "0"
 # Long period (3 bit time period)  : _method = "1"

# Configure rf_cat 
d = RfCat()

d.setFreq(_frequency)
d.setMdmModulation(MOD_ASK_OOK)
d.setMdmDRate(_baudrate)

print "SIGNAL INFORMATION"
print "------------------"
print "Frequency:                 ", _frequency
print "Baud rate:                 ", _baudrate
print "ModulationType:            ", _modulation
print "Repeat transmission count: ", _mult
print "Digital footprint:         ", _digital_footprint

mark_space = str(_digital_footprint)
xmt_stream = ""

# Scan each digital footprint bit (pulse) and convert it to the appropriate 4-bit value
# Mark = 1 (short pulse) and Space = 0 (long pulse)
mark_space = str(_digital_footprint)
xmt_stream = ""

if (_method == "0"): # transitions from space to mark (in footprint) are short (1 bit time period)
 for i in mark_space:

	if (i == "0"): # Space
		_pulse = "1110"

	if (i == "1"): # Mark
		_pulse = "1000"

	xmt_stream = xmt_stream + _pulse

if (_method == "1"): # transitions from space to mark (in footprint) are long (3 bit time period)
 for i in mark_space:

	if (i == "0"): # Space
		_pulse = "0111"

	if (i == "1"): # Mark
		_pulse = "0001"

 	xmt_stream = xmt_stream + _pulse

# If length of digital footprint is odd, then pad it with "0000" to make it 8 bits
if (len(_digital_footprint) % 2 != 0):
 xmt_stream = xmt_stream + "0000"

# Pad zeroes for gap length between transmissions
_padding = ""
for i in range(0, _pad_bytes):
 xmt_stream = xmt_stream + "00000000"
 _padding = _padding + "00000000"
print "Trailing padding:          ", _padding
 
print "RF transmit binary stream: ", xmt_stream

# Convert binary transmit stream to hex equivalent'
hex_xmt_stream = str(('%08X' % int(xmt_stream, 2)))
print "RF transmit hex stream:    ", hex_xmt_stream


mod_xmt_stream = ""
for i in xrange(0, len(hex_xmt_stream), 2):
 ch = "\\x"
 mod_xmt_stream = mod_xmt_stream + (ch + (hex_xmt_stream[i:i+2]))
print "Modified RF hex stream:    ", mod_xmt_stream

# -------------------Send Transmission ----------------------------------------#
print "Starting transmission ..."

hex_data = bytearray.fromhex(hex_xmt_stream)
d.RFxmit(hex_data, repeat = _mult)

d.setModeIDLE()
print " "
print "Transmission Complete"
