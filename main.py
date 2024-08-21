import socket

# Configurações do servidor
host = '0.0.0.0'  # Escuta em todas as interfaces de rede
port = 3333       # Porta para escutar

# Criar o socket TCP/IP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Associar o socket ao endereço e porta
server_socket.bind((host, port))

# Escutar por conexões
server_socket.listen(1)
print(f'Servidor escutando em {host}:{port}')

while True:
    try:
        # Aceitar uma nova conexão
        client_socket, client_address = server_socket.accept()
        print(f'Conexão recebida de {client_address}')

        while True:
            # Receber os dados do ESP32
            data = client_socket.recv(1024).decode('utf-8')
            if not data:
                break

            # Exibir os dados recebidos
            print(f'Dados recebidos: {data}')

        # Fechar a conexão
        client_socket.close()
        print("Conexão encerrada.")

    except KeyboardInterrupt:
        print("Servidor encerrado pelo usuário.")
        break

# Fechar o socket do servidor
server_socket.close()
