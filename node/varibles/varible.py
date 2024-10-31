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

        serial_port = serial.Serial(port="/dev/ttyS1", baudrate=230400, timeout=1)
        msg = f'{{"chip" : "{chip}", "operation" : "{self.code}"}}'+"\r\n"
        print(f"Enviando mensaje: {msg}")
        serial_port.write(msg.encode())
        time.sleep(0.2)

        if serial_port.in_waiting > 0:  # Check if data is available
            self.value = serial_port.readline().decode().strip()  # Read and decode the answer
        else:
            self.value = "N/A"  # If there is no response, assign a default value

        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) # add time to timestamp
    
        serial_port.close()

# Prueba de conexión al ejecutar el script de forma individual
if __name__ == "__main__":
    # Crear una instancia de Varible para la fase A del voltaje
    voltage_var = Varible(name="Voltage Phase A", code="getVoltageA", measurement_unit="V", reading_frequency=0.0082)
    
    # Ejecutar el método get_last_value para obtener el voltaje de la fase A en el chip 1
    voltage_var.get_last_vaule(chip="1")
    
    # Mostrar el resultado de la prueba de conexión
    print(f"Prueba de conexión para Chip 1 - Voltaje Fase A:")
    print(f"Valor obtenido: {voltage_var.value} {voltage_var.measurement_unit}")
    print(f"Timestamp de la lectura: {voltage_var.timestamp}")
