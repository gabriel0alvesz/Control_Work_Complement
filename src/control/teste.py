# teste gerado com gpt

import matplotlib.pyplot as plt
from control.matlab import bode
from control import TransferFunction

# Definir a função de transferência G(s) = 1 / (s^2 + s + 1)
numerador = [1]  # Numerador da função de transferência
denominador = [1, 1, 1]  # Denominador da função de transferência

# Criar a função de transferência
sistema = TransferFunction(numerador, denominador)

# Gerar o diagrama de Bode
magnitude, fase, frequencias = bode(sistema, dB=True)

# Mostrar o gráfico
plt.show()
