# classes/relay_controller.py
import machine

class RelayController:
    def __init__(self, pin_num):
        self.relay_pin = machine.Pin(pin_num, machine.Pin.OUT)

    def activate_relay(self):
        # Activate the relay (close the circuit)
        self.relay_pin.value(1)
        print("Relay activated")

    def deactivate_relay(self):
        # Deactivate the relay (open the circuit)
        self.relay_pin.value(0)
        print("Relay deactivated")
