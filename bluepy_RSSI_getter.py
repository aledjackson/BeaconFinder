import bluepy
import sys

manufacturer = sys.argv[1]

print "scanning for device with manufacture data |" + manufacturer + "|"

# import the necessary parts of the bluepy library
from bluepy.btle import Scanner, DefaultDelegate


global_RSSIs = []
# create a delegate class to receive the BLE broadcast packets
class ScanDelegate(DefaultDelegate):
    def __init__(self):
        DefaultDelegate.__init__(self)


    # when this python script discovers a BLE broadcast packet, print a message with the device's MAC address
    def handleDiscovery(self, dev, isNewDev, isNewData):
        for (adtype, desc, value) in dev.getScanData():
                if desc == "Manufacturer" and value == manufacturer:
                    global_RSSIs.append(dev.rssi)

    def gatherAverageRSSI(self,manufacturer, n_samples):
        global_RSSIs = []
        while len(global_RSSIs) < n_samples:
            scanner.scan(1.0)
        mean_rssi = mean(global_RSSIs)
        std_dev = std(global_RSSIs)

        cutoff_rssi = []

        lower_cutoff = mean_rssi - std_dev
        upper_cutoff = mean_rssi + std_dev
        for x in global_RSSIs:
            if not (x < lower_cutoff or x > upper_cutoff):
                cutoff_rssi.append(x)
        
        return mean(cutoff_rssi)




# create a scanner object that sends BLE broadcast packets to the ScanDelegate
scanner = Scanner().withDelegate(ScanDelegate())

scanner.gatherAverageRSSI(manufacturer, 10)

