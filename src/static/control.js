function salvarValor(param) {
    var valor = $(`#${param}`).val();
    $.ajax({
        url: `/salvar-${param}`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ [param]: valor }),
        success: function(response) {
            alert(`${JSON.stringify(response, null, 2)} salvo com sucesso!`);
        }
    });
}

$(document).ready(function() {
    function ajustarVisibilidadeTempo() {
        var modo = $("#modo").val();
        $("#tempoDiv").toggle(modo === "digital");
    }

    function enviarValores() {
        var modo = $("#modo").val();
        var tempo = modo === 'digital' ? $("#tempo").val() : 0.1;
        var tipo = $("input[name='tipoControle']:checked").val() || "erro"
        var tau = $("#tau").val() || 0.01;
        var qsi = $("#qsi").val() || 0.5;

        $.ajax({
            url: '/salvar-valores',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                modo: modo,
                tempo: tempo,
                tipo: tipo,
                tau: tau,
                qsi: qsi,
            }),
            success: function(response) {
                
                if(response.bode_image){
                    var imgSrc = 'data:image/png;base64,' + response.bode_image;
                    $('#bodeImage').attr('src', imgSrc);
                }
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

    setInterval(atualizarPotenciometro, 500);
    $("#modo").change(ajustarVisibilidadeTempo);
    $("#enviar").click(enviarValores);
});