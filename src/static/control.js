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
                Modo: ${modo}<br>
                Tempo: ${tempo}<br>
                Tau: ${tau}<br>
                Qsi: ${qsi}<br>
                Kp: ${response.kp}<br>
                Kd: ${response.kd}<br>
                Ki: ${response.ki}
            `;
            document.getElementById("valores").innerHTML = valores;
            plotarGraficos(response);
            alert('Valores enviados e salvos com sucesso!');
        }
    });
}

function plotarGraficos(data) {
    // Plotar gráfico de Bode
    var trace1 = {
        x: data.bode.frequencias,
        y: data.bode.magnitude,
        mode: 'lines',
        name: 'Magnitude'
    };

    var trace2 = {
        x: data.bode.frequencias,
        y: data.bode.fase,
        mode: 'lines',
        name: 'Fase'
    };

    var layout1 = {
        title: 'Gráfico de Bode',
        xaxis: { title: 'Frequência (rad/s)' },
        yaxis: { title: 'Magnitude (dB) / Fase (°)' }
    };

    Plotly.newPlot('bodePlot', [trace1, trace2], layout1);

    // Plotar gráfico de resposta ao degrau
    var trace3 = {
        x: data.degrau.tempo,
        y: data.degrau.resposta,
        mode: 'lines',
        name: 'Resposta ao Degrau'
    };

    var layout2 = {
        title: 'Resposta ao Degrau',
        xaxis: { title: 'Tempo (s)' },
        yaxis: { title: 'Resposta' }
    };

    Plotly.newPlot('degrauPlot', [trace3], layout2);
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
