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
        document.getElementById("mensagem-erro").style.display = "block";

        if (meuGrafico) {
            meuGrafico.destroy();
        }

        console.warn("Nenhum dado encontrado para exibir no gráfico.");
        return;
    }

    // Determina as labels e os totais com base no formato dos dados
    let labels;
    let totais;

    if (dados[0].cliente__nome) { 
        labels = dados.map(d => d.cliente__nome);
        totais = dados.map(d => d.total);
    } else if (dados[0].produto__produto) {
        labels = dados.map(d => d.produto__produto);
        totais = dados.map(d => d.total);
    } else if (dados[0].data_da_venda__year) {
        labels = dados.map(d => d.data_da_venda__year);
        totais = dados.map(d => d.total);
    }

    // Verifica se já existe o gráfico e o destrói
    if (meuGrafico) {
        meuGrafico.destroy();
    }

    const tipoGrafico = document.querySelector('select[name="tipo_grafico"]');
    const tipo = tipoGrafico.value === 'quantidade' ? 'Quantidade Total' : 'Valor Monetário (R$)';

    // Verifica o número de barras para decidir se os rótulos serão exibidos
    const exibirRotulos = labels.length <= 15;

    meuGrafico = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: tipo,
                data: totais,
                backgroundColor: 'rgba(34, 139, 34, 1)',  // Verde floresta com opacidade
                borderColor: 'rgba(75, 192, 192, 1)',
                borderWidth: 1
            }]
        },
        options: {
            scales: {
                y: {
                    beginAtZero: true
                }
            },
            plugins: {
                datalabels: exibirRotulos ? { // Só exibe rótulos se for <= 25 barras
                    color: 'black',
                    anchor: 'end',
                    align: 'top',
                    formatter: function(value) {
                        if (tipoGrafico.value === 'valor') {
                            // Garante que o valor seja numérico antes de aplicar o toFixed
                            let numero = Number(value);
                            if (!isNaN(numero)) {
                                // Formata como valor monetário com 2 casas decimais
                                return numero.toFixed(2).replace('.', ','); // Força 2 casas decimais e troca o ponto por vírgula
                            } else {
                                return '';  // Caso não seja um número, não exibe nada
                            }
                        } else {
                            // Exibe normalmente para quantidade
                            return value;
                        }
                    }
                    
                
                } : false  // Desabilita rótulos se houver mais de 25 barras
            }
        },
        plugins: [ChartDataLabels]  // Ativa o plugin de rótulos
    });

    // Exibe o botão de download ao gerar o gráfico
    document.getElementById("download-container").style.display = "block";
}



// Função para baixar o gráfico como PDF
document.getElementById("btn-download").onclick = function() {
    const canvas = document.getElementById('grafico');

    // Usar html2canvas para capturar o gráfico
    html2canvas(canvas).then(function(canvas) {
        const imgData = canvas.toDataURL('image/png');
        const pdf = new jsPDF('landscape'); // Cria um novo PDF em modo paisagem
        const imgWidth = 210; // Largura do PDF em mm (A4)
        const pageHeight = pdf.internal.pageSize.height; // Altura da página
        const imgHeight = (canvas.height * imgWidth) / canvas.width; // Calcula a altura da imagem

        let heightLeft = imgHeight;

        // Calcula as posições para centralizar a imagem
        const x = (pdf.internal.pageSize.width - imgWidth) / 2; // Centraliza horizontalmente
        const y = (pageHeight - imgHeight) / 2; // Centraliza verticalmente

        // Adiciona a imagem ao PDF, dividindo em páginas se necessário
        pdf.addImage(imgData, 'PNG', x, y, imgWidth, imgHeight); // Centraliza no meio
        heightLeft -= pageHeight;

        while (heightLeft >= 0) {
            pdf.addPage();
            pdf.addImage(imgData, 'PNG', x, y, imgWidth, imgHeight); // Centraliza no meio
            heightLeft -= pageHeight;
        }

        pdf.save('grafico_de_vendas.pdf'); // Nome do arquivo PDF
    });
};


document.getElementById("btn-limpar-grafico").onclick = function() {
    if (meuGrafico) {
        meuGrafico.destroy(); // Destrói o gráfico existente
        meuGrafico = null; // Reseta a variável
    }
    document.getElementById("mensagem-erro").style.display = "none"; // Esconde a mensagem de erro
    document.getElementById("download-container").style.display = "none"; // Esconde o botão de download
};

// Limpar Filtros
document.getElementById("btn-limpar-filtros").onclick = function() {
    // Reseta o formulário

    document.getElementById('form-filtros').reset(); 
    
    // Reinicializa o Select2
    $('.select2').select2({
        placeholder: 'Selecione uma opção',
        allowClear: false,
    });
    
    if (meuGrafico) {
        meuGrafico.destroy(); // Destrói o gráfico se existir
        meuGrafico = null; // Reseta a variável
    }
    
    // Certifica que não há erros ou gráficos exibidos
    document.getElementById("mensagem-erro").style.display = "none"; 
    document.getElementById("download-container").style.display = "none"; // Esconde o botão de download
};