import bluepy
import sys

MAC_addr = sys.argv[1]

print "scanning for |" + MAC_addr + "|"

# import the necessary parts of the bluepy library
from bluepy.btle import Scanner, DefaultDelegate

# create a delegate class to receive the BLE broadcast packets
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # when this python script discovers a BLE broadcast packet, print a message with the device's MAC address
    def handleDiscovery(self, dev, isNewDev, isNewData):
	if isNewDev:
		print dev.addr
        if dev.addr == MAC_addr:
            print "RSSI : " + str(dev.rssi)



# create a scanner object that sends BLE broadcast packets to the ScanDelegate
scanner = Scanner().withDelegate(ScanDelegate())

while True:
    scanner.scan(10.0)


