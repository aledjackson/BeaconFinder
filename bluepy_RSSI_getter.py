import bluepy
import sys
from statistics import stdev

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
                    print("found one")


def mean(numbers):
    if len(numbers) == 0:
        return None
    return float(sum(numbers)) / max(len(numbers), 1)

def gatherAverageRSSI(manufacturer, n_samples, scanner):
    RSSIs= []

    while len(RSSIs) < n_samples:
        new_devices = scanner.scan(1.0)
        for dev in new_devices:
            for (adtype, desc, value) in dev.getScanData():
                if desc == "Manufacturer" and value == manufacturer:
                    RSSIs.append(dev.rssi)



    mean_rssi = mean(RSSIs)
    std_dev = stdev(RSSIs)

    cutoff_rssi = []

    lower_cutoff = mean_rssi - std_dev
    upper_cutoff = mean_rssi + std_dev
    for x in RSSIs:
        if not (x < lower_cutoff or x > upper_cutoff):
            cutoff_rssi.append(x)
    
    return mean(cutoff_rssi)



# create a scanner object that sends BLE broadcast packets to the ScanDelegate
scanner = Scanner().withDelegate(ScanDelegate())

while True:
    print(gatherAverageRSSI(manufacturer, 10, scanner))

