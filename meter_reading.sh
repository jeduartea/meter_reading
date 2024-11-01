#!/bin/bash

echo "Iniciando script meter_reading.sh..."

# Ruta del archivo de configuración
CONFIG_FILE="/root/UsbFolder/meter_reading/meter_reading_running.txt"
echo "Archivo de configuración: $CONFIG_FILE"

# Ruta del archivo Python
PYTHON_SCRIPT="main_meter_reading.py"
PYTHON_PATH="/root/UsbFolder/meter_reading/$PYTHON_SCRIPT"
echo "Archivo de script Python: $PYTHON_PATH"

# Ruta del intérprete de Python. verificar which python3, chmod +x meter_reading.sh
PYTHON_INTERPRETER="/usr/bin/python3"

# Leer la primera línea del archivo de configuración
if [ -f "$CONFIG_FILE" ]; then
    RUNNING_STATUS=$(head -n 1 "$CONFIG_FILE")
    echo "RUNNING_STATUS: $RUNNING_STATUS"
else
    echo "Archivo $CONFIG_FILE no encontrado."
    exit 1
fi

# Verificar el estado de ejecución basado en el contenido del archivo
if [ "$RUNNING_STATUS" = "1" ]; then
    # Si RUNNING_STATUS es "1", iniciar el proceso si no está ya en ejecución
    echo "Verificando si el proceso ya está en ejecución..."
    start-stop-daemon -K -x "$PYTHON_INTERPRETER" -a "$PYTHON_PATH" >/dev/null 2>&1
    echo "Iniciando $PYTHON_SCRIPT..."
    start-stop-daemon -b -S -x "$PYTHON_INTERPRETER" -- "$PYTHON_PATH" >> /root/UsbFolder/meter_reading/log.log 2>&1
    echo "Proceso $PYTHON_SCRIPT iniciado."
else
    # Si RUNNING_STATUS no es "1", detener el proceso si está en ejecución
    echo "Deteniendo $PYTHON_SCRIPT si está en ejecución..."
    start-stop-daemon -K -x "$PYTHON_INTERPRETER" -a "$PYTHON_PATH"
    echo "Proceso $PYTHON_SCRIPT detenido si estaba en ejecución."
fi

echo "Script meter_reading.sh terminado."
