import io
import base64
import matplotlib
matplotlib.use('Agg')
import control as ctrl 
import matplotlib.pyplot as plt
import math as m
import numpy as np


def controler(Kp = 1, Ki = 0, Kd = 0, type_control = 'P', T = None): 
    if type_control == 'P':
        control = ctrl.TransferFunction([Kp], [1], T)
    elif type_control == 'PI':
        if T is None:
            control = ctrl.TransferFunction([Kp, Ki], [1, 0])
        else:
            T = float(T)
            p = ctrl.TransferFunction([Kp], [1], T)
            i = ctrl.TransferFunction([Ki*T, Ki*T], [2, -2], T)
            control = ctrl.parallel(p, i)
    elif type_control == 'PD':
        if T is None:
            control = ctrl.TransferFunction([Kd, Kp], [1])
        else:
            T = float(T)
            p = ctrl.TransferFunction([Kp], [1], T)
            d = ctrl.TransferFunction([Kd, -Kd], [T, 0], T)
            control = ctrl.parallel(p, d)
    elif type_control == 'PID':
        if T is None:
            control = ctrl.TransferFunction([Kd, Kp, Ki], [1, 0])
        else:
            T = float(T)
            p = ctrl.TransferFunction([Kp], [1], T)
            i = ctrl.TransferFunction([Ki*T, Ki*T], [2, -2], T)
            d = ctrl.TransferFunction([Kd, -Kd], [T, 0], T)
            control = ctrl.parallel(p, i, d)
    
    return control
    

def discretiza_controle(control, tempo):
    return ctrl.sample_system(control, tempo, method='zoh')


def firstOrder(K=1, tau=1, T=None):
    system = ctrl.TransferFunction([K], [tau, 1]) # Funcao canonica de 1 ordem
    if T is not None: 
        T = float(T)
        system = ctrl.sample_system(system, T, method='zoh')
    return system

def clean_transfer_function(tf_str): # feita para plotar as funcoes
    
    lines = str(tf_str).splitlines()
    
    cleaned_lines = [line.strip() for line in lines if line.strip() and not (
        line.startswith("Inputs") or line.startswith("Outputs") or 
        line.startswith("<") or line.startswith("dt"))]
    
    numerador = cleaned_lines[0]
    denominador = cleaned_lines[2]
    
    return numerador, denominador

def plote_resposta_degrau(time: list, response: list, modo: str, tipo: str) -> str:
    plt.figure()
    plt.plot(time, response)
    plt.title(f'Resposta ao Degrau')
    plt.suptitle(f"Tempo {modo.upper()} e Controle {tipo}")
    plt.xlabel('Tempo (s)')
    plt.ylabel('Amplitude')
    plt.grid(True)

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64

def plote_LGR(open_loop, modo: str, tipo: str, plot_circle=True) -> None:
    
    is_discrete = ctrl.isdtime(open_loop, strict=True) # verifica se é discreto
    
    # Obtendo polos e zeros do sistema em malha aberta
    pzmap = ctrl.pzmap(open_loop, plot=False)
    if isinstance(pzmap, tuple) and len(pzmap) == 2:
        poles, zeros = pzmap
    else:
        poles = []
        zeros = []
        print("Unexpected pzmap return format")

    # polos e raizes (real e imaginario)
    root_locus = {
        'poles': [(p.real, p.imag) for p in poles],
        'zeros': [(z.real, z.imag) for z in zeros]
    }

    # somente se o sistema for discreto e plot_circle for verdadeuro
    if plot_circle and is_discrete:
        theta = np.linspace(0, 2 * np.pi, 361)
        unit_circle_x = np.cos(theta)
        unit_circle_y = np.sin(theta)

    plt.figure()
    plt.scatter([p.real for p in poles], [p.imag for p in poles], color='r', marker='x', label='Polos') # Plota polos (x vermelhos)
    plt.scatter([z.real for z in zeros], [z.imag for z in zeros], color='b', marker='o', label='Zeros') # Plota zeros (o azuis)

    # Plota o círculo unitário se for sistema discreto
    if plot_circle and is_discrete:
        plt.plot(unit_circle_x, unit_circle_y, 'g--', label='Círculo unitário')

    # Adiciona linhas de referência e detalhes
    plt.axhline(0, color='k', linestyle='--', linewidth=1)
    plt.axvline(0, color='k', linestyle='--', linewidth=1)
    
    plt.title('Gráfico Lugar das Raízes (LGR)')
    plt.suptitle(f"Tempo {modo.upper()} e Controle {tipo}")
    plt.xlabel('Parte Real')
    plt.ylabel('Parte Imaginária')
    plt.grid(True)
    # plt.legend()

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64

def plote_Bode(open_loop, modo: str, tipo: str):
    """
    Função para plotar o gráfico de Bode (magnitude e fase).
    
    Parâmetros:
    - open_loop: sistema de malha aberta (função de transferência).
    """
    
    mag, phase, omega = ctrl.bode(open_loop, plot=False)
    phase_degrees = [m.degrees(phase_i) for phase_i in phase]# Converter fase para graus
    magnitude_db = [20 * np.log10(val) if val > 0 else -np.inf for val in mag]  # Evitar log(0) e converte magnitude para decibéis (dB)
    
    # Preparar os dados para plotagem
    bode = {
        'magnitude': magnitude_db,  # y: magnitude (em dB)
        'phase': phase_degrees,     # y: fase (em graus)
        'frequency': omega          # x: frequência (em rad/s)
    }
    
    plt.figure()
    # Gráfico de Magnitude (em dB)
    plt.subplot(2, 1, 1)  # 2 linhas, 1 coluna, 1ª posição
    plt.semilogx(bode['frequency'], bode['magnitude'], 'b')
    plt.title('Gráfico de Bode')
    plt.suptitle(f"Tempo {modo.upper()} e Controle {tipo}")
    plt.ylabel('Magnitude (dB)')
    plt.grid(True, which='both', axis='both')
    
    # Gráfico de Fase (em graus)
    plt.subplot(2, 1, 2)  # 2ª posição
    plt.semilogx(bode['frequency'], bode['phase'], 'r')
    plt.ylabel('Fase (graus)')
    plt.xlabel('Frequência (rad/s)')
    plt.grid(True, which='both', axis='both')

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    image_base64 = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return image_base64

def make_open_loop(system, control):
    return ctrl.series(system, control)

def make_closed_loop(open_loop):
    return ctrl.feedback(open_loop, 1)

def make_step_response(closed_loop):
    return ctrl.step_response(closed_loop) # x: time, y: response -> resposta ao degrau sempre é em malha fechada
