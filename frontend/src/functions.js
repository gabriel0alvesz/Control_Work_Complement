function redirect(mode) {
    window.location.href = mode + '.html';
}

function goBack() {
    window.location.href = 'index.html';
}

function resetarForm(param) {
    document.getElementById(param).reset();
    document.getElementById('bodeGraph').innerHTML = 'Gráfico de Bode';
    document.getElementById('stepGraph').innerHTML = 'Gráfico de Resposta ao Degrau';
    document.getElementById('rootGraph').innerHTML = 'Gráfico de Lugar das Raízes';
    
}

function enviarDadosContinuo() {
    const data = {
        K: document.getElementById('K').value,
        Kp: document.getElementById('Kp').value,
        Ki: document.getElementById('Ki').value,
        Kd: document.getElementById('Kd').value,
        TAU: document.getElementById('TAU').value,
        tipo: document.getElementById('tipo').value
    };
    
    fetch('http://127.0.0.1:5000/api/continuo', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(images => {
        var img_bode = "data:image/png;base64," + images.bode_image;
        var img_degrau = "data:image/png;base64," + images.step_image;
        var img_lgr = "data:image/png;base64," + images.lgr_image;

        document.getElementById('bodeGraph').innerHTML = `<img src="${img_bode}" alt="Gráfico de Bode" style="width:100%;">`;
        document.getElementById('stepGraph').innerHTML = `<img src="${img_degrau}" alt="Gráfico de Resposta ao Degrau" style="width:100%;">`;
        document.getElementById('rootGraph').innerHTML = `<img src="${img_lgr}" alt="Gráfico de Lugar das Raízes" style="width:100%;">`;
    })
    .catch(error => console.error('Erro:', error));
}


function enviarDadosDiscreto() {
    const data = {
        K: document.getElementById('K').value,
        Kp: document.getElementById('Kp').value,
        Ki: document.getElementById('Ki').value,
        Kd: document.getElementById('Kd').value,
        TAU: document.getElementById('TAU').value,
        tipo: document.getElementById('tipo').value,
        tempoAmostragem: document.getElementById('tempoAmostragem').value
    };

    fetch('http://127.0.0.1:5000/api/discreto', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(data),
    })
    .then(response => response.json())
    .then(images => {
        var img_bode = "data:image/png;base64," + images.bode_image;
        var img_degrau = "data:image/png;base64," + images.step_image;
        var img_lgr = "data:image/png;base64," + images.lgr_image;

        document.getElementById('bodeGraph').innerHTML = `<img src="${img_bode}" alt="Gráfico de Bode" style="width:100%;">`;
        document.getElementById('stepGraph').innerHTML = `<img src="${img_degrau}" alt="Gráfico de Resposta ao Degrau" style="width:100%;">`;
        document.getElementById('rootGraph').innerHTML = `<img src="${img_lgr}" alt="Gráfico de Lugar das Raízes" style="width:100%;">`;
    })
    .catch(error => console.error('Erro:', error));
}

// function obterDadosSeriais() {
//     fetch('http://127.0.0.1:5000/api/serial-data')
//         .then(response => response.json())
//         .then(data => {
//             if (!data.error) {
//                 document.getElementById('K').value = data.K;
//                 document.getElementById('Kp').value = data.Kp;
//                 document.getElementById('Ki').value = data.Ki;
//                 document.getElementById('Kd').value = data.Kd;
//                 document.getElementById('TAU').value = data.TAU;
//                 document.getElementById('tempoAmostragem').value = data.tempoAmostragem;
//                 console.log("Dados Seriais Atualizados", data);
//             } else {
//                 console.error(data.error);
//             }
//         })
//         .catch(error => console.error('Erro ao obter dados seriais:', error));
// }

// Chame essa função em intervalos para atualizar os dados na interface
// setInterval(obterDadosSeriais, 1000);  // A cada 2 segundos