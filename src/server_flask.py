from flask import Flask, jsonify, render_template, request
from scipy import signal
import numpy as np
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
            # print(valor_corrigido)
        except ValueError:
            pass
        
    return jsonify({'valor': valor_corrigido})

# def ler_dados_serial():
    

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
    dados = request.json

    try:
        kp = float(dados.get('kp', 0))
        kd = float(dados.get('kd', 0))
        ki = float(dados.get('ki', 0))
        tau = float(dados.get('tau', 0.01))  # Valor padrão
        qsi = float(dados.get('qsi', 0.5))  # Valor padrão
        modo = dados.get('modo', 'continua')

        # Verificar tempo de amostragem
        if modo == 'digital':
            try:
                tempo = float(dados.get('tempo', 0.1))
            except ValueError:
                tempo = 0.1
        else:
            tempo = 0.01  # Tempo de amostragem padrão para contínuo

        # Numerador e denominador para a função de transferência G(s)
        num = [kd, kp, ki]
        den = [1/(tau**2), 2*qsi/tau, 1]

        if modo == 'digital':
            # Discretizar o sistema para modo digital
            sistema = signal.cont2discrete((num, den), tempo, method='zoh')
            num_d, den_d = sistema[0], sistema[1]
            sistema_discreto = signal.dlti(num_d, den_d)
            
            # Cálculo da resposta em frequência (Bode) para sistema digital
            w, mag, fase = signal.dlti(num_d, den_d).bode()
            
            # Cálculo da resposta ao degrau
            t, yout = signal.dstep(sistema_discreto)
            t = np.array(t).flatten()
            yout = np.array(yout).flatten()

            # Cálculo do Lugar das Raízes (LDR) para sistema digital
            k = np.linspace(0, 10, num=500)
            rlist = []
            for k_val in k:
                num_k = [x * k_val for x in num_d]
                sistema_k = signal.dlti(num_k, den_d)
                poles = np.roots(sistema_k.den)
                rlist.append(poles.real.tolist())  # Converta para lista

            dados_bode = {'frequencia': w.tolist(), 'magnitude': mag.tolist(), 'fase': fase.tolist()}
            dados_ldr = {'raizes': rlist, 'ganhos': k.tolist()}

        else:
            # Sistema contínuo
            sistema = signal.TransferFunction(num, den)
            
            # Cálculo da resposta em frequência (Bode)
            w, mag, fase = signal.bode(sistema)
            
            # Cálculo da resposta ao degrau
            t, yout = signal.step(sistema)

            # Cálculo do Lugar das Raízes (LDR)
            k = np.linspace(0, 10, num=100)
            rlist = []
            for k_val in k:
                num_k = [x * k_val for x in num]
                sistema_k = signal.TransferFunction(num_k, den)
                poles = np.roots(sistema_k.den)
                rlist.append(poles.real.tolist())  # Converta para lista

            dados_bode = {'frequencia': w.tolist(), 'magnitude': mag.tolist(), 'fase': fase.tolist()}
            dados_degrau = {'tempo': t.tolist(), 'resposta': yout.tolist()}
            dados_ldr = {'raizes': rlist, 'ganhos': k.tolist()}

        dados_degrau = {'tempo': t.tolist(), 'resposta': yout.tolist()}

        return jsonify({'bode': dados_bode, 'degrau': dados_degrau, 'ldr': dados_ldr})
    
    except Exception as e:
        return jsonify({'erro': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
