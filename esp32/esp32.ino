#include <Keypad.h>

#define POTENTIOMETER_PIN 36 // Pino do ESP32 conectado ao potenciômetro
#define ROW_NUM 4 // Número de linhas do teclado matricial
#define COLUMN_NUM 4 // Número de colunas do teclado matricial

char keys[ROW_NUM][COLUMN_NUM] = {
  {'1','2','3','A'},
  {'4','5','6','B'},
  {'7','8','9','C'},
  {'.','0','#','D'}
};

// Definição dos pinos do teclado matricial
byte pin_rows[ROW_NUM] = {14, 27, 26, 25}; 
byte pin_column[COLUMN_NUM] = {33, 32, 18, 19}; 

Keypad keypad = Keypad(makeKeymap(keys), pin_rows, pin_column, ROW_NUM, COLUMN_NUM);

// Variáveis para armazenar os valores recebidos do teclado e potenciômetro
String K = "";
String current_value = "";
String temp_value = "";
String U = "";
String T = "";
String Kp = "", Ki = "", Kd = "";
bool ajustandoPotenciometro = false; // Controle para indicar ajuste do potenciômetro
bool ajustesExtras = false;
char parametroSelecionado = '\0';    // Indica qual parâmetro está sendo ajustado

void setup() {
  Serial.begin(115200);
  Serial.println("Iniciando...");

  pinMode(POTENTIOMETER_PIN, INPUT);
}

void loop() {
  char key = keypad.getKey();

  // Se a tecla 'A' for pressionada, iniciar ajuste do potenciômetro
  if (key == 'A') {
    Serial.println("1 - Kp \t2 - Ki \t3 - Kd");
    parametroSelecionado = selecionarParametro();
    if (parametroSelecionado != '\0') {
      ajustandoPotenciometro = true;
    }
  }

  // Enquanto estiver ajustando, o valor do potenciômetro será lido continuamente
  if (ajustandoPotenciometro) {
    int potValue = analogRead(POTENTIOMETER_PIN); // Lê o valor do potenciômetro (0-4095)
    float mappedValue = ((float)potValue / 4095.0) * 10.0; // Ajusta para a faixa desejada (0 a 10)
    String valorPotenciometro = String(mappedValue, 2); // Converte o valor para string com 2 casas decimais

    // Atualiza o valor do parâmetro selecionado
    if (parametroSelecionado == 'P') {
      current_value = valorPotenciometro;
      Serial.print("Kp: ");
    } else if (parametroSelecionado == 'I') {
      current_value = valorPotenciometro;
      Serial.print("Ki: ");
    } else if (parametroSelecionado == 'D') {
      current_value = valorPotenciometro;
      Serial.print("Kd: ");
    }
    Serial.println(valorPotenciometro);

    delay(500); // Intervalo de atualização para leitura suave
  }

  if(key == '#'){
    if (parametroSelecionado == 'P') {
      Kp = current_value;
      Serial.printf("Enviando...");
      Serial.println(Kp);
    } else if (parametroSelecionado == 'I') {
      Ki = current_value;
      Serial.printf("Enviando...");
      Serial.println(Ki);
    } else if (parametroSelecionado == 'D') {
      Kd = current_value;
      Serial.printf("Enviando...");
      Serial.println(Kd);
    }
    ajustandoPotenciometro = false;
  }

  if (key == 'B') {
    Serial.println("Enviando Json com os dados de Kp, Ki, e Kd");
    enviarDadosGanhos(Kp, Ki, Kd);
  }


  if (key == 'C'){
    Serial.println("1 - K \t2 - TAU \t3 - Tempo");
    ajustesExtras = true;
  }
    
  if(ajustesExtras){
    parametroSelecionado = selecionarParametro();

    if (parametroSelecionado == 'K') {
      K = receberValorTeclado('K');
      Serial.printf("Valor de K salvo: ");
      Serial.println(K);
      ajustesExtras = false;
    } else if (parametroSelecionado == 'U') {
      U = receberValorTeclado('U');
      Serial.printf("Valor de Tau salvo: ");
      Serial.println(U);
      ajustesExtras = false;
    } else if (parametroSelecionado == 'T') {
      T = receberValorTeclado('T');
      Serial.printf("Valor de Tempo salvo: ");
      Serial.println(T);
      ajustesExtras = false;
    }
  }
  
  
  if (key == 'D') {
    enviarDadosVariaveis(K, U, T);
  }
}


char selecionarParametro() {
  char param = '\0';
  while (param == '\0') {
    char key = keypad.getKey();
    if (key == '1') param = 'P'; // Seleciona Kp
    if (key == '2') param = 'I'; // Seleciona Ki
    if (key == '3') param = 'D'; // Seleciona Kd
    if (key == '4') param = 'K'; // Seleciona Ganho
    if (key == '5') param = 'U'; // Seleciona TAU
    if (key == '6') param = 'T'; // Seleciona Tempo de Amostragem
  }
  return param;
}

// Função para simular a inserção de valores pelo teclado matricial
String receberValorTeclado(char letra) {
  String aux = "";
  aux += letra;
  aux += ": ";

  Serial.println(aux);
  char key;

  while (true) {
    key = keypad.getKey();
    if (key != NO_KEY) {
      if (key == '#') { // Confirma o valor
        return aux;
      } else {
        aux += key;
        Serial.println(aux);
      }
    }
  }
}

// Função para enviar os dados pela porta Serial
void enviarDadosGanhos(String Kp, String Ki, String Kd) {
  String jsonData = "{";
  jsonData += "\"Kp\":\"" + Kp + "\",";
  jsonData += "\"Ki\":\"" + Ki + "\",";
  jsonData += "\"Kd\":\"" + Kd + "\"";
  jsonData += "}";
  Serial.println(jsonData);
}

void enviarDadosVariaveis(String K, String U, String T) {
  String jsonData = "{";
  jsonData += "\"K\":\"" + K + "\",";
  jsonData += "\"U\":\"" + U + "\",";
  jsonData += "\"T\":\"" + T + "\"";
  jsonData += "}";
  Serial.println(jsonData);

}
