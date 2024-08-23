$(document).ready(function() {
    function ajustarVisibilidadeTempo() {
        var modo = $("#modo").val();
        $("#tempoDiv").toggle(modo === "digital");
    }

    function salvarValor(param) {
        var valor = $(`#${param}`).val();
        $.ajax({
            url: `/salvar-${param}`,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ valor: valor }),
            success: function(response) {
                alert(`${param.toUpperCase()} salvo com sucesso!`);
            }
        });
    }

    function enviarValores() {
        var modo = $("#modo").val();
        var tempo = modo === 'digital' ? $("#tempo").val() : 0.1;
        var tau = $("#tau").val() || 0.01;
        var qsi = $("#qsi").val() || 0.5;

        $.ajax({
            url: '/salvar-valores',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                modo: modo,
                tempo: tempo,
                tau: tau,
                qsi: qsi,
                kp: $("#kp").val(),
                kd: $("#kd").val(),
                ki: $("#ki").val()
            }),
            success: function(response) {
                plotarGraficos(response);
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

    function plotarGraficos(dados) {
        var trace1 = {
            x: dados.bode.frequencia,
            y: dados.bode.magnitude,
            mode: 'lines',
            name: 'Bode - Magnitude'
        };
        var trace2 = {
            x: dados.bode.frequencia,
            y: dados.bode.fase,
            mode: 'lines',
            name: 'Bode - Fase'
        };
        var trace3 = {
            x: dados.degrau.tempo,
            y: dados.degrau.resposta,
            mode: 'lines',
            name: 'Resposta ao Degrau'
        };
        var trace4 = {
            x: dados.ldr.ganhos,
            y: dados.ldr.raizes,
            mode: 'lines',
            name: 'Lugar das Raízes'
        };

        Plotly.newPlot('graficoBode', [trace1, trace2]);
        Plotly.newPlot('graficoDegrau', [trace3]);
        Plotly.newPlot('graficoLDR', [trace4]);
    }

    setInterval(atualizarPotenciometro, 1000);
    $("#modo").change(ajustarVisibilidadeTempo);
    $("#enviar").click(enviarValores);
});
