function ajustarVisibilidadeTempo() {
    var modo = document.getElementById("modo").value;
    var tempoDiv = document.getElementById("tempoDiv");
    if (modo === "digital") {
        tempoDiv.style.display = "block";
    } else {
        tempoDiv.style.display = "none";
    }
}

function salvarValor(param) {
    var valor = document.getElementById(param).value;
    $.ajax({
        url: `/salvar-${param}`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ valor: valor }),
        success: function(response) {
            alert(param.toUpperCase() + ' salvo com sucesso!');
        }
    });
}

function enviarValores() {
    var modo = document.getElementById("modo").value;
    var tempo = document.getElementById("tempo").value;
    var tau = document.getElementById("tau").value;
    var qsi = document.getElementById("qsi").value;

    $.ajax({
        url: '/salvar-valores',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({
            modo: modo,
            tempo: tempo,
            tau: tau,
            qsi: qsi
        }),
        success: function(response) {
            var valores = `
                Modo: ${response.modo}<br>
                Tempo: ${response.tempo}<br>
                Tau: ${response.tau}<br>
                Qsi: ${response.qsi}<br>
                Kp: ${response.kp}<br>
                Kd: ${response.kd}<br>
                Ki: ${response.ki}
            `;
            document.getElementById("valores").innerHTML = valores;
            alert('Valores enviados e salvos com sucesso!');
        }
    });
}

function atualizarPotenciometro() {
    $.ajax({
        url: '/atualizar-potenciometro',
        type: 'GET',
        success: function(response) {
            $('#kp').val(response.valor);
            $('#kd').val(response.valor);
            $('#ki').val(response.valor);
        }
    });
}

setInterval(atualizarPotenciometro, 1000); // Atualiza a cada 1 segundo
