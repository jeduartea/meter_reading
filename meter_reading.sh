#!/bin/bash

echo "Iniciando script meter_reading.sh..."

# Ruta del archivo de configuración
CONFIG_FILE="meter_reading_running.txt"
echo "Archivo de configuración: $CONFIG_FILE"

# Ruta del archivo Python
PYTHON_SCRIPT="main_meter_reading.py"
echo "Archivo de script Python: $PYTHON_SCRIPT"

# Función para verificar si el proceso está en ejecución
is_process_running() {
    pgrep -f "$PYTHON_SCRIPT" > /dev/null 2>&1
}

# Leer la primera línea del archivo de configuración
if [[ -f "$CONFIG_FILE" ]]; then
    RUNNING_STATUS=$(head -n 1 "$CONFIG_FILE")
    echo "RUNNING_STATUS: $RUNNING_STATUS"
else
    echo "Archivo $CONFIG_FILE no encontrado."
    exit 1
fi

# Verificar el estado de ejecución basado en el contenido del archivo
if [[ "$RUNNING_STATUS" == "1" ]]; then
    # Si RUNNING_STATUS es "1", verificar si el proceso ya está corriendo
    if is_process_running; then
        echo "El proceso $PYTHON_SCRIPT ya está en ejecución."
    else
        echo "Iniciando $PYTHON_SCRIPT..."
        python3 "$PYTHON_SCRIPT" &
    fi
else
    # Si RUNNING_STATUS no es "1", verificar si el proceso está corriendo y terminarlo
    if is_process_running; then
        echo "Deteniendo $PYTHON_SCRIPT..."
        pkill -f "$PYTHON_SCRIPT"
    else
        echo "No hay ningún proceso $PYTHON_SCRIPT en ejecución para detener."
    fi
fi

echo "Script meter_reading.sh terminado."
