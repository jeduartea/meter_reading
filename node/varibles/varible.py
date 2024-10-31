import time
import serial


class Varible: 
    def __init__(self, name, code, measurement_unit, reading_frequency):
        self.name = name
        self.code = code
        self.measurement_unit = measurement_unit
        self.reading_frequency = reading_frequency
        self.value = "N/A"
        self.timestamp = ""
    
    def get_last_vaule(self, chip) -> None:

        serial_port = serial.Serial(port="/dev/ttyS1", baudrate=230400, timeout=0.1)
        msg = f'{{"chip":"{chip}", "operation":"{self.code}"}}'
        serial_port.write(msg.encode())
        time.sleep(0.2)

        if serial_port.in_waiting > 0:  # Check if data is available
            self.value = serial_port.readline().decode().strip()  # Read and decode the answer
        else:
            self.value = "N/A"  # If there is no response, assign a default value

        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # add time to timestamp
    
        serial_port.close()