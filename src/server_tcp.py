import socket
import threading

esp32_host = '0.0.0.0'
esp32_port = 3333

def handle_client(client_socket):
    try:
        data = client_socket.recv(1024).decode('utf-8')
        if data:
            print(f'Dado recebido: {data}')
            client_socket.sendall(b'Recebido com sucesso\n')
    except Exception as e:
        print(f'Erro: {e}')
    finally:
        client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((esp32_host, esp32_port))
    server.listen(5)
    print(f'Servidor escutando em {esp32_host}:{esp32_port}')

    while True:
        client_socket, addr = server.accept()
        print(f'Conexão recebida de {addr}')
        client_handler = threading.Thread(target=handle_client, args=(client_socket,))
        client_handler.start()

if __name__ == '__main__':
    start_server()
