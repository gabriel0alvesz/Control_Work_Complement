import threading
import serial
import time
import json  # Use json para evitar problemas de segurança com eval

ser = serial.Serial('/dev/tty.usbserial-0001', 115200)  # Use o caminho correto para sua porta serial

# Variáveis globais para armazenar os dados recebidos da serial
serial_data = {}

def ler_dados_serial():
    global serial_data
    while True:
        if ser.in_waiting > 0:
            try:
                linha_serial = ser.readline().decode('utf-8').strip()
                print(f'\n\n{linha_serial}\n\n')
            except Exception as e:
                print(f"Erro ao ler dados da serial: {e}")
        time.sleep(0.1)  # Evita sobrecarregar a CPU

if __name__ == '__main__':
    # Inicie a thread e execute a leitura dos dados da serial
    serial_thread = threading.Thread(target=ler_dados_serial, daemon=True)
    serial_thread.start()

    # Manter o main thread viva para que a thread daemon continue a executar
    try:
        while True:
            time.sleep(0.1)
    except KeyboardInterrupt:
        print("Encerrando...")
