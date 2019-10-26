# import the necessary parts of the bluepy library
from bluepy.btle import Scanner, DefaultDelegate

# create a delegate class to receive the BLE broadcast packets
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)

    # when this python script discovers a BLE broadcast packet, print a message with the device's MAC address
    def handleDiscovery(self, dev, isNewDev, isNewData):
        if isNewDev:
            print "Discovered device", dev.addr
        elif isNewData:
            print "Received new data from", dev.addr

# create a scanner object that sends BLE broadcast packets to the ScanDelegate
scanner = Scanner().withDelegate(ScanDelegate())

# create a list of unique devices that the scanner discovered during a 10-second scan
devices = scanner.scan(10.0)

desc_set = set()

# for each device  in the list of devices
for dev in devices:
    

    for (adtype, desc, value) in dev.getScanData():
        desc_set.add(desc)

        # print "  %s = %s" % (desc, value)
        if (desc == "Manufacturer" and "01010101" in value) :
            print("found you boi")
            print "Device %s (%s), RSSI=%d dB" % (dev.addr, dev.addrType, dev.rssi)
            print "  %s = %s" % (desc, value)


        # if (desc == "Complete Local Name" or desc == "Short Local Name" or desc == ""):
        #     print "  %s = %s" % (desc, value)


print "printing the sets"
for x in desc_set:
    print x

