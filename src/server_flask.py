from flask import Flask, request, jsonify, render_template
import socket

app = Flask(__name__)

# Variáveis para armazenar os valores dos inputs
kp = 0
kd = 0
ki = 0
tempo = 0.0
valor_potenciometro = 0  

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/atualizar-potenciometro', methods=['GET'])
def atualizar_potenciometro():
    global valor_potenciometro
    return jsonify({'valor': valor_potenciometro})

@app.route('/receber-potenciometro', methods=['POST'])
def receber_potenciometro():
    global valor_potenciometro
    valor_potenciometro = request.json.get('valor')
    return jsonify({'status': 'ok', 'valor_recebido': valor_potenciometro})

@app.route('/salvar-kp', methods=['POST'])
def salvar_kp():
    global kp
    kp = request.json.get('valor')
    return jsonify({'status': 'ok', 'kp': kp})

@app.route('/salvar-kd', methods=['POST'])
def salvar_kd():
    global kd
    kd = request.json.get('valor')
    return jsonify({'status': 'ok', 'kd': kd})

@app.route('/salvar-ki', methods=['POST'])
def salvar_ki():
    global ki
    ki = request.json.get('valor')
    return jsonify({'status': 'ok', 'ki': ki})

@app.route('/enviar-valores', methods=['POST'])
def enviar_valores():
    global kp, kd, ki, tempo
    tempo = request.json.get('tempo')

    # Configurações do servidor TCP 
    tcp_server_host = '127.0.0.1'
    tcp_server_port = 3333

    # Conectar ao servidor TCP e enviar os valores
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((tcp_server_host, tcp_server_port))
        message = f"Kp: {kp}, Kd: {kd}, Ki: {ki}, Tempo: {tempo}\n"
        s.sendall(message.encode('utf-8'))
        data = s.recv(1024).decode('utf-8')

    return jsonify({'mensagem': 'Valores enviados com sucesso!', 'resposta': data})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
