from flask import Flask, request, jsonify
import threading
import serial  # Adiciona a biblioteca pySerial
import time
from flask_cors import CORS
import control_functions as cf

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})


# ser = serial.Serial('/dev/tty.usbserial-0001', 115200)

# # Variáveis globais para armazenar os dados recebidos da serial
# serial_data = {}

# def ler_dados_serial():
    
#     global serial_data
#     while True:
#         if ser.in_waiting > 0:
#             try:
                
#                 linha_serial = ser.readline().decode('utf-8').strip()
                

#             except Exception as e:
#                 print(f"Erro ao ler dados da serial: {e}")
#         time.sleep(0.1)  # evita sobrecarregar a CPU

# threading.Thread(target=ler_dados_serial, daemon=True).start()

# # Rota para o front-end obter os dados seriais
# @app.route('/api/serial-data', methods=['GET'])
# def get_serial_data():
#     """
#     Retorna os dados mais recentes recebidos da porta serial.
#     """
#     if serial_data:
#         return jsonify(serial_data)
#     else:
#         return jsonify({'error': 'Nenhum dado recebido ainda'}), 400


# Rota para o sistema contínuo
@app.route('/api/continuo', methods=['POST'])
def sistema_continuo():
    dados = request.json
    print(f'Recebendo dados do sistema contínuo: {dados}')

    K = float(dados['K'])
    Kp = float(dados['Kp'])
    Ki = float(dados['Ki'])
    Kd = float(dados['Kd'])
    tau = float(dados['TAU'])
    tipo = str(dados['tipo'])

    sistema = cf.firstOrder(K=K, tau=tau, T=None)
    controle = cf.controler(Kp, Ki, Kd, tipo, None)
    malha_aberta = cf.make_open_loop(sistema, controle)
    malha_fechada = cf.make_closed_loop(malha_aberta)

    t_degrau, resposta = cf.make_step_response(malha_fechada)

    imagem_bode = cf.plote_Bode(open_loop=malha_aberta, modo="Continuo", tipo=tipo)
    imagem_degrau = cf.plote_resposta_degrau(time=t_degrau, response=resposta, modo="Continuo", tipo=tipo)
    imagem_lgr = cf.plote_LGR(open_loop=malha_aberta, modo="Continuo", tipo=tipo, plot_circle=False)

    imagens = {
        'bode_image': imagem_bode,
        'step_image': imagem_degrau,
        'lgr_image': imagem_lgr
    }

    return jsonify(imagens)



# Rota para o sistema discreto
@app.route('/api/discreto', methods=['POST'])
def sistema_discreto():
    dados = request.json
    print(f'Recebendo dados do sistema discreto: {dados}')
    
    K = float(dados['K'])
    Kp = float(dados['Kp'])
    Ki = float(dados['Ki'])
    Kd = float(dados['Kd'])
    tau = float(dados['TAU'])
    tipo = str(dados['tipo'])
    amostragem = float(dados['tempoAmostragem'])

    sistema = cf.firstOrder(K=K, tau=tau, T=amostragem)

    controle = cf.controler(Kp=Kp, Ki=Ki, Kd=Kd, type_control=tipo, T=amostragem)
    malha_aberta = cf.make_open_loop(sistema, controle)
    malha_fechada = cf.make_closed_loop(sistema)

    t_degrau, resposta = cf.make_step_response(malha_fechada)

    imagem_bode = cf.plote_Bode(open_loop=malha_aberta, modo="Discreto", tipo=tipo)
    imagem_degrau = cf.plote_resposta_degrau(time=t_degrau, response=resposta, modo="Discreto", tipo=tipo)
    imagem_lgr = cf.plote_LGR(open_loop=malha_aberta, modo="Discreto", tipo=tipo, plot_circle=True)

    imagens = {
        'bode_image': imagem_bode,
        'step_image': imagem_degrau,
        'lgr_image': imagem_lgr
    }

    return jsonify(imagens)

if __name__ == '__main__':
    app.run(port=5000, debug=True)
