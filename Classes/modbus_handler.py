# classes/modbus_handler.py
import machine

class ModbusHandler:
    def __init__(self, uart_num, baudrate, tx_pin, rx_pin):
        self.uart = machine.UART(uart_num, baudrate=baudrate, tx=tx_pin, rx=rx_pin)
        self.byte_array = bytearray(250)
        self.byte_data = [0] * 20
        self.energy = 0

    def send_modbus_frame(self):
        msg = bytes([0x01, 0x04, 0x00, 0x00, 0x00, 0x0A, 0x70, 0x0D])

        #print("SENDING DATA - SEND DATA")
        for i in range(len(msg)):
            self.uart.write(msg[i:i+1])
            #print("[{}] = {}".format(i, hex(msg[i])))
        #print()

    def receive_modbus_frame(self):
        a = 0
        #print("DATA RECEPTION - RECEPCIÓN DATOS")
        while self.uart.any():
            self.byte_array[a] = ord(self.uart.read(1))
            a += 1

        #for b in range(a):
            #print("[{}] = {}".format(b, hex(self.byte_array[b])), end=' ')
        #print("\n")
            
    def process_registers(self):
        #print("REGISTERS HEX")

        self.byte_data[0] = self.byte_array[3] * 256 + self.byte_array[4]
        #print(self.byte_data[0])

        self.byte_data[1] = self.byte_array[5] * 256 + self.byte_array[6]
        #print(self.byte_data[1])

        self.byte_data[3] = self.byte_array[9] * 256 + self.byte_array[10]
        #print(self.byte_data[3])

        self.byte_data[5] = self.byte_array[13] * 256 + self.byte_array[14]
        #print(self.byte_data[5])

        self.byte_data[7] = self.byte_array[17] * 256 + self.byte_array[18]
        #print(self.byte_data[7])

        self.byte_data[8] = self.byte_array[19] * 256 + self.byte_array[20]
        #print(self.byte_data[8])

        self.energy = self.byte_data[5]

    def normalize_values(self):
        print("MEASUREMENTS")

        voltage = self.byte_data[0] * 0.1
        current = self.byte_data[1] * 0.001
        power = self.byte_data[3] * 0.1
        frequency = self.byte_data[7] * 0.1
        power_factor = self.byte_data[8] * 0.01

        print("Voltage: {}".format(voltage))
        print("Current: {}".format(current))
        print("Power: {}".format(power))
        print("Energy: {}".format(self.energy))
        print("Frequency: {}".format(frequency))
        print("Power Factor: {}".format(power_factor))
        print()
