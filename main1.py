import machine
import network
import time
from Classes.mongodb_handler import MongoDBHandler
from Classes.relay_controller import RelayController
from Classes.modbus_handler import ModbusHandler
from machine import Pin

# Constants for your WiFi credentials
INTERNET_NAME = "Galaxy-A04e"
INTERNET_PASSWORD = "nzvy9668"

DEVICE_ID = "EMTECH001"

# Define your URL and API Key
URL = "https://ap-south-1.aws.data.mongodb-api.com/app/data-ayowg/endpoint/data/v1/action/"
API_KEY = "HL3fefAMoRVpkF75bekFPvmevUlfLpzOTH7rmDSqsAzIuWpDeZM0s8W55LWTh1St"

# Specify the pin number for the relay
RELAY_PIN = 2  # Example pin number, replace with the actual pin number


Wifi_Pin = 9  # The pin number you want to activate
pin = Pin(Wifi_Pin, Pin.OUT)  # Create a Pin object in output mode
pin.value(1)  # Set the pin high (3.3V)

# Constants for ModbusHandler
RXD2 = 1
TXD2 = 0

def main():
    # Create MongoDBHandler instance
    mongo_handler = MongoDBHandler(url=URL, api_key=API_KEY)
    
    # Create RelayController instance with specified pin number
    relay_controller = RelayController(RELAY_PIN)

    # Create ModbusHandler instance
    modbus_handler = ModbusHandler(uart_num=0, baudrate=9600, tx_pin=TXD2, rx_pin=RXD2)

    # Connect to WiFi
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    while True:
        try:
            wlan.connect(INTERNET_NAME, INTERNET_PASSWORD)
            while not wlan.isconnected():
                print("Waiting to Connect")
                time.sleep(10)
            print("Connected to WiFi")
            break  # Break the loop once connected
        except Exception as e:
            print(e)
            print("Retrying WiFi connection...")
            time.sleep(10)
        else:
            wlan.connect(INTERNET_NAME, INTERNET_PASSWORD)
            

    while wlan.isconnected():
        # Send Modbus frame and receive response
        modbus_handler.send_modbus_frame()
        modbus_handler.receive_modbus_frame()
        modbus_handler.process_registers()
        modbus_handler.normalize_values()
        
        if(wlan.isconnected()):
            try:
                token_balance, lights_state = mongo_handler.get_device_info(DEVICE_ID)
                if token_balance is not None and lights_state is not None:
                    try:
                        token_balance = float(token_balance)
                        lights_state = int(lights_state)
                    except ValueError:
                        print("Error converting token balance to float")
                        token_balance = 0.0
                        lights_state=0
                    
                    if(token_balance>0 and lights_state>0):
                        print("working")
                        relay_controller.activate_relay()
                    
                    else:
                        relay_controller.deactivate_relay()
            except OSError as e:
                if e.errno==errno.ECONNRESET:
                    print("connection reset by peer")
                
                 # Get energy and power from ModbusHandler
        cumulative_energy = str(modbus_handler.energy)
        power = str(modbus_handler.byte_data[3] * 0.1)  # Normalize power value
        # Print the information in an orderly manner
        print("\n----- Device Information -----")
        print("Device ID: ", DEVICE_ID)
        print("Token Balance: ", token_balance)
        print("State of Lights: ", lights_state)
        print("Cumulative Energy: ", cumulative_energy)
        print("Power: ", power)
        print("-------------------------------\n")
        


        # Update energy and power to MongoDB
        mongo_handler.update_device_info(DEVICE_ID, cumulative_energy, power)
    


if __name__ == "__main__":
    main()


