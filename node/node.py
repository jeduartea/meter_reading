import os
import time
import csv
from node.devices import Device

class Node:
    
    def __init__(self, name, location, current_dir, names_conf_device_files) -> None:
        self.name = name
        self.location = location
        self.current_dir = current_dir
        self.names_conf_device_files = names_conf_device_files
        self.devices = {}
    
        self.add_devices(names_conf_device_files)

    def add_devices(self, names_conf_device_files) -> None:
        for name_device in names_conf_device_files:
            file_path = os.path.join(self.current_dir, "node","conf_files", name_device)
            read_device = Device(file_path)
            self.devices[str(name_device[:-5])] = read_device
    
    def read_and_get_all_varibles_values(self) -> list:
        result_list_devices = []
        for device_key in self.devices.keys():
            self.devices[device_key].read_all_varibles()
            device_result = self.devices[device_key].get_all_varibles_values()
            result_list_devices.append(device_result)
        return result_list_devices
    
    def add_all_values_to_csv(self, n_rows, output_folder) -> None:
        # Generar el timestamp actual
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        
        # Obtener los valores actuales de las variables para cada dispositivo
        all_data = self.read_and_get_all_varibles_values()
        
        for device_data in all_data:
            device_name = device_data["name"]

            # Obtener el nombre de las variables para el encabezado
            variable_names = [var["name"] for var in device_data["varibles"]]
            headers = ["timestamp"] + variable_names

            # Encontrar el último archivo CSV para el dispositivo y determinar el número más alto
            csv_files = [f for f in os.listdir(output_folder) if f.startswith(f"{device_name}_") and f.endswith('.csv')]
            max_number = max([int(f[len(device_name) + 1:-4]) for f in csv_files], default=0)
            current_file = os.path.join(output_folder, f"{device_name}_{max_number}.csv") if max_number > 0 else os.path.join(output_folder, f"{device_name}_1.csv")
            
            # Contar filas en el archivo actual o crear uno nuevo si está vacío o lleno
            if os.path.exists(current_file):
                with open(current_file, 'r') as csvfile:
                    reader = csv.reader(csvfile)
                    row_count = sum(1 for row in reader)
            else:
                row_count = 0

            # Crear un nuevo archivo si el actual alcanza el límite de filas
            if row_count >= n_rows:
                current_file = os.path.join(output_folder, f"{device_name}_{max_number + 1}.csv")
            
            # Escribir datos en el archivo CSV
            with open(current_file, 'a', newline='') as csvfile:
                writer = csv.writer(csvfile)
                
                # Escribir el encabezado si el archivo está vacío
                if row_count == 0:
                    writer.writerow(headers)
                
                # Agregar la fila con el timestamp y los valores de las variables
                row = [timestamp]
                for var in device_data["varibles"]:
                    row.append(var["value"])
                writer.writerow(row)

