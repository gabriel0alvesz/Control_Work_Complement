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
    # Aceitar uma nova conexão
    client_socket, client_address = server_socket.accept()
    print(f'Conexão recebida de {client_address}')

    # Receber a mensagem do cliente (ESP32)
    data = client_socket.recv(1024).decode('utf-8')
    if data:
        print(f'Mensagem recebida: {data}')
        # Enviar uma resposta ao ESP32 (opcional)
        client_socket.sendall(b'Recebido com sucesso\n')

    # Fechar a conexão
    client_socket.close()
