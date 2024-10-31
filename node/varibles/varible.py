import time
import serial
import json


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
        serial_port.write(msg.encode('utf8'))
        time.sleep(0.5)


        while not serial_port.inWaiting():
            time.sleep(0.1)
            
        if serial_port.inWaiting():
                recibidoSerial = serial_port.readline()
                data = json.loads(recibidoSerial)
                response = data["value"]
                print("recibido:", response)
        
        self.value = response if response else "N/A"
        self.timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
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
