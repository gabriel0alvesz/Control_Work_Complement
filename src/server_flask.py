import io
import base64
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import control as ctrl
import serial
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# valores dos inputs
kp = 0
kd = 0
ki = 0
tau = 0.0
tempo = 0.0
valor_corrigido = 0.0
modo_operacao = "continua"
epsilon = 1e-10

ser = serial.Serial('/dev/tty.usbserial-0001', 115200)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/atualizar-potenciometro', methods=['GET'])
def atualizar_potenciometro():
    global valor_corrigido
    if ser.in_waiting > 0:
        try:
            linha = ser.readline().decode('utf-8').strip()
            valor_corrigido = round((10 * int(linha)) / 4095, 3)
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
        tau = float(dados.get('tau', 0.01))  
        modo = dados.get('modo', 'continuo')
        tipo = dados.get("tipo", "PID")
        tempo = float(dados.get("tempo"))
        
        # Função de transferência contínua G(s) = (Kp + Ki/s + Kd*s) / (1 + tau*s)

        if(tipo == "PID"):
            num = [kp, ki, kd]
        elif(tipo == "PD"):
            num = [kp, 0, kd]
        elif(tipo == "PI"):
            num = [kp, ki, 0]

        den = [epsilon, tau, 1]

        sistema_geral = ctrl.TransferFunction(num, den) # Cria o sistema padrão

        if(modo == "digital"):
            sistema_discreto = ctrl.sample_system(sistema_geral, tempo, method="zoh")
           
            bode_image = transform_bode(sistema=sistema_discreto, modo=modo, tipo=tipo)
            degrau_image = transform_degrau(sistema=sistema_discreto, modo=modo, tipo=tipo)
            lgr_image = transform_lgr(sistema=sistema_discreto, modo=modo, tipo=tipo)
        else:
            bode_image = transform_bode(sistema=sistema_geral, modo=modo, tipo=tipo)
            degrau_image = transform_degrau(sistema=sistema_geral, modo=modo, tipo=tipo)
            lgr_image = transform_lgr(sistema=sistema_geral, modo=modo, tipo=tipo)
        
        return jsonify({
            "tau": tau, 
            "modo": modo,
            "tempo": tempo, 
            "tipo": tipo,
            "Ks": [kp, ki, kd], 
            "bode_image": bode_image,
            "degrau_image": degrau_image,
            "lgr_image": lgr_image
        })
    
    except Exception as e:
        print(str(e))
        return jsonify({'erro': str(e)}), 500

def transform_bode(sistema, modo: str, tipo: str) -> str:
     
    plt.figure()
    ctrl.bode(sistema, dB=True)
    plt.suptitle(f"Diagrama de Bode - Modo: {modo.upper()} - {tipo}", fontsize=12)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64

def transform_degrau(sistema, modo: str, tipo: str) -> str:
    
    t, y = ctrl.step_response(sistema)
    
    plt.figure()
    plt.plot(t, y)
    plt.title(f"Resposta ao Degrau - Modo: {modo.upper()} - {tipo}", fontsize=12)
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)
    
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64

def transform_lgr(sistema, modo: str, tipo: str) -> str:
    
    plt.figure()

    ctrl.root_locus(sistema, plot=True)

    plt.title(f"Lugar das Raízes (LGR) - Modo: {modo.upper()} - {tipo}", fontsize=12)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=4000)
