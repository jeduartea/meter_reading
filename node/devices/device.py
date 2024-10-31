import json
import time
from node.varibles import Varible

class Device:

    def __init__(self, file_conf_path) -> None:
        self.name = ""
        self.status = ""
        self.description = ""
        self.chip = ""
        self.varibles = {} # Dict of Variable objects

        self.get_config_parametres(file_conf_path)

    def get_config_parametres(self, file_conf_path) -> None:
        # Open and load the configuration JSON file
        with open(file_conf_path, 'r') as file:
            config = json.load(file)
        
        # Assign configuration values ​​to the device
        self.name = config.get("name", "")
        self.status = config.get("status", "")
        self.description = config.get("description", "")
        self.chip = config.get("chip", "")
        
        # Process each variable in the JSON variable list
        for var in config.get("variables", []):
            # Create a Variable instance with the data of each variable
            variable = Varible(
                name=var.get("name", ""),
                code=var.get("code", ""),
                measurement_unit=var.get("measurement_unit", ""),
                reading_frequency=var.get("reading_frequency", 0.0082)
            )
            # Add the variable to the device variable list
            self.varibles[var.get("code", "")] = variable


    def read_all_varibles(self) -> None:

        for varible_key in self.varibles.keys():
            self.varibles[varible_key].get_last_vaule(self.chip)
            time.sleep(0.1)
        

    def get_all_varibles_values(self) -> dict:
        # Build the dictionary in the requested format
        result = {
            "name": self.name,
            "status": self.status,
            "varibles": []
        }
        
        for variable in self.varibles.values():
            # Append each variable's details as a dictionary
            result["varibles"].append({
                "name": variable.name,
                "code": variable.code,
                "measurement_unit": variable.measurement_unit,
                "value": variable.value,
                "timestamp": variable.timestamp
            })
        
        return result