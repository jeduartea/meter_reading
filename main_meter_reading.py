
from datetime import datetime
from time import sleep
import logging
import os

from node import Node


def setup_logging(log_file):
    logging.basicConfig(filename=log_file,
                        filemode='w',
                        format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)


def check_running_status(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.readline().strip()
            return content == "1"  # Devuelve True si el contenido es "1", False en caso contrario
    except FileNotFoundError:
        logging.warning(f"File {file_path} not found. Ending program.")
        return False
       
if "__main__" == __name__:

    current_file_path = os.path.abspath(__file__)
    current_dir = os.path.dirname(current_file_path)
    log_file = os.path.join(current_dir, "node", "output", "logs", "main.log")
    output_folder = os.path.join(current_dir, "node", "output","csv_files")
    status_file = os.path.join(current_dir, "meter_reading_running.txt")
    setup_logging(log_file)

    start_time = datetime.now()
    logging.info(f"MAIN FUNCTION START")
    logging.info(f"start at: {start_time}")

    try:
        logging.info(f"Node building ....")
        node_home = Node("Home_node", "Bogotá", current_dir, ["eGEO_1.json", "eGEO_2.json"])
        logging.info(f"Node built")

        logging.info(f"Start reading and saving ...")

        running_status = check_running_status(status_file)

        while running_status:
            Node.add_all_values_to_csv(n_rows=500, output_folder=output_folder)
            sleep(60)
            running_status = check_running_status(status_file)  # Verifica nuevamente el archivo después de cada iteración

        logging.info(f"Ending Function running_status is False")
        end_time = datetime.now()
        logging.info(f"Program end at: {end_time}")
        logging.info(f'Main function executed successfully. Program duration: {end_time - start_time}')
        logging.info(f"MAIN FUNCTION END")
        logging.shutdown()

    except Exception as error:
        logging.error(f"{error}")