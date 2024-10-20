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