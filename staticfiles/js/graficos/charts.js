// Inicializa o Select2 nos campos de seleção
$(document).ready(function() {
    $('.select2').select2({
        placeholder: 'Selecione uma opção',
        allowClear: false,
    });   
});

$(document).ready(function () {
    $('.select2').select2();
});



document.getElementById('form-filtros').onsubmit = async function(event) {
    event.preventDefault();
    
    // Cria os parâmetros de consulta a partir do formulário
    const params = new URLSearchParams(new FormData(this));
    
    // Faz a requisição GET com os parâmetros de consulta
    const response = await fetch(`?${params}`);
    const dados = await response.json();
    gerarGrafico(dados);
};

let meuGrafico;  // Variável para armazenar a referência do gráfico

async function gerarGrafico(dados) {

    document.getElementById("mensagem-erro").style.display = "none";
    document.getElementById("download-container").style.display = "none"; 
    
    const ctx = document.getElementById('grafico').getContext('2d');

    // Verifica se há dados
    if (dados.length === 0) {
        // Exibe a mensagem de erro
        document.getElementById("mensagem-erro").style.display = "block";

        // Destroi o gráfico se existir
        if (meuGrafico) {
            meuGrafico.destroy();
        }

        console.warn("Nenhum dado encontrado para exibir no gráfico.");
        return;  // Não tenta desenhar o gráfico
    }

    // Determina as labels e os totais com base no formato dos dados
    let labels;
    let totais;

    if (dados[0].cliente__nome) { // Vendedor e ano
        labels = dados.map(d => d.cliente__nome);
        totais = dados.map(d => d.total);
    } else if (dados[0].produto__produto) { // Vendedor e cliente
        labels = dados.map(d => d.produto__produto);
        totais = dados.map(d => d.total);
    } else if (dados[0].data_da_venda__year) { // Apenas vendedor
        labels = dados.map(d => d.data_da_venda__year); // Anos
        totais = dados.map(d => d.total); // Totais correspondentes
    }

    // Verifica se já existe o gráfico e o destrói
    if (meuGrafico) {
        meuGrafico.destroy();
    }

    const tipoGrafico = document.querySelector('select[name="tipo_grafico"]');
    const tipo = tipoGrafico.value === 'quantidade' ? 'Quantidade Total' : 'Valor Monetário';

    meuGrafico = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: tipo,
                data: totais,
                backgroundColor: 'rgba(75, 192, 192, 0.2)',
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Exibe o botão de download ao gerar o gráfico
    document.getElementById("download-container").style.display = "block";

}

// Função para baixar o gráfico como imagem PNG
document.getElementById("btn-download").onclick = function() {
    const canvas = document.getElementById('grafico');
    const link = document.createElement('a');
    link.href = canvas.toDataURL(); // Converte o gráfico em uma URL de imagem
    link.download = 'grafico_de_vendas.png';  // Nome do arquivo de download
    link.click();  // Inicia o download
};