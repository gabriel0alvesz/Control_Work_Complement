function salvarValor(param) {
    var valor = $(`#${param}`).val();
    $.ajax({
        url: `/salvar-${param}`,
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({ [param]: valor }),
        success: function(response) {
            $(`#${param}-btn`).addClass('saved');
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
        var tipo = $("input[name='tipoControle']:checked").val() || "PID"
        var tau = $("#tau").val() || 0.01;

        $.ajax({
            url: '/salvar-valores',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                modo: modo,
                tempo: tempo,
                tipo: tipo,
                tau: tau,
            }),
            success: function(response) {

                exibeValores(response)

                // console.log(response)
                
                if(response.bode_image){
                    var img_bode = "data:image/png;base64," + response.bode_image;
                    var img_degrau = "data:image/png;base64," + response.degrau_image;
                    var img_lgr = "data:image/png;base64," + response.lgr_image;
                    $('#bodeImage').attr('src', img_bode);
                    $('#degrauImage').attr('src', img_degrau);
                    $('#lgrImage').attr('src', img_lgr);
                }
            }
        });
    }

    function exibeValores(response) {
        var texto = `Kp = ${response.Ks[0] || 0} \t Ki = ${response.Ks[1] || 0} \t Kd = ${response.Ks[2] || 0}\n
        Modo = ${(response.modo)} \t Tempo = ${String(response.tempo)} \t Controle = ${String(response.tipo)}`;

        $('#exibeValoresFinais span').html(texto)
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

    // Função para resetar o formulário
    function resetarFormulario() {
        
        document.getElementById('kp-btn').classList.remove('saved')
        document.getElementById('ki-btn').classList.remove('saved')
        document.getElementById('kd-btn').classList.remove('saved')

        // Limpa a seleção de radio buttons
        document.querySelectorAll('input[type="radio"]').forEach(radio => {
            radio.checked = false;
        });

        // Limpa a seleção do dropdown
        document.getElementById('modo').value = 'continuo';

        // Oculta o tempoDiv
        document.getElementById('tempoDiv').style.display = 'none';

        // Limpa os valores finais exibidos
        document.getElementById('exibeValoresFinais').innerHTML = '';

        // Oculta as imagens
        document.querySelectorAll('#graficoBode, #graficoDegrau, #graficoLDR').forEach(div => {
            div.style.display = 'none';
        });
    }

    // Adicione o event listener ao botão de reset
    document.getElementById('reset').addEventListener('click', resetarFormulario);


    setInterval(atualizarPotenciometro, 500);
    $("#modo").change(ajustarVisibilidadeTempo);
    $("#enviar").click(enviarValores);
});