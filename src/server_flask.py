import io
import base64
from flask import Flask, jsonify, render_template, request
from scipy import signal
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import serial

app = Flask(__name__)

# Variáveis para armazenar os valores dos inputs
kp = 0
kd = 0
ki = 0
tau = 0.0
qsi = 0.0
tempo = 0.0
valor_corrigido = 0.0
modo_operacao = "continua"

# Inicializa a conexão serial
ser = serial.Serial('/dev/tty.usbserial-0001', 115200)  # Atualize para a porta correta

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/atualizar-potenciometro', methods=['GET'])
def atualizar_potenciometro():
    global valor_corrigido
    if ser.in_waiting > 0:
        try:
            linha = ser.readline().decode('utf-8').strip()
            valor_corrigido = round((3 * int(linha)) / 4095, 3)
        except ValueError as v:
            print(f"Erro ao atualizar valor: {v}")
    return jsonify({'valor': valor_corrigido})
    

@app.route('/salvar-kp', methods=['POST'])
def salvar_kp():
    global kp
    kp = float(request.json.get('kp'))
    return jsonify({'status': 'ok', 'kp': kp})

@app.route('/salvar-kd', methods=['POST'])
def salvar_kd():
    global kd 
    kd = float(request.json.get('kd'))
    return jsonify({'status': 'ok', 'kd': kd})

@app.route('/salvar-ki', methods=['POST'])
def salvar_ki():
    global ki
    ki = float(request.json.get('ki'))
    return jsonify({'status': 'ok', 'ki': ki})

@app.route('/salvar-valores', methods=['POST'])
def salvar_valores():
    dados = request.json

    try:
    
        tau = float(dados.get('tau', 0.01))  # Valor padrão
        qsi = float(dados.get('qsi', 0.5))  # Valor padrão
        modo = dados.get('modo', 'continuo')
        tipo = dados.get("tipo", "PID")
        num = [kd, kp, ki]
        den = [1/(tau**2), 2*qsi/tau, 1]

        if(modo == "digital"):
            tempo = float(dados.get("tempo"))
            bode_image = transform_bode(numerador=num, denominador=den, tempo=tempo,modo=modo, tipo=tipo)

        else:
            tempo = 0.1
            bode_image = transform_bode(numerador=num, denominador=den, tempo=tempo,modo=modo, tipo=tipo)
        
        return jsonify({"bode_image": bode_image})
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

def transform_bode(numerador: float, denominador: float,  tempo: float, modo: str, tipo: str) -> str:

    if(modo == "digital"):
        sistema = signal.cont2discrete((numerador, denominador), tempo, method='zoh') # Faz a Função de Transferência
        num_d, den_d = sistema[0], sistema[1];
        
        # Calculo da resposta em frequência
        w, mag, fase = signal.dlti(num_d, den_d).bode()
        
    else:
        sistema = signal.TransferFunction(numerador, denominador)

        # Cálculo da resposta em frequência (Bode)
        w, mag, fase = signal.bode(sistema)

    return plote_bode(w, mag, fase,  tipo)

def plote_bode(w, mag, fase, tipo):
    # Cria o gráfico
    fig, ax = plt.subplots(2, 1, figsize=(8, 6))

    # Plota gráfico de magnitude
    ax[0].semilogx(w, mag)
    ax[0].set_title(f'Gráfico de Bode - {tipo.upper()}')
    ax[0].set_xlabel('Frequência [rad/s]')
    ax[0].set_ylabel('Magnitude [dB]')

    # Plota gráfico de fase
    ax[1].semilogx(w, fase)
    ax[1].set_xlabel('Frequência [rad/s]')
    ax[1].set_ylabel('Fase [graus]')

    plt.tight_layout()

    # Salva o gráfico em um buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0) # Posição contigua da memória

    # Converte a imagem para Base64
    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    # Retorna a string Base64
    return image_base64

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
