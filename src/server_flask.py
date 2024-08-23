from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Variáveis para armazenar os valores dos inputs
kp = 0
kd = 0
ki = 0
tau = 0.0
qsi = 0.0
tempo = 0.0
modo_operacao = "continua"
valor_corrigido = 0

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
    tempo = request.json.get('tempo')
    tau = request.json.get('tau')
    qsi = request.json.get('qsi')
    return jsonify({
        'status': 'ok',
        'modo': modo_operacao,
        'tempo': tempo,
        'tau': tau,
        'qsi': qsi,
        'kp': kp,
        'kd': kd,
        'ki': ki
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
