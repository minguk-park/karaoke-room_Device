import dbus
import dbus.mainloop.glib
from gpiozero import PWMOutputDevice
from time import sleep, time
 
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject
 
from bluez_components import *
 
mainloop = None
 
 
def set_vib(motor, value):
    if value[0] == 0x00:
        motor.value = 0.8
    else:
        motor.value = 0
 
class cmdChrc(Characteristic):
    CMD_UUID = 'c6a89af5-0385-4d4a-8cb4-c856fcbf1321'
 
    def __init__(self, bus, index, service, motor):
        Characteristic.__init__(
            self, bus, index,
            self.CMD_UUID, 
            ['read', 'write'],
            service)
        self.value = [ 0x00 for i in xrange(1024) ] 
        self.motor = motor
 
    def ReadValue(self, options):
        print('RowCharacteristic Read: ' + repr(self.value))
        return self.value
 
    def WriteValue(self, value, options):
        print("value:%s" % ''.join([str(v) for v in value]))
        #print('RowCharacteristic Write: ' + repr(value))
        set_vib(self.motor, value)
 
 
class MotorService(Service):
    DKDK_SVC_UUID = 'c6a89af5-0385-4d4a-8cb4-c856fcbf1320'
 
    def __init__(self, bus, index, motor):
        Service.__init__(self, bus, index, self.DKDK_SVC_UUID, True)
        self.add_characteristic(cmdChrc(bus, 0, self, motor))
 
 
class MotorApplication(Application):
    def __init__(self, bus, motor):
        Application.__init__(self, bus)
        self.add_service(MotorService(bus, 0, motor))
 
 
class MotorAdvertisement(Advertisement):
    def __init__(self, bus, index):
        Advertisement.__init__(self, bus, index, 'peripheral')
        self.add_service_uuid(MotorService.DKDK_SVC_UUID)
        self.include_tx_power = True
 
 
def setup_motor():
    motor = PWMOutputDevice(14)
    return motor
 
 
def register_ad_cb():
    """
    Callback if registering advertisement was successful
    """
    print('Advertisement registered')
 
 
def register_ad_error_cb(error):
    """
    Callback if registering advertisement failed
    """
    print('Failed to register advertisement: ' + str(error))
    mainloop.quit()
 
 
def register_app_cb():
    """
    Callback if registering GATT application was successful
    """
    print('GATT application registered')
 
 
def register_app_error_cb(error):
    """
    Callback if registering GATT application failed.
    """
    print('Failed to register application: ' + str(error))
    mainloop.quit()
 
 
def main():
    global mainloop
    global motor
 
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
 
    bus = dbus.SystemBus()
 
    # Get ServiceManager and AdvertisingManager
    service_manager = get_service_manager(bus)
    ad_manager = get_ad_manager(bus)
 
    # Create gatt services
    motor = setup_motor()
    app = MotorApplication(bus, motor)
 
    # Create advertisement
    dkdk_advertisement = MotorAdvertisement(bus, 0)
 
    mainloop = GObject.MainLoop()

    # Register gatt services
    service_manager.RegisterApplication(app.get_path(), {},
                                        reply_handler=register_app_cb,
                                        error_handler=register_app_error_cb)
    # Register advertisement
    ad_manager.RegisterAdvertisement(dkdk_advertisement.get_path(), {},
                                     reply_handler=register_ad_cb,
                                     error_handler=register_ad_error_cb)
    print("aaaaaaaaaa") 
    try:
        mainloop.run()
    except KeyboardInterrupt:
        print("Finished")
 
 
if __name__ == '__main__':
    main()