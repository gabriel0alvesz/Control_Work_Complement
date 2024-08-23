from flask import Flask, request, jsonify, render_template
import socket
from math import log10, atan, pi

app = Flask(__name__)

# Variáveis para armazenar os valores dos inputs
kp = 0
kd = 0
ki = 0
tau = 0.0
qsi = 0.0
tempo = 0.0
modo_operacao = "continua"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/atualizar-potenciometro', methods=['GET'])
def atualizar_potenciometro():
    global valor_corrigido
    return jsonify({'valor': valor_corrigido})

@app.route('/receber-potenciometro', methods=['POST'])
def receber_potenciometro():
    global valor_corrigido
    valor_potenciometro = request.json.get('valor')
    valor_corrigido = round(valor_potenciometro / 4095, 3)
    return jsonify({'status': 'ok', 'valor_recebido': valor_corrigido})

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

@app.route('/salvar-valores', methods=['POST'])
def salvar_valores():
    global kp, kd, ki, tau, qsi, tempo, modo_operacao

    modo_operacao = request.json.get('modo')
    tau = float(request.json.get('tau', 0))  # Converter para float
    qsi = float(request.json.get('qsi', 0))  # Converter para float

    tempo_str = request.json.get('tempo', '')
    if modo_operacao == "continua":
        tempo = 0.01
    elif tempo_str:
        try:
            tempo = float(tempo_str)  # Converter para float se digital
        except ValueError:
            tempo = 0.01  # Defina um valor padrão se a conversão falhar
    else:
        tempo = 0.01  # Defina um valor padrão se o campo estiver vazio

    # Cálculo para gráfico de Bode e resposta ao degrau
    a = [1, qsi + tau, tau * qsi]  # Agora qsi e tau são floats
    b = [1, 0]  # Exemplo simplificado para Bode
    frequencias = [0.1, 1, 10, 100]  # Exemplo de frequências
    magnitude = [20 * log10(abs(1 / (tau * f))) for f in frequencias]
    fase = [-atan(tau * f) * 180 / pi for f in frequencias]

    tempo_degrau = [0, 1, 2, 3, 4]  # Exemplo de tempo
    resposta_degrau = [0, 1, 1.5, 1.8, 2]  # Exemplo de resposta ao degrau

    return jsonify({
        'kp': kp,
        'kd': kd,
        'ki': ki,
        'bode': {'frequencias': frequencias, 'magnitude': magnitude, 'fase': fase},
        'degrau': {'tempo': tempo_degrau, 'resposta': resposta_degrau}
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
