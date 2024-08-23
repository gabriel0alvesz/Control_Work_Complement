# Trabalho integrado de Controle de Sistemas Dinâmicos 2 e Microcontroladores

Conecte a um Arduino ou outro microcontrolador
•	Um teclado de membrana ou outro;
•	1 ou 3 potenciômetro (s) ligado(s) a entrada(s) analógica(s)

Sabemos que um sinal quando é lido por um microprocessador ocorre um processo de discretização. No entanto para que possamos obter um sinal próximo pode-se obter um sistema discreto que se assemelhe ao comportamento contínuo, diminuindo o intervalo de amostragem para um valor muito pequeno.
**Considere um sistema com realimentação unitária negativa**

-	O usuário deverá iniciar o programa e escolher, por meio do teclado, entre uma abordagem contínua ou digital;
-	Se o usuário optar por uma análise contínua, automaticamente o programa deverá atribuir um tempo de amostragem bem pequeno, a fim de obter um processo discreto que se aproxime do contínuo;
-	Se o usuário escolher pelo modo digital o usuário deverá digitar o tempo de amostragem utilizando o teclado;
-	Após isso, na tela permita ao usuário escolher a estratégia de controle (P, PI, PD, PID), se quiser aprofundar insira compensadores;
-	Gere os gráficos da resposta no tempo e na frequência (degrau, bode e lgr);
-	Está facultado utilizar para o processo as funções canônicas de transferência em s e em z para primeira e/ou segunda ordem;
-	Sobre os parâmetros da função de transferência, como tau, qsi entre outros, possibilite ao usuário inserir os valores também por meio do teclado;
-	Os usuários poderão ajustar os valores das constantes (kp, ki e kd) de controle através do giro do potenciômetro (pode usar um potenciômetro para cada constante de controle, ou 1 único para todas). Em tempo real à medida que gira o potenciômetro da constante de controle o usuário poderá visualizar o sistema variar a resposta.
-	Permita ao usuário fazer download do diagrama de blocos e das figuras de resposta.

---
### 1ª Parte
- [x] Criar servidor Flask
- [x] Cria servidor comum via Socket - Middleware para plotagem
- [x] Potenciometro conectando no servidor
- [x] Envio de Dados para o servidor
- [ ] Aceitar comunicação via teclado matricial
- [x] inputs de *TAU* e *qsi*
- [x] Escolha entre continuo ou digital

### 2ª Parte
- [ ] Gerar pontos para plotagem dos gráficos 
  - [ ] Degrau
  - [ ] Bode
  - [ ] LGR

### 3ª Parte
- [ ] Envio dos pontos para plotagem do gráfico na página
- [ ] Plotagem dos grafos
- [ ] Possibilidade de download dos gráficos